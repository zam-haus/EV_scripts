#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import datetime
from collections import defaultdict

from easyverein import EasyvereinAPI

api_key = os.getenv('EV_API_KEY', '')
with (Path('.') / "config.json").open() as fp:
    config = json.load(fp)
if not api_key:
    api_key = config['API_TOKEN']

#logging.basicConfig(level=logging.DEBUG)
ev_client = EasyvereinAPI(api_key, auto_retry=True)

# read all bookings (that are not blocked!)
bookings = ev_client.c.fetch_paginated(
    "https://hexa.easyverein.com/api/v1.7/booking?query={id,amount,date,description,receiver,bookingProject{projectCostCentre}}&blocked=false")
# id,billingId,receiver,description
sum_per_project_year = defaultdict(lambda: defaultdict(float))
bookings_per_project = defaultdict(list)

# compile pro project per year lists and sums
years = set()
for b in bookings.result:
    pcc = None
    if b['bookingProject']:
        pcc = b['bookingProject']['projectCostCentre']
    
    year = str(datetime.fromisoformat(b['date']).year)
    years.add(year)
    sum_per_project_year[pcc][year] += float(b['amount'])
    bookings_per_project[pcc].append(b)


# save to csv
years = sorted(years)
print("sphaere;KSt;"+";".join(years)+";Datenstand "+datetime.now().isoformat()+";booking_ids;")
for pcc in sorted(sum_per_project_year, key=lambda k: '' if k is None else k):
    if pcc:
        print(";/".join(pcc.split('/')), end=";")
    else:
        print(";;", end="")
    for y in years:
        print("{:.2f}".format(sum_per_project_year[pcc][y]).replace('.', ','), end=";")
    if pcc in bookings_per_project:
        print(" ".join([str(b['id']) for b in bookings_per_project[pcc]]), end=";")
    print()

