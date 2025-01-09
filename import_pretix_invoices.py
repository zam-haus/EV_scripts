#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import date
import io
import sys
import re
from pprint import pprint

from easyverein import EasyvereinAPI, EasyvereinAPIException
from easyverein.models.invoice import InvoiceFilter
from easyverein.models import InvoiceUpdate, InvoiceCreate

import pandas as pd

def read_invoices_excel(p):
    data = pd.read_excel(p, keep_default_na=False)
    data.fillna('None')
    data = data.to_dict('records')
    # remove/ignore cancellations and cancelled 
    remove_invNums = set()
    for row in data:
        if row["Invoice type"] == "Cancellation":
            remove_invNums.add(row["Cancellation of"])
            remove_invNums.add(row["Invoice number"])
    data = [r for r in data if r["Invoice number"] not in remove_invNums]
    return data


def get_corresponding_booking(ev_client, code, amount):
    result = ev_client.c.fetch_paginated(
        f"https://hexa.easyverein.com/api/v1.7/booking?search={code}&amount={amount}")
    if len(result) == 1:
        return result[0]
    else:
        print(f"none or too many bookings: ", result, file=sys.stderr, end=" ", flush=True)
        return None


def main():
    if len(sys.argv) < 3:
        print("Usage:",sys.argv[0],"invoices-excel.xlsx path-to-invoice-pdf-folder")

    api_key = os.getenv('EV_API_KEY', '')
    with (Path('.') / "config.json").open() as fp:
        config = json.load(fp)
    if not api_key:
        api_key = config['API_TOKEN']

    ev_client = EasyvereinAPI(api_key, auto_retry=True)

    # Order of things
    # 1. read invoices from excel file
    invoices = read_invoices_excel(Path(sys.argv[1]))

    # 2. find corresponding pdfs
    for i in invoices:
        p = Path(sys.argv[2])/(i['Invoice number']+'-'+i['Order code']+'.pdf')
        i['invoice-pdf'] = p if p.exists() else None

    # from here on we process each invoice individually
    for i in invoices:
        print(i['Order code'], end=" ", flush=True, file=sys.stderr)
        # 3. find matching bank transfer and book (optional)
        # compare amount and transfer comment with Order code
        booking = get_corresponding_booking(ev_client, i['Order code'], i['Total value (with taxes)'])
        if booking:
            print(f'booking={booking['id']}', end=" ", flush=True, file=sys.stderr)

        # 4. create invoice and upload pdf
        invoice_create = InvoiceCreate(
            kind="revenue",
            date=i['Date'],
            dateItHappend="2024-11-20",  ## TODO event date
            invNumber=i['Invoice number'],
            refNumber=f"VULCAVOW24-{i['Order code']}",  ## TODO event prefix
            receiver=f"{i['Invoice recipient: Company']}\n{i['Invoice recipient: Name']}\n{i['Invoice recipient: Street address']}\n{i['Invoice recipient: ZIP code']} {i['Invoice recipient: City']}\n{i['Invoice recipient: Country']}",
            totalPrice=i['Total value (with taxes)'],
            tax=f"{i['Total value (with taxes)']-i['Total value (without taxes)']}",
            taxRate="7.00",
            gross=True)
        if not invoice_create.receiver.strip():
            invoice_create.receiver = f"UNBEKANNT\n{i['E-mail address']}"
        invoice_create.isDraft = True
        try:
            invoice = ev_client.invoice.create(invoice_create)
        except EasyvereinAPIException as e:
            print(e)
            continue

        if i["invoice-pdf"]:
            ev_client.invoice.upload_attachment(invoice, i["invoice-pdf"])
            print(f'attached', end=" ", flush=True, file=sys.stderr)
        invoice = ev_client.invoice.update(invoice, InvoiceUpdate(isDraft=False))
        print(f'invoice={invoice.id}', end=" ", flush=True, file=sys.stderr)

        if booking:
            invoice_create.relatedBookings = [booking['id']]
            invoice = ev_client.invoice.update(invoice, InvoiceUpdate(relatedBookings=[booking['id']]))

        # 5. Update booking amount to recalc paymentDifference (quick fix)
        if invoice.relatedBookings:
            ev_client.c._do_request("patch", invoice.relatedBookings[0],
                                    data={'billingAccount': "https://easyverein.com/api/v1.7/billing-account/880"})
        print('.', file=sys.stderr)

if __name__ == "__main__":
    main()