import requests
from functools import cached_property


class SmartZonePublicAPI:
    def __init__(self, prefix, username, password):
        self._prefix = prefix

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
        resp = self._cli.request(method, url, params=params, **kwargs)
        return resp.json()

    def get(self, ressource, **kwargs):
        return self.request('GET', ressource, **kwargs)

    def post(self, ressource, **kwargs):
        return self.request('POST', ressource, **kwargs)
