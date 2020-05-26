#!/usr/bin/env python
"""
Example script
"""

from __future__ import print_function
import os
import sys
from pysigsci import sigsciapi
from pysigsci.sigsciapi import parse_time_delta

if "SIGSCI_EMAIL" in os.environ:
    EMAIL = os.environ['SIGSCI_EMAIL']
else:
    print('SIGSCI_EMAIL required.')
    sys.exit()

if "SIGSCI_API_TOKEN" in os.environ:
    API_TOKEN = os.environ['SIGSCI_API_TOKEN']
else:
    print('SIGSCI_API_TOKEN required.')
    sys.exit()


def main():
    """
    Example main function
    """
    # create sigsci api object
    sigsci = sigsciapi.SigSciApi(email=EMAIL, api_token=API_TOKEN)

    if "SIGSCI_CORP" in os.environ:
        sigsci.corp = os.environ['SIGSCI_CORP']
    else:
        print('SIGSCI_CORP required.')
        sys.exit()

    if "SIGSCI_SITE" in os.environ:
        sigsci.site = os.environ['SIGSCI_SITE']
    else:
        print('SIGSCI_SITE required.')
        sys.exit()

    # List corps
    print(sigsci.get_corps())
    # Get corp by name
    print(sigsci.get_corp())
    # Update corp by name
    data = {"displayName": "My Display Name"}
    print(sigsci.update_corp(data))
    # List corp users
    print(sigsci.get_corp_users())
    # List custom alerts
    print(sigsci.get_custom_alerts())
    # List events
    print(sigsci.get_events())
    # List requests
    sigsci.site = "mysite"
    params = {"q": "from:-1d tag:XSS"}
    print(sigsci.get_requests(parameters=params))
    # Get request feed
    sigsci.site = "mysite"
    params = {
        "from": parse_time_delta("-1d"),
        "until": parse_time_delta("-5m"),
        "tags": "xss"
        }
    print(sigsci.get_request_feed(parameters=params))


if __name__ == '__main__':
    main()
