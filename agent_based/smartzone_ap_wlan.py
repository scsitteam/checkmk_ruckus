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
    GetRateError,
    Metric,
    Service,
)


_Section = list[dict]


def parse_smartzone_ap_wlan(string_table):
    return [
        json.loads(line[0])
        for line in string_table
    ]


agent_section_smartzone_ap = AgentSection(
    name= 'smartzone_ap_wlan',
    parse_function=parse_smartzone_ap_wlan,
)


def discovery_smartzone_ap_wlan(section: _Section) -> DiscoveryResult:
    for wlan in section:
        yield Service(item=f"{wlan['radioId']}:{wlan['ssid']}", parameters=dict(radioId=wlan['radioId'], ssid=wlan['ssid']))


def check_smartzone_ap_wlan(item, section: _Section) -> CheckResult:
    wlan = next((wlan for wlan in section if f"{wlan['radioId']}:{wlan['ssid']}" == item), None)
    if wlan is None:
        return

    yield from check_levels(
        label='Clients',
        value=int(wlan.get('totalNumClients', 0)) or 0,
        metric_name='clients',
    )

    value_store = get_value_store()
    try:
        yield Metric(name='if_in_octets', value=get_rate(value_store, f"check_smartzone_ap_wlan.{item}.in", time.time(), int(wlan.get('rxBytes', 0))))
    except GetRateError:
        pass
    try:
        yield Metric(name='if_out_octets', value=get_rate(value_store, f"check_smartzone_ap_wlan.{item}.out", time.time(), int(wlan.get('txBytes', 0))))
    except GetRateError:
        pass


check_plugin_smartzone_ap_wlan = CheckPlugin(
    name='smartzone_ap_wlan',
    service_name='WLAN %s',
    discovery_function=discovery_smartzone_ap_wlan,
    check_function=check_smartzone_ap_wlan,
)
