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
from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Result,
    Service,
    State,
    Metric,
)


_Section = list[dict]


def parse_json_list(string_table):
    return [
        json.loads(line[0])
        for line in string_table
    ]


agent_section_smartzone_ap_radio = AgentSection(
    name='smartzone_ap_radio',
    parse_function=parse_json_list,
)


def discovery_smartzone_ap_radio(
    section: _Section | None,
) -> DiscoveryResult:
    for radio in section:
        yield Service(item=radio['radioId'])


def check_smartzone_ap_radio(
    item: str,
    section: _Section | None,
) -> CheckResult:
    radio = next((radio for radio in section if radio['radioId'] == item), None)
    if radio is None:
        return

    yield Result(state=State.OK, summary=f"TX power: {radio['txPower']}")

    if radio['txPower'] == 'max':
        power = 0
    elif radio['txPower'] == 'min':
        power = -11
    else:
        power = int(radio['txPower'].split(' ')[0])
    yield Metric(name='tx_power', value=power)


check_plugin_smartzone_ap_radio = CheckPlugin(
    name='smartzone_ap_radio',
    service_name='Radio %s',
    discovery_function=discovery_smartzone_ap_radio,
    check_function=check_smartzone_ap_radio,
)
