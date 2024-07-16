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

from functools import reduce
from cmk.agent_based.v2 import (
    check_levels,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Metric,
    Service,
)


_Section = list[dict]


def discovery_smartzone_apgroup(
    section: _Section | None,
) -> DiscoveryResult:
    apgroups = set(ap['apGroupName'] for ap in section)
    if len(apgroups) <= 1:
        return
    for group in apgroups:
        yield Service(item=group)


def check_smartzone_apgroup(
    item: str,
    section: _Section | None,
) -> CheckResult:
    aps = [
        ap for ap in section
        if ap['apGroupName'] == item
    ]
    if len(aps) == 0:
        return

    yield from check_levels(
        value=reduce(lambda sum, ap: sum + (1 if ap['status'] in ['Online', 'Flagged'] else 0), aps, 0),
        metric_name='aps_connected',
        boundaries=(0, len(aps)),
        label='Connected APs',
    )

    apsum = reduce(lambda sum, ap: {k: sum[k] + ap[k] for k in sum}, aps, dict(numClients24G=0, numClients5G=0, numClients6G=0))
    yield Metric(name='clients_24', value=apsum['numClients24G'])
    yield Metric(name='clients_5', value=apsum['numClients5G'])
    yield Metric(name='clients_6', value=apsum['numClients6G'])


check_plugin_smartzone_apgroup = CheckPlugin(
    name='smartzone_apgroup',
    sections=['smartzone_ap'],
    service_name='Group %s',
    discovery_function=discovery_smartzone_apgroup,
    check_function=check_smartzone_apgroup,
)
