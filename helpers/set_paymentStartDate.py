#!/usr/bin/env python3
import sys
import requests
from pprint import pprint
from datetime import datetime

API_URL = "https://easyverein.com/api/stable/member"
API_TOKEN = "-"  # DO NOT SHARE!

s = requests.Session()
s.headers.update({'Authorization': 'Token '+API_TOKEN})
# Get list of all members
req = s.get(API_URL + '?query={id,emailOrUserName,joinDate,_paymentStartDate}')
res = req.json()
while 'results' in res:
    # For each member:
    for m in res['results']:
        # calculate _paymentStartDate from joinDate:
        try:
            joinDate = datetime.fromisoformat(m['joinDate'])
        except TypeError:
            print('   ', 'missing joinDate')
            continue
        paymentStartDate = joinDate.replace(day=1, month=1, hour=12).isoformat()
        # set _paymentStartDate to Jan 1 of joinDate
        print(m['emailOrUserName'], joinDate, paymentStartDate, m['_paymentStartDate'], m['_paymentStartDate'] is None or m['_paymentStartDate'][:10] != paymentStartDate[:10])
        if m['_paymentStartDate'] is None or m['_paymentStartDate'][:10] != paymentStartDate[:10]:
            # patch user to have new _paymentStartDate
            patch_req = s.patch(API_URL + '/' + str(m['id']),
                json={'_paymentStartDate': paymentStartDate})
            if not patch_req.ok:
                print('    ', patch_req.status_code, patch_req.reason)
                print('    ', patch_req.content)
                sys.exit(0)
    if res['next']:
        req = requests.get(res['next'], headers={'Authorization': 'Token '+API_TOKEN})
        res = req.json()
    else:
        break
