#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import datetime
import io
import sys
from collections import defaultdict

from easyverein import EasyvereinAPI, EasyvereinAPINotFoundException
from easyverein.models.invoice import InvoiceFilter
from easyverein.models import InvoiceUpdate, InvoiceCreate

api_key = os.getenv('EV_API_KEY', '')
with (Path('.') / "config.json").open() as fp:
    config = json.load(fp)
if not api_key:
    api_key = config['API_TOKEN']

ev_client = EasyvereinAPI(api_key, auto_retry=True)

# read all bookings (that are not blocked!)
bookings = ev_client.c.fetch_paginated(
    "https://hexa.easyverein.com/api/v1.7/booking?query={amount,date,bookingProject{projectCostCentre}}&blocked=false")
# id,billingId,receiver,description
bookings_per_project_year = defaultdict(lambda: defaultdict(float))

# compile pro project per year lists and sums
years = set()
for b in bookings:
    pcc = None
    if b['bookingProject']:
        pcc = b['bookingProject']['projectCostCentre']
    
    year = str(datetime.fromisoformat(b['date']).year)
    years.add(year)
    bookings_per_project_year[pcc][year] += float(b['amount'])


# save to csv
years = sorted(years)
print("sphaere;KSt;"+";".join(years)+";Datenstand "+datetime.now().isoformat())
for pcc in bookings_per_project_year:
    if pcc:
        print(";/".join(pcc.split('/')), end=";")
    else:
        print(";;", end="")
    for y in years:
        print("{:.2f}".format(bookings_per_project_year[pcc][y]).replace('.', ','), end=";")
    print()

