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
    HostLabel,
    HostLabelGenerator,
    Metric,
    render,
    Result,
    Service,
    ServiceLabel,
    State,
)


_Section = list[dict]


def parse_json_list(string_table):
    return [
        json.loads(line[0])
        for line in string_table
    ]


def host_label_smartzone_ap(section: _Section) -> HostLabelGenerator:
    if len(section) == 1:
        ap = section[0]
        yield HostLabel('ruckus/smartzone/zone', ap['zoneName'])
        yield HostLabel('ruckus/smartzone/apgroup', ap['apGroupName'])
        yield HostLabel('ruckus/smartzone/model', ap['model'])


agent_section_smartzone_ap = AgentSection(
    name='smartzone_ap',
    parse_function=parse_json_list,
    host_label_function=host_label_smartzone_ap,
)

agent_section_smartzone_ap_alarm = AgentSection(
    name='smartzone_ap_alarm',
    parse_function=parse_json_list,
)


def discovery_smartzone_ap(
    section_smartzone_ap: _Section | None,
    section_smartzone_ap_alarm: _Section | None,
) -> DiscoveryResult:
    for ap in section_smartzone_ap:
        yield Service(item=ap['deviceName'], labels=[
            ServiceLabel('ruckus/smartzone/zone', ap['zoneName']),
            ServiceLabel('ruckus/smartzone/apgroup', ap['apGroupName']),
            ServiceLabel('ruckus/smartzone/model', ap['model']),
        ])


def check_smartzone_ap(
    item: str,
    section_smartzone_ap: _Section | None,
    section_smartzone_ap_alarm: _Section | None,
) -> CheckResult:
    ap = next((ap for ap in section_smartzone_ap if ap['deviceName'] == item), None)
    if ap is None:
        return

    yield Result(
        state=State.OK if ap['status'] == 'Online' else State.WARN,
        notice=f"Status: {ap['status']}",
    )
    yield Result(
        state=State.OK if ap['configurationStatus'] == 'Up-to-date' else State.WARN,
        notice=f"Config: {ap['configurationStatus']}",
    )

    yield Result(state=State.OK, summary=f"Model: {ap['model']}")

    if ap['firmwareVersion'] == ap['zoneFirmwareVersion']:
        yield Result(state=State.OK, summary=f"FW: {ap['firmwareVersion']}")
    else:
        yield Result(state=State.WARN, summary=f"FW: {ap['firmwareVersion']} (expected: {ap['zoneFirmwareVersion']})")

    if ap['noise24G']:
        yield Metric(name='airtime_24', value=ap['airtime24G'], boundaries=(0, 100))
        yield Metric(name='latency_24', value=ap['latency24G'])
        yield Metric(name='noise_24', value=ap['noise24G'])
        yield Metric(name='clients_24', value=ap['numClients24G'])
        yield Metric(name='eirp_24', value=ap['eirp24G'])

    if ap['noise5G']:
        yield Metric(name='airtime_5', value=ap['airtime5G'], boundaries=(0, 100))
        yield Metric(name='latency_5', value=ap['latency50G'])
        yield Metric(name='noise_5', value=ap['noise5G'])
        yield Metric(name='clients_5', value=ap['numClients5G'])
        yield Metric(name='eirp_5', value=ap['eirp50G'])

    if ap['noise6G']:
        yield Metric(name='airtime_6', value=ap['airtime6G'], boundaries=(0, 100))
        yield Metric(name='latency_6', value=ap['latency6G'])
        yield Metric(name='noise_6', value=ap['noise6G'])
        yield Metric(name='clients_6', value=ap['numClients6G'])
        yield Metric(name='eirp_6', value=ap['eirp6G'])

    value_store = get_value_store()
    for key, label, metric_name in (
        ('cumulativeRx24G', 'Received 2.4G', 'if24g_in_octets'),
        ('cumulativeTx24G', 'Transmitted 2.4G', 'if24g_out_octets'),
        ('cumulativeRx5G', 'Received 5G', 'if5g_in_octets'),
        ('cumulativeTx5G', 'Transmitted 5G', 'if5g_out_octets'),
        ('cumulativeRx6G', 'Received 6G', 'if6g_in_octets'),
        ('cumulativeTx6G', 'Transmitted 6G', 'if6g_out_octets'),
    ):
        if key in ap:
            try:
                value = get_rate(value_store, f"check_smartzone_ap.{item}.{key}", time.time(), ap[key])
                yield from check_levels(
                    value=value,
                    metric_name=metric_name,
                    render_func=render.iobandwidth,
                    boundaries=(0, None),
                    label=label,
                    notice_only=True,
                )
            except Exception:
                pass

    if section_smartzone_ap_alarm:
        for alarm in section_smartzone_ap_alarm:
            yield Result(
                state=State.CRIT if alarm['acknowledged'] != 'Yes' else State.WARN,
                summary=alarm['alarmType'],
                details=alarm['activity'],
            )


check_plugin_jb_fls = CheckPlugin(
    name='smartzone_ap',
    sections=['smartzone_ap', 'smartzone_ap_alarm'],
    service_name='AP %s',
    discovery_function=discovery_smartzone_ap,
    check_function=check_smartzone_ap,
)
