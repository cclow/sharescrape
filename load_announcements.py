#! /usr/bin/env python

import json
from datetime import datetime
from sqlalchemy.sql import exists
import urllib
import logging

from announcement import Announcement
from db import Session

def _to_broadcast_time(str):
    try:
        return datetime.strptime(str, "%m/%d/%Y %I:%M:%S %p")
    except:
        logging.warning("Cannot parse broadcast time '%s'" % str)
        return None

def announcement_from_json(item):
    SGX_KEY_KEY     = "key"
    ISSUER_NAME_KEY = "IssuerName"
    SECURITY_NAME_KEY = "SecurityName"
    GROUP_CODE_KEY  = "GroupCode"
    CATEGORY_CODE_KEY = "CategoryCode"
    CATEGORY_NAME_KEY = "CategoryName"
    TITLE_KEY       = "AnnTitle"
    BROADCAST_TIME_KEY = "BroadcastDateTime"
    SIBLINGS_KEY    = "Siblings"

    try:
        broadcast_time = _to_broadcast_time(item[BROADCAST_TIME_KEY])
        return Announcement(sgx_key=item[SGX_KEY_KEY], broadcast_time=broadcast_time,
                issuer_name=item[ISSUER_NAME_KEY], security_name=item[SECURITY_NAME_KEY],
                group_code=item[GROUP_CODE_KEY], category_code=item[CATEGORY_CODE_KEY],
                category_name=item[CATEGORY_NAME_KEY], title=item[TITLE_KEY],
                siblings=item[SIBLINGS_KEY])
    except:
        logging.warning("Cannot create announcement from %s" % item)
        return None

def load_announcements_from_sgx(n):
    SGX_ANNOUNCEMENTS_URL = 'http://sgx.com/proxy/SgxDominoHttpProxy?timeout=1000&dominoHost=http%3A%2F%2Finfofeed.sgx.com%2FApps%3FA%3DCOW_CorpAnnouncement_Content%26B%3DAnnouncementLast3Months%26R_C%3D%26C_T%3D' + ("%d" % n)
    f = urllib.urlopen(SGX_ANNOUNCEMENTS_URL)
    json_data = f.read()[4:]
    f.close()
    load_announcements(json_data)

def _sgx_key_exists(session, sgx_key):
    return session.query(exists().where(Announcement.sgx_key == sgx_key)).scalar()

def load_announcements(json_data):
    data = json.loads(json_data)

    items = data["items"]
    items.remove({})

    session = Session()
    for item in items:
        announcement = announcement_from_json(item)

        if announcement and not _sgx_key_exists(session, announcement.sgx_key):
            session.add(announcement)
            print "Added %s" % announcement

    session.commit()

if __name__ == "__main__":
    import sys
    try:
        load_announcements_from_sgx(int(sys.argv[1]))
    except IndexError:
        load_announcements_from_sgx(200)
