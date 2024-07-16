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
from functools import reduce
from cmk.agent_based.v2 import (
    AgentSection,
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Service,
)


_Section = list[dict]


def parse_json_list(string_table):
    return [
        json.loads(line[0])
        for line in string_table
    ]


agent_section_smartzone_zone = AgentSection(
    name='smartzone_zone',
    parse_function=parse_json_list,
)


def discovery_smartzone_zone(
    section_smartzone_zone: _Section | None,
    section_smartzone_ap: _Section | None,
) -> DiscoveryResult:
    if section_smartzone_zone is None:
        return
    for zone in section_smartzone_zone:
        yield Service(item=zone['zoneName'])


def check_smartzone_zone(
    item: str,
    section_smartzone_zone: _Section | None,
    section_smartzone_ap: _Section | None,
) -> CheckResult:
    zone = next((zone for zone in section_smartzone_zone if zone['zoneName'] == item), None)
    if zone is None:
        return

    aps = [
        ap for ap in section_smartzone_ap
        if ap['zoneName'] == item
    ]

    yield from check_levels(
        value=zone['connectedAPs'],
        metric_name='aps_connected',
        boundaries=(0, zone['totalAPs']),
        label='Connected APs',
    )

    yield from check_levels(
        value=zone['disconnectedAPs'],
        metric_name='aps_disconnected',
        boundaries=(0, zone['totalAPs']),
        label='Disconnected APs',
        levels_upper=('fixed', (1, zone['totalAPs'] / 10)),
        notice_only=True
    )

    yield from check_levels(
        value=zone['rebootingAPs'],
        metric_name='aps_rebooting',
        boundaries=(0, zone['totalAPs']),
        label='Rebooting APs',
        levels_upper=('fixed', (1, zone['totalAPs'] / 10)),
        notice_only=True
    )

    apsum = reduce(lambda sum, ap: {k: sum[k] + ap[k] for k in sum}, aps, dict(numClients24G=0, numClients5G=0, numClients6G=0))
    yield Metric(name='clients_24', value=apsum['numClients24G'])
    yield Metric(name='clients_5', value=apsum['numClients5G'])
    yield Metric(name='clients_6', value=apsum['numClients6G'])


check_plugin_smartzone_zone = CheckPlugin(
    name='smartzone_zone',
    sections=['smartzone_zone', 'smartzone_ap'],
    service_name='Zone %s',
    discovery_function=discovery_smartzone_zone,
    check_function=check_smartzone_zone,
)
