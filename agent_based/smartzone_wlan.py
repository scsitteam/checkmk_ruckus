#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2024  Marius Rieder <marius.rieder@scs.ch>
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

from collections.abc import Mapping
import json
import time
from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    get_rate,
    get_value_store,
    Service,
    Result,
    State,
    render,
)


_Section = list[dict]


def parse_smartzone_wlan(string_table):
    return [
        json.loads(line[0])
        for line in string_table
    ]


agent_section_smartzone_ap = AgentSection(
    name= 'smartzone_wlan',
    parse_function=parse_smartzone_wlan,
)


def discovery_smartzone_wlan(params: Mapping[str, dict], section: _Section) -> DiscoveryResult:
    for wlan in section:
        match params.get('naming'):
            case 'zone_wlan':
                item = f"{wlan['zoneName']}/{wlan['name']}"
            case 'zone_ssid':
                item = f"{wlan['zoneName']}/{wlan['ssid']}"
            case 'ssid':
                item = wlan['ssid']
            case _:
                item = wlan['name']
        yield Service(item=item, parameters={key: wlan[key] for key in ('zoneName', 'name', 'ssid', 'authMethod', 'authType', 'encryptionMethod') if key in wlan})


def check_smartzone_wlan(item, params, section: _Section) -> CheckResult:
    wlan = next((wlan for wlan in section if wlan['zoneName'] == params.get('zoneName') and wlan['name'] == params.get('name')), None)
    if wlan is None:
        return

    for label, key in (
        ('SSID', 'ssid'),
        ('Auth', 'authMethod'),
        ('AuthType', 'authType'),
        ('Enc', 'encryptionMethod'),
    ):
        if key not in wlan and key not in params:
            continue
        if wlan.get(key) == params.get(key):
            yield Result(state=State.OK, summary=f"{label}: {wlan.get(key)}")
        else:
            yield Result(state=State.WARN, summary=f"{label}: {wlan.get(key)} (expected: {params.get(key)})")

    yield from check_levels(
        label='Clients 2.4G',
        value=int(wlan.get('numClients24G', 0)) or 0,
        metric_name='clients_24',
        notice_only=True,
    )
    yield from check_levels(
        label='Clients 5G',
        value=int(wlan.get('numClients5G', 0)) or 0,
        metric_name='clients_5',
        notice_only=True,
    )
    yield from check_levels(
        label='Clients 6G',
        value=int(wlan.get('numClients6G', 0)) or 0,
        metric_name='clients_6',
        notice_only=True,
    )

    value_store = get_value_store()
    if wlan.get('trafficUplink'):
        try:
            value = get_rate(value_store, f"check_smartzone_wlan.{wlan['zoneName']}.{wlan['name']}.trafficUplink", time.time(), int(wlan.get('trafficUplink', 0)))
            yield from check_levels(
                value=value,
                metric_name='if_in_octets',
                render_func=render.iobandwidth,
                boundaries=(0, None),
                label='Received',
            )
        except Exception:
            pass

    if wlan.get('trafficDownlink'):
        try:
            value = get_rate(value_store, f"check_smartzone_wlan.{wlan['zoneName']}.{wlan['name']}.trafficDownlink", time.time(), int(wlan.get('trafficDownlink', 0)))
            yield from check_levels(
                value=value,
                metric_name='if_out_octets',
                render_func=render.iobandwidth,
                boundaries=(0, None),
                label='Transmitted',
            )
        except Exception:
            pass


check_plugin_smartzone_wlan = CheckPlugin(
    name='smartzone_wlan',
    service_name='WLAN %s',
    discovery_function=discovery_smartzone_wlan,
    discovery_ruleset_name='smartzone_wlan',
    discovery_default_parameters={},
    check_function=check_smartzone_wlan,
    check_default_parameters={},
)
