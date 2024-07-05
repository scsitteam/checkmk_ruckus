import requests
import logging
from functools import cached_property

LOGGING = logging.getLogger('ruckus.lib.ruckus')


class SmartZonePublicAPI:
    def __init__(self, prefix, username, password, verify_cert=True):
        self._prefix = prefix
        self._verify_cert = verify_cert

        resp = self.post('serviceTicket', json=dict(
            username=username,
            password=password,
        ))

        self._serviceTicket = resp['serviceTicket']

    @cached_property
    def apiInfo(self):
        return self.get('apiInfo', api_version=False)

    @cached_property
    def latest_version(self):
        return self.apiInfo['apiSupportVersions'][-1]

    @cached_property
    def _cli(self):
        return requests.Session()

    def request(self, method, ressource, api_version=True, params={}, **kwargs):
        if hasattr(self, '_serviceTicket'):
            params['serviceTicket'] = self._serviceTicket
        if api_version is True:
            api_version = self.latest_version
        url = "/".join(u for u in (self._prefix, api_version, ressource) if u)
        LOGGING.debug(f">> {method} {url}")
        resp = self._cli.request(method, url, params=params, verify=self._verify_cert, **kwargs)
        return resp.json()

    def get(self, ressource, **kwargs):
        return self.request('GET', ressource, **kwargs)

    def post(self, ressource, **kwargs):
        return self.request('POST', ressource, **kwargs)

    def query(self, ressource, json={}, **kwargs):
        LOGGING.debug(f">> QUERY {ressource}")
        json.update(dict(page=1))
        while True:
            page = self.post(f"query/{ressource}", json=json, **kwargs)
            for item in page['list']:
                yield item
            if not page['hasMore']:
                return
            json['page'] += 1

    def query_count(self, ressource, json={}, **kwargs):
        LOGGING.debug(f">> QUERY {ressource}")
        page = self.post(f"query/{ressource}", json=json, **kwargs)
        return page['totalCount']

    def retrive_list(self, ressource, fetch=False, params={}):
        params['index'] = 0
        while True:
            page = self.get(ressource, params=params)
            if 'data' in page:
                page = page['data']
            for item in page['list']:
                yield item
            if not page['hasMore']:
                return
            params['index'] += len(page['list'])
