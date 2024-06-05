#!/usr/bin/env python3
import os
from pathlib import Path
import json
from datetime import date
import io
import sys
from urllib.request import urlopen
import csv
from io import StringIO

from easyverein import EasyvereinAPI, EasyvereinAPINotFoundException
from easyverein.models.invoice import InvoiceFilter
from easyverein.models import InvoiceUpdate, InvoiceCreate

api_key = os.getenv('EV_API_KEY', '')
with (Path('.') / "config.json").open() as fp:
    config = json.load(fp)
if not api_key:
    api_key = config['API_TOKEN']

ev_client = EasyvereinAPI(api_key, auto_retry=True)


# Load google spreadsheet with Kastenstellenplan
url = 'https://docs.google.com/spreadsheets/d/1D3I7mYO-8TFBje3JLh4OuOrWVAG_LDeWYy-JgADJN1o/export?gid=0&format=csv'

print("Fetching csv from google sheet:")
print(url)

with urlopen(url) as f:
    rawcsv = f.read().decode('utf-8')
kostenstellentabelle = csv.reader(StringIO(rawcsv))
next(kostenstellentabelle)  # skip headers (1/2)
next(kostenstellentabelle)  # skip headers (2/2)

sphaeren_names = {
    "1": "ideell",
    "2": "zweck",
    "3": "wirtschaftlich",
    "4": "vermögensverwaltung",
    "9": "ohne Sphäre",
}
sphaeren_shorts = {
    "1": "ID",
    "2": "ZW",
    "3": "WG",
    "4": "VV",
    "9": "OS",
}

projects = []
for sphaeren, kstnr, titel, *_ in kostenstellentabelle:
    print(sphaeren, kstnr, titel)
    for sp in sphaeren:
        d = {
                "name": titel + " (" + sphaeren_names[sp] + ") " + sp + kstnr,
                "short": sphaeren_shorts[sp],
                "budget": '0.00',
                "projectCostCentre": sp+kstnr,
            }
        projects.append(d)


projects_by_pcc = {d['projectCostCentre']: d for d in projects}

# GET ALL PROJECTS FROM eV
projects_eV = ev_client.c.fetch_paginated("https://hexa.easyverein.com/api/v1.7/booking-project")
projects_eV_by_pcc = {d['projectCostCentre']: d for d in projects_eV}

# GET USAGE OF PROJECTS
project_usage_by_pcc = {}
for b in ev_client.c.fetch_paginated(
        "https://hexa.easyverein.com/api/v1.7/booking?query={bookingProject{projectCostCentre}}"):
    if b['bookingProject'] is not None:
        pcc = b['bookingProject']['projectCostCentre']
        project_usage_by_pcc[pcc] = project_usage_by_pcc.get(pcc, 0) + 1

# UPDATE
for d in projects:
    if d['projectCostCentre'] in projects_eV_by_pcc:
        d_eV = projects_eV_by_pcc[d['projectCostCentre']]
        for k in d:
            if d[k] != d_eV[k]:
                print("CHANGE", repr(d_eV[k]), "->", repr(d[k]))
                print(ev_client.c._do_request(
                    "patch", "https://hexa.easyverein.com/api/v1.7/booking-project/%s" % d_eV['id'], data=d))

# CREATE
for d in projects:
    if d['projectCostCentre'] not in projects_eV_by_pcc:
        print("CREATE", d)
        print(ev_client.c._do_request("post", "https://hexa.easyverein.com/api/v1.7/booking-project", data=d))

# DELETE
for p in projects_eV:
    if p['projectCostCentre'] not in projects_by_pcc:
        print("DELETE!", p)
        # Check if used
        if project_usage_by_pcc.get(p['projectCostCentre'], 0) > 0:
            print("IN USE BY %s INVOICES. NOT DELETED!" % project_usage_by_pcc[p['projectCostCentre']])
        else:
            try:
                while True:
                    ev_client.c._do_request(
                        "delete", "https://hexa.easyverein.com/api/v1.7/booking-project/%s" % p['id'])
            except EasyvereinAPINotFoundException:
                # all good
                pass