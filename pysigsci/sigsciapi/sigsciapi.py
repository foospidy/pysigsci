"""
Signal Sciences API Client
"""

import requests


class SigSciApi(object):
    """
    Class for Signal Sciences API
    """
    base_url = "https://dashboard.signalsciences.net/api/"
    api_version = "v0"
    token = None
    corp = None
    site = None

    # endpoints
    ep_auth = "/auth"
    ep_auth_logout = ep_auth + "/logout"
    ep_corps = "/corps"

    def __init__(self, email=None, password=None):
        """
        sigsciapi
        """
        if email is not None:
            self.auth(email, password)

    def _make_request(self, endpoint, options=dict(), method="GET"):
        data = dict()
        headers = dict()

        if endpoint != self.ep_auth:
            headers["Authorization"] = "Bearer {}".format(self.token['token'])
            headers["Content-Type"] = "application/json"

        # Add any passed in options to the data dictionary to be included
        # in the web request.
        for key in options:
            data[key] = options[key]

        url = self.base_url + self.api_version + endpoint

        result = None
        if method == "GET":
            result = requests.get(url, params=data, headers=headers)
        elif method == "POST":
            result = requests.post(url, data=data, headers=headers)
        elif method == "POST_JSON":
            result = requests.post(url, json=data, headers=headers)
        elif method == "PATCH":
            result = requests.post(url, json=data, headers=headers)
        elif method == "DELETE":
            result = requests.delete(url, params=data, headers=headers)
        else:
            raise Exception("InvalidRequestMethod: " + str(method))

        return result.json()

    def auth(self, email, password):
        """
        Log into the API
        https://docs.signalsciences.net/api/#_auth_post
        POST /auth
        """
        options = {"email": email, "password": password}
        self.token = self._make_request(self.ep_auth, options, "POST")
        return True

    # CORPS
    def get_corps(self):
        """
        List corps
        https://docs.signalsciences.net/api/#_corps_get
        GET /corps/
        """
        return self._make_request(self.ep_corps)

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
            "{}/{}".format(self.ep_corps, self.corp), data, "PATCH")

    # CORP USERS
    def get_corp_users(self):
        """
        List users in corp
        https://docs.signalsciences.net/api/#list-users-in-corp
        GET /corps/{corpName}/users
        """
        return self._make_request(
            "{}/{}/users".format(self.ep_corps, self.corp))

    def get_corp_user(self, email):
        """
        Get corp user by email
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__get
        GET /corps/{corpName}/users/{userEmail}
        """
        return self._make_request(
            "{}/{}/users/{}".format(self.ep_corps, self.corp, email))

    def delete_corp_user(self, email):
        """
        Delete user from corp
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__delete
        DELETE /corps/{corpName}/users/{userEmail}
        """
        return self._make_request(
            "{}/{}/users/{}".format(self.ep_corps, self.corp, email), method="DELETE")

    def invite_corp_user(self, email, data):
        """
        Invite user to corp
        https://docs.signalsciences.net/api/#_corps__corpName__users__userEmail__invite_post
        POST /corps/{corpName}/users/{userEmail}/invite
        """
        return self._make_request(
            "{}/{}/users/{}/invite".format(self.ep_corps, self.corp, email),
            data,
            method="POST_JSON")

    # OVERVIEW REPORT
    def get_overview_report(self, parameters=dict()):
        """
        Get overview report data
        https://docs.signalsciences.net/api/#_corps__corpName__reports_attacks_get
        GET /corps/{corpName}/reports/attacks
        """
        return self._make_request(
            "{}/{}/reports/attacks".format(self.ep_corps, self.corp),
            options=parameters)

    # SITES
    def get_corp_sites(self):
        """
        List sites in corp
        https://docs.signalsciences.net/api/#_corps__corpName__sites_get
        GET /corps/{corpName}/sites
        """
        return self._make_request(
            "{}/{}/sites".format(self.ep_corps, self.corp))

    def get_corp_site(self, site_name):
        """
        Get site by name
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__get
        GET /corps/{corpName}/sites/{siteName}
        """
        return self._make_request(
            "{}/{}/sites/{}".format(self.ep_corps, self.corp, site_name))

    def update_site(self, data):
        """
        Update a site by name
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__patch
        PATCH /corps/{corpName}/sites/{siteName}
        """
        return self._make_request(
            "{}/{}/sites/{}".format(self.ep_corps, self.corp, self.site), data, "PATCH")

    # CUSTOM ALERTS
    def get_custom_alerts(self):
        """
        List custom alerts
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_get
        GET /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            "{}/{}/sites/{}/alerts".format(self.ep_corps, self.corp, self.site))

    def create_custom_alert(self, data):
        """
        Create custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts_post
        POST /corps/{corpName}/sites/{siteName}/alerts
        """
        return self._make_request(
            "{}/{}/sites/{}/alerts".format(self.ep_corps, self.corp, self.site),
            options=data,
            method="POST_JSON")

    def get_custom_alert(self, alert_id):
        """
        Get custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__get
        GET /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            "{}/{}/sites/{}/alerts/{}".format(self.ep_corps, self.corp, self.site, alert_id))

    def update_custom_alert(self, alertid, data):
        """
        Update custom alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__patch
        PATCH /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            "{}/{}/sites/{}/alerts/{}".format(self.ep_corps, self.corp, self.site, alertid),
            options=data,
            method="PATCH")

    def delete_custom_alert(self, alertid):
        """
        Delete alert
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__alerts__alertID__delete
        DELETE /corps/{corpName}/sites/{siteName}/alerts/{alertID}
        """
        return self._make_request(
            "{}/{}/sites/{}/alerts/{}".format(self.ep_corps, self.corp, self.site, alertid),
            method="DELETE")

    # EVENTS
    def get_events(self):
        """
        List events
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__events_get
        GET /corps/{corpName}/sites/{siteName}/events
        """
        return self._make_request(
            "{}/{}/sites/{}/events".format(self.ep_corps, self.corp, self.site))

    # REQUESTS
    def get_requests(self, parameters=dict()):
        """
        Search requests
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__requests_get
        GET /corps/{corpName}/sites/{siteName}/requests
        """
        return self._make_request(
            "{}/{}/sites/{}/requests".format(self.ep_corps, self.corp, self.site),
            options=parameters)

    def get_request_feed(self, parameters=dict()):
        """
        Get request feed
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__feed_requests_get
        GET /corps/{corpName}/sites/{siteName}/feed/requests
        """
        return self._make_request("{}/{}/sites/{}/feed/requests".format(
            self.ep_corps, self.corp, self.site), options=parameters)

    # WHITELISTS
    def get_whitelists(self):
        """
        Get whitelist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__whitelist_get
        GET /corps/{corpName}/sites/{siteName}/whitelist
        """
        return self._make_request(
            "{}/{}/sites/{}/whitelist".format(self.ep_corps, self.corp, self.site))

    # BLACKLISTS
    def get_blacklists(self):
        """
        Get blacklist
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__blacklist_get
        GET /corps/{corpName}/sites/{siteName}/blacklist
        """
        return self._make_request(
            "{}/{}/sites/{}/blacklist".format(self.ep_corps, self.corp, self.site))

    # PRIVACY REDACTIONS
    def get_redactions(self):
        """
        List redactions
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__redactions_get
        GET /corps/{corpName}/sites/{siteName}/redactions
        """
        return self._make_request(
            "{}/{}/sites/{}/redactions".format(self.ep_corps, self.corp, self.site))

    # INTEGRATIONS
    def get_integrations(self):
        """
        List integrations
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__integrations_get
        GET /corps/{corpName}/sites/{siteName}/integrations
        """
        return self._make_request(
            "{}/{}/sites/{}/integrations".format(self.ep_corps, self.corp, self.site))

    # PARAMETER WHITELIST
    def get_parameter_whitelist(self):
        """
        List whitelisted parameters
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__paramwhitelist_get
        GET /corps/{corpName}/sites/{siteName}/paramwhitelist
        """
        return self._make_request(
            "{}/{}/sites/{}/paramwhitelist".format(self.ep_corps, self.corp, self.site))

    # PATH WHITELIST
    def get_path_whitelist(self):
        """
        List whitelisted paths
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__pathwhitelist_get
        GET /corps/{corpName}/sites/{siteName}/pathwhitelist
        """
        return self._make_request(
            "{}/{}/sites/{}/pathwhitelist".format(self.ep_corps, self.corp, self.site))

    # ACTIVITY
    def get_activity(self):
        """
        List activity events
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__analytics_events_get
        GET /corps/{corpName}/sites/{siteName}/analytics/events
        """
        return self._make_request(
            "{}/{}/sites/{}/analytics/events".format(self.ep_corps, self.corp, self.site))

    # HEADER LINKS
    def get_header_links(self):
        """
        List header links
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__headerLinks_get
        GET /corps/{corpName}/sites/{siteName}/headerLinks
        """
        return self._make_request(
            "{}/{}/sites/{}/headerLinks".format(self.ep_corps, self.corp, self.site))

    # SITE MEMBERS
    def get_site_members(self):
        """
        List site members
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__members_get
        GET /corps/{corpName}/sites/{siteName}/members
        """
        return self._make_request(
            "{}/{}/sites/{}/members".format(self.ep_corps, self.corp, self.site))

    # SITE MONITOR
    def get_site_monitor(self):
        """
        Get site monitor
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__monitors_get
        GET /corps/{corpName}/sites/{siteName}/monitors
        """
        return self._make_request(
            "{}/{}/sites/{}/monitors".format(self.ep_corps, self.corp, self.site))

    # AGENTS
    def get_agents(self):
        """
        List agents
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__agents_get
        GET /corps/{corpName}/sites/{siteName}/agents
        """
        return self._make_request(
            "{}/{}/sites/{}/agents".format(self.ep_corps, self.corp, self.site))

    # SUSPICIOUS IPS
    def get_suspicious_ips(self):
        """
        List suspicious IPs
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__suspiciousIPs_get
        GET /corps/{corpName}/sites/{siteName}/suspiciousIPs
        """
        return self._make_request(
            "{}/{}/sites/{}/suspiciousIPs".format(self.ep_corps, self.corp, self.site))

    # TOP ATTACKS
    def get_top_attacks(self):
        """
        List top attacks
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__top_attacks_get
        GET /corps/{corpName}/sites/{siteName}/top/attacks
        """
        return self._make_request(
            "{}/{}/sites/{}/top/attacks".format(self.ep_corps, self.corp, self.site))

    # TIMESERIES
    def get_timeseries_requests(self, parameters=dict()):
        """
        Get timeseries request info
        https://docs.signalsciences.net/api/#_corps__corpName__sites__siteName__timeseries_requests_get
        GET /corps/{corpName}/sites/{siteName}/timeseries/requests
        """
        return self._make_request("{}/{}/sites/{}/timeseries/requests".format(
            self.ep_corps, self.corp, self.site), options=parameters)
