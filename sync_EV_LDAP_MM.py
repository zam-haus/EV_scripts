#!/usr/bin/env python3

# Goal:
# * set LDAP ID in eV profile for all ppl that have an LDAP/SSO account
#   match using email
# * sync active eV membership with LDAP membership of "Mitglieder" group
#   eV -> LDAP
#   remove all accounts that are either not matched to eV
#   or with inactive eV membership status
# * report unmatched LDAP accounts for manual linking
# * update mailman betreiberverein-mitglieder

import sys
from pprint import pprint
from datetime import datetime
from copy import deepcopy
import subprocess
from pathlib import Path
import json

import requests
import ldap
import ldap.modlist

with (Path(__file__).parent / "config.json").open() as fp:
    config = json.load(fp)

def EV_get_session():
    """
    Return requesets session with presete API token
    """
    session = requests.Session()
    session.headers.update({'Authorization': 'Token '+config['API_TOKEN']})
    return session

def EV_get_all_ppl(session):
    """
    Return list of all easyVerein users

    User dictionaries have __ACTIVE_MEMBER__ attribute, a boolean that is True if
    member status is up-to-date
    """
    # get all ppl (members and non-members) with
    #     name, mail, LDAP_ID, membership status (yes/no)
    req = session.get(config['API_URL'] +
                '?query={id,contactDetails{name,id},emailOrUserName,'
                'customFields{id,customField{id,name},'
                'value},resignationDate,joinDate}')
    res = req.json()

    members = []

    while 'results' in res:
        # For each member:
        for m in res['results']:
            members.append(m)
            active = False  # assume member is not an active member

            # has joined in past?
            try:
                joinDate = datetime.fromisoformat(m['joinDate'])
                if joinDate < datetime.now(tz=joinDate.tzinfo):
                    active = True
            except TypeError:
                pass

            # has left since?
            if active:
                try:
                    resignationDate = datetime.fromisoformat(m['resignationDate'])
                    if resignationDate > joinDate:
                        active = False
                except TypeError:
                    pass
            
            m['__ACTIVE_MEMBER__'] = active

        if res['next']:
            req = requests.get(res['next'], headers={'Authorization': 'Token '+config['API_TOKEN']})
            res = req.json()
            print('.', end='', flush=True)
        else:
            break
    return members

def EV_update_custom_field(session, member_id, custom_field_entry_id, value):
    """Set LDAP ID on member profile."""
    r = session.patch(config['API_URL'] +
                '/{}/custom-fields/{}'.format(
                    member_id, custom_field_entry_id),
                json={'value': value})
    if not r.ok:
        r.raise_for_status()
    return r

def EV_create_custom_field(session, member_id, custom_field_id, value):
    """create custom field on member profile."""
    r = session.post(config['API_URL'] +
                '/{}/custom-fields'.format(member_id),
                json={'customField': custom_field_id,
                      'value': value})
    if not r.ok:
        r.raise_for_status()
    return r

def EV_delete_custom_field(session, member_id, custom_field_entry_id):
    """Set LDAP ID on member profile."""
    r = session.delete(config['API_URL'] +
                '/{}/custom-fields/{}'.format(
                    member_id, custom_field_entry_id))
    if not r.ok:
        r.raise_for_status()
    return r

def LDAP_initialize():
    l = ldap.initialize(config['LDAP_URL'])
    l.simple_bind_s(config['LDAP_USER'], config['LDAP_PASS'])
    return l

def LDAP_get_ppl(ldap_con, print_weirdos=True):
    ldap_ppl = ldap_con.search_s("ou=users,dc=betreiberverein,dc=de",
                                 ldap.SCOPE_ONELEVEL,
                                 "objectclass=inetOrgPerson",
                                 ('mail','entryUUID','uid'))

    if print_weirdos:
        weirdos = [p for p in ldap_ppl if 'mail' not in p[1]]
        if weirdos:
            print("We have weird LDAP accounts without email:")
            pprint(weirdos)
            print("They will be ignored.")
    
    return ldap_ppl

