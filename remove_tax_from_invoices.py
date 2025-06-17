#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import date
import io
import sys
import re

from easyverein import EasyvereinAPI, EasyvereinAPIException
from easyverein.models.invoice import InvoiceFilter
from easyverein.models import InvoiceUpdate, InvoiceCreate

# change list
changes = {
    # invoice id: change set dict

    # malformed date
    66968819: dict(date=date(2021,5,21)),
    162534629: dict(date=date(2023,4,23)),
}

api_key = os.getenv('EV_API_KEY', '')
with (Path('.') / "config.json").open() as fp:
    config = json.load(fp)
if not api_key:
    api_key = config['API_TOKEN']

ev_client = EasyvereinAPI(api_key, auto_retry=True)

search = InvoiceFilter(date__gt=date(2021,12,31))#, id__in=[194598380])
invoices = ev_client.invoice.get_all(search=search)
missing_attachments = []
for invoice in invoices:
    if invoice.kind in ["membership", "kind"]:
        continue
    
    print(invoice.id, invoice.kind, invoice.invNumber, invoice.date, invoice.tax, invoice.totalPrice, sep='\t')
    print("https://hexa.easyverein.com/app/bookkeeping/invoice/", invoice.id, sep="")
    print(invoice.receiver)

    # Sanity checks:
    if invoice.templateName is not None:
        print("!!! templateName")
        continue
    if invoice.dateSent is not None:
        print("!!! dateSent")
        continue
    if invoice.date < date(2021,3,4) and invoice.id not in [162534629, 66968819]:
        print("!!! date")
        continue
    if invoice.dateItHappend is not None and invoice.dateItHappend < date(2021,3,4):
        print("!!! dateItHappend")
        continue

    if invoice.tax == 0:
        pass
        #continue
    #print(invoice)

    # 1. Download attached document
    print("# 1 DOWNLOAD or local selection")
    missing_attachment = True
    if invoice.path is not None:
        try:
            data, headers = ev_client.invoice.get_attachment(invoice)
            file_name = headers['Content-Disposition'].replace('attachment; filename="', "").replace('"', "")
            attachment = Path('temp')/file_name
            with attachment.open('wb') as f:
                f.write(data)
            print(attachment)
            missing_attachment = False
        except KeyError:
            print("!!! attachment not downloadable", dict(invoice.path.query_params())['path'])
            attachment = None
    else:
        print("!!! no attachment")
        attachment = None
    
    if attachment is None:
        while attachment is None or not attachment.is_file():
            print('new attachment: ', end="")
            sys.stdout.flush()
            readline = sys.stdin.readline().strip().replace(r"\ ", " ").replace(r'\#', '#')
            if readline == "":
                print("SKIP")
                attachment = None
                break
            attachment = Path(readline)
        if attachment is None:
            continue

    if invoice.tax == 0 and not missing_attachment:
        print("all good\n")
        continue

    # 2. Remove from booking and save booking reference!
    print("# 2 REMOVE FROM BOOKING")
    if len(invoice.relatedBookings) > 1:
        print("!!! multiple related bookings")
        break
    elif len(invoice.relatedBookings) == 0:
        booking_url, booking = None, None
    else:
        booking_url = invoice.relatedBookings[0]
        booking = ev_client.c.fetch_one(booking_url)
        print(booking['id'], booking_url)
        if len(booking['relatedInvoice']) != 1:
            print("!!! multiple related invoices")
            break
        ev_client.c._do_request("patch", booking_url, data={'relatedInvoice':[]})

    # 3. Delete old invoice (to free up invNumber)
    print("# 3 DELETE OLD INVOICE")
    ev_client.invoice.delete(invoice, delete_from_recycle_bin=True)

    # 4. Create new invoice with reference to booking
    print("# 4 CREATE NEW INVOICE")
    invoice_create = InvoiceCreate(**{k:v for k,v in invoice.__dict__.items() if k in [
        "gross", "date", "dateItHappend", "invNumber", "receiver", "description", "totalPrice", "kind"]})
    invoice_create.isDraft = True
    if booking is not None:
        invoice_create.relatedBookings = [booking_url]
    
    for k,v in changes.get(invoice.id, {}).items():
        setattr(invoice_create, k, v)
    #print(invoice_create)

    new_invoice = ev_client.invoice.create(invoice_create)
    print('new_invoice', new_invoice.id)

    # 5. Upload attachment and finalize
    print("# 5 UPLOAD ATTACHMENT")
    ev_client.invoice.upload_attachment(new_invoice, attachment)
    
    ev_client.invoice.update(new_invoice, InvoiceUpdate(isDraft=False))
    new_invoice.isDraft = False

    # QuickFix: Update booking amount to recalc paymentDifference
    if booking is not None:
        ev_client.c._do_request("patch", booking_url, data={'amount': booking['amount']})

    # 6. Clean up attachment
    #attachment.unlink()

    print("\n---------------\n\n")

#    break
#
#from IPython import embed; embed();


print("missing attachments: ", len(missing_attachments), missing_attachments)

