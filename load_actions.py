#! /usr/bin/env python

import json
from datetime import datetime
from sqlalchemy.sql import exists
import urllib
import logging

from action import Action
from db import Session

def _to_date(str):
    try:
        return datetime.strptime(str, "%d %b %Y")
    except:
        return None

def action_from_json(item):

    SGX_KEY_KEY    = "key"
    COMPANY_NAME_KEY = "CompanyName"
    TYPE_KEY       = "Annc_Type"
    EX_DATE_KEY    = "Ex_Date"
    RECORD_DATE_KEY = "Record_Date"
    PAID_DATE_KEY  = "DatePaid_Payable"
    NOTES_KEY      = "Particulars"
    SIBLINGS_KEY   = "Siblings"

    try:
        sgx_key = int(item[SGX_KEY_KEY])
        ex_date = _to_date(item[EX_DATE_KEY])
        record_date = _to_date(item[RECORD_DATE_KEY])
        paid_date = _to_date(item[PAID_DATE_KEY])
        return Action(sgx_key=sgx_key, type=item[TYPE_KEY], 
                company_name=item[COMPANY_NAME_KEY],
                ex_date=ex_date, record_date=record_date,
                paid_date=paid_date, notes=item[NOTES_KEY],
                siblings=item[SIBLINGS_KEY])
    except:
        logging.warning("Cannot create action from %s" % item)
        return None

def load_actions_from_sgx(n):
    SGX_ACTIONS_URL = 'http://sgx.com/proxy/SgxDominoHttpProxy?timeout=1000&dominoHost=http%3A%2F%2Finfofeed.sgx.com%2FApps%3FA%3DCow_CorporateInformation_Content%26B%3DCorpDistributionByExDate%26C_T%3D' + ("%d" % n)
    f = urllib.urlopen(SGX_ACTIONS_URL)
    json_data = f.read()[4:]
    f.close()
    load_actions(json_data)

def _sgx_key_exists(session, sgx_key):
    return session.query(exists().where(Action.sgx_key == sgx_key)).scalar()

def load_actions(json_data):
    data = json.loads(json_data)

    items = data["items"]
    items.remove({})

    session = Session()

    for item in items:
        action = action_from_json(item)

        if action and not _sgx_key_exists(session, action.sgx_key):
            session.add(action)
            print "Added %s" % action

    session.commit()

if __name__ == "__main__":
    import sys
    try:
        load_actions_from_sgx(int(sys.argv[1]))
    except IndexError:
        load_actions_from_sgx(200)