# Get data from LDAP
LDAP_con = LDAP_initialize()
LDAP_ppl = LDAP_get_ppl(LDAP_con)
LDAP_ppl_by_mail = {p[1]['mail'][0].decode().lower(): p for p in LDAP_ppl if 'mail' in p[1]}
LDAP_ppl_by_uuid = {p[1]['entryUUID'][0].decode(): p for p in LDAP_ppl}

print ('LDAP:', len(LDAP_ppl), 'total')

# Get data from easyVerein
EV_session = EV_get_session()
EV_members = EV_get_all_ppl(EV_session)

print('easyVerein:', len(EV_members), 'total   ', len([m for m in EV_members if m['__ACTIVE_MEMBER__']]), 'active')

active_members_with_ldap = []
for m in EV_members:
    customFields = {cf['customField']['id']: cf for cf in m['customFields'] or []}
    LDAP_ID = customFields.get(config['LDAP_ID_CUSTOM_FIELD_ID'], {}).get('value', None)

    print("{:<40}".format(m['emailOrUserName']), end=" - ")

    # If user has an LDAP ID set:
    if LDAP_ID:
        # Validate that user is found in LDAP_ppl, if not delete LDAP_ID from eV
        if LDAP_ID not in LDAP_ppl_by_uuid:
            # remove LDAP_ID entry from user `m` in easyVerein
            EV_delete_custom_field(EV_session, m['id'], config['LDAP_ID_CUSTOM_FIELD_ID'])
            # Unset LDAP_ID to try and match by mail again
            print("no-more-ldap", end=" ")
            LDAP_ID = None
        else:
            # Everything is up-to-date
            print("    has-ldap", end=" ")
            pass

    if not LDAP_ID:  # User has no LDAP ID set
        # search for email in LDAP
        if m['emailOrUserName'].lower() in LDAP_ppl_by_mail:
            # set LDAP_ID in eV profile
            LDAP_ID = LDAP_ppl_by_mail[m['emailOrUserName'].lower()][1]['entryUUID'][0].decode()
            EV_create_custom_field(EV_session, m['id'], config['LDAP_ID_CUSTOM_FIELD_ID'], LDAP_ID)
            print("matched-mail", end=" ")
        else:
            # no matching LDAP account found, ignoring this eV account
            print("     no-ldap", end=" ")
            pass
    m['LDAP_ID'] = LDAP_ID
    
    if m['__ACTIVE_MEMBER__']:
        if LDAP_ID:
            active_members_with_ldap.append(LDAP_ppl_by_uuid[LDAP_ID][0])
        print("  active", end=" ")
    else:
        print("inactive", end=" ")
    print()

# update "Mitglieder" group from active_members_with_ldap:
# remove all non-members, add all new members

ldap_members_group = LDAP_con.search_s(
    "cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
    ldap.SCOPE_BASE,
    "objectclass=groupOfUniqueNames")
ldap_members_group_new = deepcopy(ldap_members_group)
ldap_members_group_new[0][1]['uniqueMember'] = [cn.encode() for cn in active_members_with_ldap]

modlist = ldap.modlist.modifyModlist(ldap_members_group[0][1], ldap_members_group_new[0][1])
LDAP_con.modify_s("cn=mitglied,ou=groups,dc=betreiberverein,dc=de",
           modlist)

# report unmatched
# print("Unmatec LDAP Users:")
# EV_members_by_ldap_id = {m['LDAP_ID'].lower(): m for m in EV_members if m['LDAP_ID']}
# for p in LDAP_ppl:
#     if p[1]['entryUUID'][0].decode() not in EV_members_by_ldap_id:
#         print(p)

# update/sync betreiberverein-mitglieder@ from active_member_list
active_member_mails = [
    '"{}" <{}>'.format(m['contactDetails']['name'], m['emailOrUserName'].lower())
    for m in EV_members if m['__ACTIVE_MEMBER__']]
p = subprocess.run(
    'sync_members -f - betreiberverein-mitglieder'.split(),
    input='\n'.join(active_member_mails).encode())
p.check_returncode()

# TODO enforce sane usernames? Probably better located at self-registration

# TODO use LDAP mail-groups for mailman sync
# TODO add to keycloak self-service