#!/usr/bin/env python
"""
Example script
"""

from __future__ import print_function
import os
import sys
from pysigsci import sigsciapi

if "SIGSCI_EMAIL" in os.environ:
    EMAIL = os.environ['SIGSCI_EMAIL']
else:
    print('SIGSCI_EMAIL required.')
    sys.exit()

if "SIGSCI_PASSWORD" in os.environ:
    PASSWORD = os.environ['SIGSCI_PASSWORD']
else:
    print('SIGSCI_PASSWORD required.')
    sys.exit()


def main():
    """
    Example main function
    """
    # create sigsci api object
    sigsci = sigsciapi.SigSciApi()

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

    if sigsci.auth(EMAIL, PASSWORD):
        print(sigsci.bearer_token)

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
        params = {"from": "-1d", "tags": "xss"}
        print(sigsci.get_request_feed(parameters=params))


if __name__ == '__main__':
    main()
