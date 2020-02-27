"""
Signal Sciences API Client
"""

import requests
import pysigsci


class SigSciApi(object):
    """
    Class for Signal Sciences API
    """
    base_url = "https://dashboard.signalsciences.net/api/"
    api_version = "v0"
    bearer_token = None
    api_user = None
    api_token = None
    cookies = None
    corp = None
    site = None

    # endpoints
    ep_auth = "/auth"
    ep_auth_logout = ep_auth + "/logout"
    ep_corps = "/corps"

    def __init__(self, email=None, password=None, api_token=None):
        """
        sigsciapi
        """
        if email is not None and password is not None:
            self.auth(email, password)
        elif email is not None and api_token is not None:
            self.api_user = email
            self.api_token = api_token


    def _make_request(self,
                      endpoint,
                      params=None,
                      data=None,
                      json=None,
                      method="GET"):
        headers = dict()
        cookies = None

        if endpoint != self.ep_auth and self.bearer_token is not None:
            headers["Authorization"] = "Bearer {}".format(self.bearer_token['token'])
        elif endpoint != self.ep_auth:
            headers["X-Api-User"] = self.api_user
            headers['X-Api-Token'] = self.api_token

        headers["Content-Type"] = "application/json"
        headers['User-Agent'] = 'pysigsci v' + pysigsci.VERSION

        if self.cookies is not None:
            cookies = self.cookies

        url = self.base_url + self.api_version + endpoint

        result = None
        if method == "GET":
            result = requests.get(url, params=params, headers=headers, cookies=cookies)
        elif method == "POST":
            result = requests.post(url, data=data, headers=headers, cookies=cookies)
        elif method == "POST_JSON":
            result = requests.post(url, json=json, headers=headers, cookies=cookies)
        elif method == "PUT":
            result = requests.put(url, json=json, headers=headers, cookies=cookies)
        elif method == "PATCH":
            result = requests.patch(url, json=json, headers=headers, cookies=cookies)
        elif method == "DELETE":
            headers["Content-Type"] = "application/json"
            result = requests.delete(url, params=params, headers=headers, cookies=cookies)
        else:
            raise Exception("InvalidRequestMethod: " + str(method))

        if result.status_code == 204:
            return dict({'message': '{} {}'.format(method, 'successful.')})

        if result.status_code == 400:
            raise Exception('400 Bad Request: {}'.format(result.json()['message']))

        return result.json()

    def auth(self, email, password):
        """
        Log into the API
        https://docs.signalsciences.net/api/#_auth_post
        POST /auth
        """
        data = {"email": email, "password": password}
        self.bearer_token = self._make_request(
            endpoint=self.ep_auth,
            data=data,
            method="POST")
        return True

    # CORPS
    def get_corps(self):
        """
        List corps
        https://docs.signalsciences.net/api/#_corps_get
        GET /corps/
        """
        return self._make_request(endpoint=self.ep_corps)

    def get_corp(self):
        """
        Get corp by name
        https://docs.signalsciences.net/api/#get-corp-by-name
        GET /corps/{corpName}
        """
        return self._make_request("{}/{}".format(self.ep_corps, self.corp))

    def update_corp(self, data):
        """
        Update corp by name
        https://docs.signalsciences.net/api/#update-corp-by-name
        PATCH /corps/{corpName}
        """
        return self._make_request(
            endpoint="{}/{}".format(self.ep_corps, self.corp),
            json=data,
            method="PATCH")

    # CORP USERS
    def get_corp_users(self):
        """
        List users in corp
        https://docs.signalsciences.net/api/#list-users-in-corp
        GET /corps/{corpName}/users
        """
        return self._make_request(
            endpoint="{}/{}/users".format(self.ep_corps, self.corp))

    def get_corp_user(self, email):
        """
        Get corp user by email
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__get
        GET /corps/{corpName}/users/{userEmail}
        """
        return self._make_request(
            endpoint="{}/{}/users/{}".format(self.ep_corps, self.corp, email))

    def delete_corp_user(self, email):
        """
        Delete user from corp
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__delete
        DELETE /corps/{corpName}/users/{userEmail}
        """
        return self._make_request(
            endpoint="{}/{}/users/{}".format(self.ep_corps, self.corp, email),
            method="DELETE")

    def add_corp_user(self, email, data):
        """
        Invite user to corp
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__invite_post
        POST /corps/{corpName}/users/{userEmail}/invite
        """
        return self._make_request(
            endpoint="{}/{}/users/{}/invite".format(
                self.ep_corps, self.corp, email),
            json=data,
            method="POST_JSON")

    def update_corp_user(self, email, data):
        """
        Update corp user by email
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__patch
        PATCH /corps/{corpName}/users/{userEmail}
        """
        return self._make_request(
            endpoint="{}/{}/users/{}".format(self.ep_corps,
                                             self.corp,
                                             email),
            json=data,
            method="PATCH")

    # OVERVIEW REPORT
    def get_overview_report(self, parameters=dict()):
        """
        Get overview report data
        https://docs.signalsciences.net/api/#_corps__corpName__reports_attacks_get
        GET /corps/{corpName}/reports/attacks
        """
        return self._make_request(
            endpoint="{}/{}/reports/attacks".format(self.ep_corps, self.corp),
            params=parameters)

    # SITES
    def get_corp_sites(self):
        """
        List sites in corp
        https://docs.signalsciences.net/api/#_corps__corpName__sites_get
        GET /corps/{corpName}/sites
        """
        return self._make_request(
            endpoint="{}/{}/sites".format(self.ep_corps, self.corp))

    def get_corp_site(self, site_name):
        """
        Get site by name
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__get
        GET /corps/{corpName}/sites/{siteName}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}".format(self.ep_corps,
                                             self.corp,
                                             site_name))

    def update_corp_site(self, data):
        """
        Update a site by name
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__patch
        PATCH /corps/{corpName}/sites/{siteName}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}".format(self.ep_corps,
                                             self.corp,
                                             self.site),
            json=data,
            method="PATCH")

    def create_corp_site(self, data):
        """
        Create site in corp
        https://docs.signalsciences.net/api/#_corps__corpName__sites_post
        POST /corps/{corpName}/sites
        """
        return self._make_request(
            endpoint="{}/{}/sites".format(self.ep_corps,
                                          self.corp),
            json=data,
            method="POST_JSON")

    # CORP/SITE SIGNALS (TAGS)
    def get_custom_signals(self):
        """
        Get Custom Signals - Here for backwards compatability
        """
        return self.get_site_signals()

    def add_custom_signals(self, data):
        """
        Add custom signal - Here for backwards compatability
        """
        return self.add_site_signals(data)

    def delete_custom_signal(self, identifier):
        """
        Delete Custom Signals - Here for backwards compatability
        """
        return self.delete_site_signal(identifier)

    def get_site_signals(self):
        """
        Get Site Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags".format(self.ep_corps,
                                                  self.corp,
                                                  self.site))

    def add_site_signals(self, data):
        """
        Add custom signal
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        POST /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags".format(
                self.ep_corps, self.corp, self.site),
            json=data,
            method="POST_JSON")

    def delete_site_signal(self, identifier):
        """
        Delete Custom Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/tags/{}".format(self.ep_corps,
                                                     self.corp,
                                                     self.site,
                                                     identifier),
            method="DELETE")

    def get_corp_signals(self):
        """
        Get Corp Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/tags".format(self.ep_corps,
                                         self.corp))

    def add_corp_signals(self, data):
        """
        Add Corp Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/tags
        """
        return self._make_request(
            endpoint="{}/{}//tags".format(
                self.ep_corps, self.corp),
            json=data,
            method="POST_JSON")

    def delete_corp_signals(self, identifier):
        """
        Delete Corp Signals
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/tags
        """
        return self._make_request(
            endpoint="{}/{}/tags/{}".format(self.ep_corps,
                                            self.corp,
                                            identifier),
            method="DELETE")

    # CUSTOM ALERTS
    def get_custom_alerts(self):
        """
        List custom alerts
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_get
        GET /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts".format(self.ep_corps,
                                                    self.corp,
                                                    self.site))

    def get_custom_alert(self, identifier):
        """
        Get custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__get
        GET /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts/{}".format(self.ep_corps,
                                                       self.corp,
                                                       self.site,
                                                       identifier))

    def add_custom_alert(self, data):
        """
        Create custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_post
        POST /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts".format(
                self.ep_corps, self.corp, self.site),
            json=data,
            method="POST_JSON")

    def update_custom_alert(self, identifier, data):
        """
        Update custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__patch
        PATCH /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts/{}".format(self.ep_corps,
                                                       self.corp,
                                                       self.site,
                                                       identifier),
            json=data,
            method="PATCH")

    def delete_custom_alert(self, identifier):
        """
        Delete alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__delete
        DELETE /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/alerts/{}".format(self.ep_corps,
                                                       self.corp,
                                                       self.site,
                                                       identifier),
            method="DELETE")

    # EVENTS
    def get_events(self, parameters=dict()):
        """
        List events
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__events_get
        GET /corps/{corpName}/sites/{siteName}/events
        """

        return self._make_request(
            endpoint="{}/{}/sites/{}/events".format(self.ep_corps,
                                                    self.corp,
                                                    self.site),
            params=parameters)

    def get_event(self, identifier):
        """
        Get event by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__events__eventID__get
        GET /corps/{corpName}/sites/{siteName}/events/{eventID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/events/{}".format(self.ep_corps,
                                                       self.corp,
                                                       self.site,
                                                       identifier))

    def expire_event(self, event_id):
        """
        Expire an event by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__events__eventID__expire_post
        POST /corps/{corpName}/sites/{siteName}/events/{eventID}/expire
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/events/{}/expire".format(self.ep_corps,
                                                              self.corp,
                                                              self.site,
                                                              event_id),
            method="POST")

    # REQUESTS
    def get_requests(self, parameters=dict()):
        """
        Search requests
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__requests_get
        GET /corps/{corpName}/sites/{siteName}/requests
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/requests".format(self.ep_corps,
                                                      self.corp,
                                                      self.site),
            params=parameters)

    def get_request(self, identifier):
        """
        Get request by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__requests__requestID__get
        GET /corps/{corpName}/sites/{siteName}/requests/{requestID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/requests/{}".format(self.ep_corps,
                                                         self.corp,
                                                         self.site,
                                                         identifier))

    def get_request_feed(self, parameters=dict()):
        """
        Get request feed
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__feed_requests_get
        GET /corps/{corpName}/sites/{siteName}/feed/requests
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/feed/requests".format(
                self.ep_corps, self.corp, self.site),
            params=parameters)

    # WHITELISTS
    def get_whitelist(self):
        """
        Get whitelist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__whitelist_get
        GET /corps/{corpName}/sites/{siteName}/whitelist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/whitelist".format(self.ep_corps,
                                                       self.corp,
                                                       self.site))

    def add_whitelist(self, data):
        """
        Add to whitelist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__whitelist_put
        PUT /corps/{corpName}/sites/{siteName}/whitelist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/whitelist".format(self.ep_corps,
                                                       self.corp,
                                                       self.site),
            json=data,
            method="PUT")

    def delete_whitelist(self, identifier):
        """
        Delete from whitelist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__whitelist__id__delete
        DELETE /corps/{corpName}/sites/{siteName}/whitelist/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/whitelist/{}".format(
                self.ep_corps, self.corp, self.site, identifier),
            method="DELETE")

    # BLACKLISTS
    def get_blacklist(self):
        """
        Get blacklist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__blacklist_get
        GET /corps/{corpName}/sites/{siteName}/blacklist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/blacklist".format(self.ep_corps,
                                                       self.corp,
                                                       self.site))

    def add_blacklist(self, data):
        """
        Add to blacklist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__blacklist_put
        PUT /corps/{corpName}/sites/{siteName}/blacklist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/blacklist".format(self.ep_corps,
                                                       self.corp, self.site),
            json=data,
            method="PUT")

    def delete_blacklist(self, identifier):
        """
        Delete from blacklist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__blacklist__id__delete
        DELETE /corps/{corpName}/sites/{siteName}/blacklist/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/blacklist/{}".format(
                self.ep_corps, self.corp, self.site, identifier),
            method="DELETE")

    # RULES
    def get_request_rules(self):
        """
        Get Request Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/requestRules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/requestRules".format(self.ep_corps,
                                                          self.corp,
                                                          self.site))

    def add_request_rules(self, data):
        """
        Add Request Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/requestRules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/requestRules".format(self.ep_corps,
                                                          self.corp,
                                                          self.site),
            json=data,
            method="POST_JSON")

    def delete_request_rule(self, identifier):
        """
        Delete Request Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/rules/{ID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/rule/{}".format(self.ep_corps,
                                                     self.corp,
                                                     self.site,
                                                     identifier),
            method="DELETE")

    def get_signal_rules(self):
        """
        Get Signal Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/signalRules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/signalRules".format(self.ep_corps,
                                                         self.corp,
                                                         self.site))

    def add_signal_rules(self, data):
        """
        Add Signal Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/signalRules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/signalRules".format(self.ep_corps,
                                                         self.corp,
                                                         self.site),
            json=data,
            method="POST_JSON")

    def get_templated_rule(self, identifier):
        """
        Get Templated Rule
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates/{}".format(self.ep_corps,
                                                                    self.corp,
                                                                    self.site,
                                                                    identifier))

    def get_templated_rules(self):
        """
        Get Templated Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates".format(self.ep_corps,
                                                                 self.corp,
                                                                 self.site))

    def add_templated_rules(self, identifier, data):
        """
        Add Templated Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates/{name}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates/{}".format(self.ep_corps,
                                                                    self.corp,
                                                                    self.site,
                                                                    identifier),
            json=data,
            method="POST_JSON")

    def delete_templated_rule(self, identifier):
        """
        Add Templated Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates/{name}
        """
        data = {
            "alertAdds": [],
            "alertDeletes": [],
            "alertUpdates": [],
            "detectionAdds": [],
            "detectionDeletes": [],
            "detectionUpdates": []
        }
        templated_rule = self.get_templated_rule(identifier)

        data['alertDeletes'] = templated_rule['alerts']
        data['detectionDeletes'] = templated_rule['detections']

        return self._make_request(
            endpoint="{}/{}/sites/{}/configuredtemplates/{}".format(self.ep_corps,
                                                                    self.corp,
                                                                    self.site,
                                                                    identifier),
            json=data,
            method="POST_JSON")

    def get_advanced_rules(self):
        """
        Get Advanced Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/advancedRules
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/advancedRules".format(self.ep_corps,
                                                           self.corp,
                                                           self.site))

    def add_advanced_rules(self, data):
        """
        Add Advanced Rules
        WARNING: This is an undocumented endpoint. No support provided, and the
        endpoint may change.
        /corps/{corpName}/sites/{siteName}/configuredtemplates/{name}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/advancedRules".format(self.ep_corps,
                                                           self.corp,
                                                           self.site),
            json=data,
            method="POST_JSON")

    # CORP/SITE LISTS
    def get_rule_lists(self):
        """
        Get site lists - Here for backwards compatability
        """
        return self.get_site_rule_lists()

    def get_site_rule_lists(self):
        """
        Get Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists_get
        GET /corps/{corpName}/sites/{siteName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists".format(self.ep_corps,
                                                   self.corp,
                                                   self.site))

    def add_rule_lists(self, data):
        """
        Add a site list - Here for backwards compatability
        """
        return self.add_site_rule_lists(data)

    def add_site_rule_lists(self, data):
        """
        Add Site Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists_post
        POST /corps/{corpName}/sites/{siteName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists".format(self.ep_corps,
                                                   self.corp,
                                                   self.site),
            json=data,
            method="POST_JSON")

    def update_rule_lists(self, identifier, data):
        """
        Update a site list - Here for backwards compatability
        """
        return self.update_site_rule_lists(identifier, data)

    def update_site_rule_lists(self, identifier, data):
        """
        Update a site list by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists__id__patch
        PATCH /corps/{corpName}/sites/{siteName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists/{}".format(
                self.ep_corps, self.corp, self.site, identifier),
            json=data,
            method="PATCH")

    def delete_rule_lists(self, identifier):
        """
        Delete site list - Here for backwards compatability
        """
        return self.delete_site_rule_lists(identifier)

    def delete_site_rule_lists(self, identifier):
        """
        Delete a site list by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__lists__id__delete
        DELETE /corps/{corpName}/sites/{siteName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/lists/{}".format(self.ep_corps,
                                                      self.corp,
                                                      self.site,
                                                      identifier),
            method="DELETE")

    def get_corp_rule_lists(self):
        """
        Get Corp Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__lists_get
        GET /corps/{corpName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/lists".format(self.ep_corps,
                                          self.corp))

    def add_corp_rule_lists(self, data):
        """
        Add Corp Rule Lists
        https://docs.signalsciences.net/api/#_corps__corpName__lists_post
        POST /corps/{corpName}/lists
        """
        return self._make_request(
            endpoint="{}/{}/lists".format(self.ep_corps,
                                          self.corp),
            json=data,
            method="POST_JSON")

    def update_corp_rule_lists(self, identifier, data):
        """
        Update a corp list by ID
        https://docs.signalsciences.net/api/#_corps__corpName__lists__id__patch
        PATCH /corps/{corpName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/lists/{}".format(
                self.ep_corps, self.corp, identifier),
            json=data,
            method="PATCH")

    def delete_corp_rule_lists(self, identifier):
        """
        Delete a corp list by ID
        https://docs.signalsciences.net/api/#_corps__corpName__lists__id__delete
        DELETE /corps/{corpName}/lists/{id}
        """
        return self._make_request(
            endpoint="{}/{}/lists/{}".format(self.ep_corps,
                                             self.corp,
                                             identifier),
            method="DELETE")

    # PRIVACY REDACTIONS
    def get_redactions(self):
        """
        List redactions
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__redactions_get
        GET /corps/{corpName}/sites/{siteName}/redactions
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/redactions".format(self.ep_corps,
                                                        self.corp,
                                                        self.site))

    def add_redactions(self, data):
        """
        Add to redactions
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__redactions_put
        POST /corps/{corpName}/sites/{siteName}/redactions
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/redactions".format(self.ep_corps,
                                                        self.corp,
                                                        self.site),
            json=data,
            method="POST_JSON")

    def delete_redactions(self, field):
        """
        Delete from redactions
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__redactions__id__delete
        DELETE /corps/{corpName}/sites/{siteName}/redactions/{field}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/redactions/{}".format(
                self.ep_corps, self.corp, self.site, field),
            method="DELETE")

    # INTEGRATIONS
    def get_integrations(self):
        """
        List integrations
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations_get
        GET /corps/{corpName}/sites/{siteName}/integrations
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations".format(self.ep_corps,
                                                          self.corp,
                                                          self.site))

    def add_integration(self, data):
        """
        Add to integrations
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations_post
        POST /corps/{corpName}/sites/{siteName}/integrations
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations".format(
                self.ep_corps, self.corp, self.site),
            json=data,
            method="POST_JSON")

    def get_integration(self, identifier):
        """
        Get integration by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations__integrationID__get
        GET /corps/{corpName}/sites/{siteName}/integrations/{integrationID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations/{}".format(self.ep_corps,
                                                             self.corp,
                                                             self.site,
                                                             identifier))

    def update_integration(self, identifier, data):
        """
        Update an integration by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations__integrationID__patch
        PATCH /corps/{corpName}/sites/{siteName}/integrations/{integrationID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations/{}".format(
                self.ep_corps, self.corp, self.site, identifier),
            json=data,
            method="PATCH")

    def delete_integration(self, identifier):
        """
        Delete from integrations
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations__integrationID__delete
        DELETE /corps/{corpName}/sites/{siteName}/integrations/{integrationID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/integrations/{}".format(self.ep_corps,
                                                             self.corp, self.site, identifier),
            method="DELETE")

    # PARAMETER WHITELIST
    def get_parameter_whitelist(self):
        """
        List whitelisted parameters
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__paramwhitelist_get
        GET /corps/{corpName}/sites/{siteName}/paramwhitelist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/paramwhitelist".format(self.ep_corps,
                                                            self.corp,
                                                            self.site))

    # PATH WHITELIST
    def get_path_whitelist(self):
        """
        List whitelisted paths
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__pathwhitelist_get
        GET /corps/{corpName}/sites/{siteName}/pathwhitelist
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/pathwhitelist".format(self.ep_corps,
                                                           self.corp,
                                                           self.site))

    # ACTIVITY
    def get_activity(self):
        """
        List activity events
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__analytics_events_get
        GET /corps/{corpName}/sites/{siteName}/analytics/events
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/analytics/events".format(self.ep_corps,
                                                              self.corp,
                                                              self.site))

    # HEADER LINKS
    def get_header_links(self):
        """
        List header links
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__headerLinks_get
        GET /corps/{corpName}/sites/{siteName}/headerLinks
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/headerLinks".format(self.ep_corps,
                                                         self.corp,
                                                         self.site))

    def add_header_links(self, data):
        """
        Add to header links
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__headerLinks_post
        POST /corps/{corpName}/sites/{siteName}/headerLinks
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/headerLinks".format(
                self.ep_corps, self.corp, self.site),
            json=data,
            method="POST_JSON")

    def get_header_link(self, identifier):
        """
        Get header link by ID
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__headerLinks__headerLinkID__get
        GET /corps/{corpName}/sites/{siteName}/headerLinks/{headerLinkID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/headerLinks/{}".format(self.ep_corps,
                                                            self.corp,
                                                            self.site,
                                                            identifier))

    def delete_header_links(self, identifier):
        """
        Delete from header links
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__headerLinks__headerLinkID__delete
        DELETE /corps/{corpName}/sites/{siteName}/headerLinks/{headerLinkID}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/headerLinks/{}".format(
                self.ep_corps, self.corp, self.site, identifier),
            method="DELETE")

    # SITE MEMBERS
    def get_site_members(self):
        """
        List site members
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members_get
        GET /corps/{corpName}/sites/{siteName}/members
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members".format(self.ep_corps,
                                                     self.corp,
                                                     self.site))

    def get_site_member(self, email):
        """
        Get site member by email
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members__siteMemberEmail__get
        GET /corps/{corpName}/sites/{siteName}/members/{siteMemberEmail}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members/{}".format(self.ep_corps,
                                                        self.corp,
                                                        self.site,
                                                        email))

    def get_memberships(self, email):
        """
        Get memberships by email
        GET /corps/{corpName}/users/{siteMemberEmail}/memberships
        """
        return self._make_request(
            endpoint="{}/{}/users/{}/memberships".format(self.ep_corps,
                                                         self.corp,
                                                         email))

    def delete_site_member(self, email):
        """
        Delete from site members
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members__siteMemberEmail__delete
        DELETE /corps/{corpName}/sites/{siteName}/members/{siteMemberEmail}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members/{}".format(
                self.ep_corps, self.corp, self.site, email),
            method="DELETE")

    def add_site_member(self, email, data):
        """
        Invite a site member
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members__siteMemberEmail__invite_post
        POST /corps/{corpName}/sites/{siteName}/members/{siteMemberEmail}/invite
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/members/{}/invite".format(self.ep_corps,
                                                               self.corp,
                                                               self.site,
                                                               email),
            json=data,
            method="POST_JSON")

    # SITE MONITOR
    def get_site_monitor(self):
        """
        Get site monitor
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__monitors_get
        GET /corps/{corpName}/sites/{siteName}/monitors
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/monitors".format(self.ep_corps,
                                                      self.corp,
                                                      self.site))

    def generate_site_monitor_url(self):
        """
        Generate site monitor URL
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__monitors_post
        POST /corps/{corpName}/sites/{siteName}/monitors
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/monitors".format(
                self.ep_corps, self.corp, self.site),
            method="POST")

    def enable_site_monitor(self):
        """
        Enable site monitor
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__monitors_enable_post
        POST /corps/{corpName}/sites/{siteName}/monitors/enable
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/monitors/enable".format(
                self.ep_corps, self.corp, self.site),
            method="POST")

    def disable_site_monitor(self):
        """
        Disable site monitor
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__monitors_disable_post
        POST /corps/{corpName}/sites/{siteName}/monitors/disable
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/monitors/disable".format(
                self.ep_corps, self.corp, self.site),
            method="POST")

    # AGENTS
    def get_agents(self):
        """
        List agents
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__agents_get
        GET /corps/{corpName}/sites/{siteName}/agents
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/agents".format(self.ep_corps,
                                                    self.corp,
                                                    self.site))

    def get_agent(self, identifier):
        """
        Agent Details
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__agents__agentName__get
        GET /corps/{corpName}/sites/{siteName}/agents/{agentName}
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/agents/{}".format(self.ep_corps,
                                                       self.corp,
                                                       self.site,
                                                       identifier))

    def get_agent_logs(self, identifier):
        """
        Get agent logs by agent name
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__agents__agentName__logs_get
        GET /corps/{corpName}/sites/{siteName}/agents/{agentName}/logs
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/agents/{}/logs".format(self.ep_corps,
                                                            self.corp,
                                                            self.site,
                                                            identifier))

    def enable_agent_alerts(self, identifier=None):
        """
        Uses: List custom alerts & Update custom alerts
        Alert names:
        - requests_total - The average RPS across all agents is less than 10
        - agent_scoreboards - The site's Online Agent count is zero
        """
        alerts = self.get_custom_alerts()['data']
        responses = []
        agent_alert_tagnames = ['requests_total', 'agent_scoreboards']

        if identifier is not None and identifier in agent_alert_tagnames:
            agent_alert_tagnames = [identifier]

        for alert in alerts:
            if alert['tagName'] in agent_alert_tagnames:
                alert['enabled'] = True
                identifier = alert['id']
                responses.append(self.update_custom_alert(identifier, alert))

        return responses

    def enable_agent_alerts_all_sites(self, identifier=None):
        """
        Uses: Get corp sites, List custom alerts, & Update custom alerts
        Alert names:
        - requests_total - The average RPS across all agents is less than 10
        - agent_scoreboards - The site's Online Agent count is zero
        """
        sites = self.get_corp_sites()['data']
        response = []
        agent_alert_tagnames = ['requests_total', 'agent_scoreboards']

        if identifier is not None and identifier in agent_alert_tagnames:
            agent_alert_tagnames = [identifier]

        for site in sites:
            self.site = site['name']
            alerts = self.get_custom_alerts()['data']

            for alert in alerts:
                if alert['tagName'] in agent_alert_tagnames:
                    alert['enabled'] = True
                    identifier = alert['id']
                    response.append(
                        self.update_custom_alert(
                            identifier, alert))

        return response

    def disable_agent_alerts(self, identifier=None):
        """
        Uses: List custom alerts & Update custom alerts
        Alert names:
        - requests_total - The average RPS across all agents is less than 10
        - agent_scoreboards - The site's Online Agent count is zero
        """
        alerts = self.get_custom_alerts()['data']
        responses = []
        agent_alert_tagnames = ['requests_total', 'agent_scoreboards']

        if identifier is not None and identifier in agent_alert_tagnames:
            agent_alert_tagnames = [identifier]

        for alert in alerts:
            if alert['tagName'] in agent_alert_tagnames:
                alert['enabled'] = False
                identifier = alert['id']
                responses.append(self.update_custom_alert(identifier, alert))

        return responses

    def disable_agent_alerts_all_sites(self, identifier=None):
        """
        Uses: Get corp sites, List custom alerts, & Update custom alerts
        Alert names:
        - requests_total - The average RPS across all agents is less than 10
        - agent_scoreboards - The site's Online Agent count is zero
        """
        sites = self.get_corp_sites()['data']
        responses = []
        agent_alert_tagnames = ['requests_total', 'agent_scoreboards']

        if identifier is not None and identifier in agent_alert_tagnames:
            agent_alert_tagnames = [identifier]

        for site in sites:
            self.site = site['name']
            alerts = self.get_custom_alerts()['data']

            for alert in alerts:
                if alert['tagName'] in agent_alert_tagnames:
                    alert['enabled'] = False
                    identifier = alert['id']
                    responses.append(
                        self.update_custom_alert(
                            identifier, alert))

        return responses

    # SUSPICIOUS IPS
    def get_suspicious_ips(self):
        """
        List suspicious IPs
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__suspiciousIPs_get
        GET /corps/{corpName}/sites/{siteName}/suspiciousIPs
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/suspiciousIPs".format(self.ep_corps,
                                                           self.corp,
                                                           self.site))

    # TOP ATTACKS
    def get_top_attacks(self):
        """
        List top attacks
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__top_attacks_get
        GET /corps/{corpName}/sites/{siteName}/top/attacks
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/top/attacks".format(self.ep_corps,
                                                         self.corp,
                                                         self.site))

    # TIMESERIES
    def get_timeseries_requests(self, parameters=dict()):
        """
        Get timeseries request info
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__timeseries_requests_get
        GET /corps/{corpName}/sites/{siteName}/timeseries/requests
        """
        return self._make_request(
            endpoint="{}/{}/sites/{}/timeseries/requests".format(self.ep_corps,
                                                                 self.corp,
                                                                 self.site),
            params=parameters)
