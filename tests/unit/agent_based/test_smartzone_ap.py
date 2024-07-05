# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# smartzone_wlan - Ruckus AP WLan for Checkmk
#
# Copyright (C) 2023 Marius Rieder <marius.rieder@scs.ch>
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

import pytest  # type: ignore[import]
from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import smartzone_wlan

EXAMPLE_STRING_TABLE = [
    ['{"authMethod": "OPEN", "availability": 1, "encryptionMethod": "NONE", "name": "None", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "None", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}'],
    ['{"authMethod": "OPEN", "encryptionMethod": "WEP", "name": "WEP128", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WEP128", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}'],
    ['{"authMethod": "OPEN", "encryptionMethod": "WEP", "name": "WEP64", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WEP64", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}'],
    ['{"authMethod": "OPEN", "encryptionMethod": "WPA", "name": "WPA-Mixed", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WPA-Mixed", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}'],
    ['{"authMethod": "OPEN", "encryptionMethod": "WPA", "name": "wpa2", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "wpa2", "trafficDownlink": 100, "trafficUplink": 200, "zoneName": "public-api-zone-ipv6"}'],
]
EXAMPLE_SECTION = [
    {'authMethod': 'OPEN', 'availability': 1, 'encryptionMethod': 'NONE', 'name': 'None', 'numClients24G': 2, 'numClients5G': 2, 'numClients6G': 2, 'ssid': 'None', 'trafficDownlink': None, 'trafficUplink': None, "zoneName": "public-api-zone-ipv6"},
    {'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP128', 'numClients24G': 2, 'numClients5G': 2, 'numClients6G': 2, 'ssid': 'WEP128', 'trafficDownlink': None, 'trafficUplink': None, "zoneName": "public-api-zone-ipv6"},
    {'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP64', 'numClients24G': 2, 'numClients5G': 2, 'numClients6G': 2, 'ssid': 'WEP64', 'trafficDownlink': None, 'trafficUplink': None, "zoneName": "public-api-zone-ipv6"},
    {'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'WPA-Mixed', 'numClients24G': 2, 'numClients5G': 2, 'numClients6G': 2, 'ssid': 'WPA-Mixed', 'trafficDownlink': None, 'trafficUplink': None, "zoneName": "public-api-zone-ipv6"},
    {'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'wpa2', 'numClients24G': 2, 'numClients5G': 2, 'numClients6G': 2, 'ssid': 'wpa2', 'trafficDownlink': 100, 'trafficUplink': 200, "zoneName": "public-api-zone-ipv6"},
]


@pytest.mark.parametrize('string_table, result', [
    ([], []),
    (EXAMPLE_STRING_TABLE, EXAMPLE_SECTION),
])
def test_parse_smartzone_wlan(string_table, result):
    assert list(smartzone_wlan.parse_smartzone_wlan(string_table)) == result


@pytest.mark.parametrize('section, params, result', [
    ([], {}, []),
    (EXAMPLE_SECTION, {}, [
        Service(item='None', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'NONE', 'name': 'None', 'ssid': 'None', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='WEP128', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP128', 'ssid': 'WEP128', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='WEP64', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP64', 'ssid': 'WEP64', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='WPA-Mixed', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'WPA-Mixed', 'ssid': 'WPA-Mixed', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='wpa2', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'wpa2', 'ssid': 'wpa2', 'zoneName': 'public-api-zone-ipv6'}),
    ]),
    (EXAMPLE_SECTION, {'naming': 'zone_ssid'}, [
        Service(item='public-api-zone-ipv6/None', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'NONE', 'name': 'None', 'ssid': 'None', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='public-api-zone-ipv6/WEP128', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP128', 'ssid': 'WEP128', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='public-api-zone-ipv6/WEP64', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WEP', 'name': 'WEP64', 'ssid': 'WEP64', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='public-api-zone-ipv6/WPA-Mixed', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'WPA-Mixed', 'ssid': 'WPA-Mixed', 'zoneName': 'public-api-zone-ipv6'}),
        Service(item='public-api-zone-ipv6/wpa2', parameters={'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'wpa2', 'ssid': 'wpa2', 'zoneName': 'public-api-zone-ipv6'}),
    ]),
])
def test_discovery_smartzone_wlan(section, params, result):
    assert list(smartzone_wlan.discovery_smartzone_wlan(params, section)) == result


@pytest.mark.parametrize('item, params,, result', [
    ('', {}, []),
    (
        'public-api-zone-ipv6/wpa2',
        {'authMethod': 'OPEN', 'encryptionMethod': 'WPA', 'name': 'wpa2', 'ssid': 'wpa2', 'zoneName': 'public-api-zone-ipv6'},
        [
            Result(state=State.OK, summary='SSID: wpa2'),
            Result(state=State.OK, summary='Auth: OPEN'),
            Result(state=State.OK, summary='Enc: WPA'),
            Result(state=State.OK, notice='Clients 2.4G: 2.00'),
            Metric('clients_24', 2.0),
            Result(state=State.OK, notice='Clients 5G: 2.00'),
            Metric('clients_5', 2.0),
            Result(state=State.OK, notice='Clients 6G: 2.00'),
            Metric('clients_6', 2.0),
            Result(state=State.OK, summary='Received: 200 B/s'),
            Metric('if_in_octets', 200.0, boundaries=(0.0, None)),
            Result(state=State.OK, summary='Transmitted: 100 B/s'),
            Metric('if_out_octets', 100.0, boundaries=(0.0, None)),
        ]
    ),
])
def test_check_smartzone_wlan(monkeypatch, item, params, result):
    monkeypatch.setattr(smartzone_wlan, 'get_value_store', lambda: {})
    monkeypatch.setattr(smartzone_wlan, 'get_rate', lambda _v, _k, _t, v: v)
    assert list(smartzone_wlan.check_smartzone_wlan(item, params, EXAMPLE_SECTION)) == result
