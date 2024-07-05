# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Ruckus Extension for Checkmk
#
# Copyright (C) 2024 Marius Rieder <marius.rieder@scs.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os
import io
import json
from pathlib import Path
import pytest
import requests
from urllib.parse import urlparse

BASEURL = 'https://vsz:8443/wsg/api/public/'
VERSION = 'vcmk_test'


@pytest.fixture
def public_api(requests_mock):
    def public_api_matcher(request):
        if not request.url.startswith(BASEURL):
            return None

        url = urlparse(request.url[len(BASEURL):])

        if request.method == 'GET' and url.path == 'apiInfo':
            resp = requests.Response()
            json_str = json.dumps(dict(apiSupportVersions=[VERSION]))
            bytes_data = json_str.encode('utf-8')
            resp.raw = io.BytesIO(bytes_data)
            resp.status_code = 200
            return resp

        if not url.path.startswith(f"{VERSION}/"):
            resp = requests.Response()
            json_str = json.dumps(dict(success=False))
            bytes_data = json_str.encode('utf-8')
            resp.raw = io.BytesIO(bytes_data)
            resp.status_code = 404
            return resp

        mockpath = Path(__file__).parent / 'public_api_mock' / f"{url.path[len(f"{VERSION}/"):]}.{request.method.lower()}.json"

        if not os.access(mockpath, os.R_OK):
            resp = requests.Response()
            json_str = json.dumps(dict(success=False, mockpath=str(mockpath)))
            bytes_data = json_str.encode('utf-8')
            resp.raw = io.BytesIO(bytes_data)
            resp.status_code = 404
            return resp

        resp = requests.Response()
        resp.raw = open(mockpath, mode='rb')
        resp.status_code = 200
        return resp

    requests_mock.add_matcher(public_api_matcher)
