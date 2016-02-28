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

# TODO: load_announcements_from_sgx to update latest announcements from sgx.com

def load_announcements(json_data):
    data = json.loads(json_data)

    items = data["items"]
    items.remove({})

    session = Session()
    for item in items:
        announcement = announcement_from_json(item)

        if announcement:
            session.add(announcement)
            print "Added %s" % announcement

    session.commit()
