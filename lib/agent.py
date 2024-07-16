#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# checkmk_ruckus - Checkmk Extension for monitoring Ruckus Smartzone.
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

from typing import Optional, Sequence
import logging
from functools import cached_property

from cmk.special_agents.v0_unstable.agent_common import (
    SectionWriter,
    ConditionalPiggybackSection,
    special_agent_main,
)
from cmk.special_agents.v0_unstable.argument_parsing import Args, create_default_argument_parser

from cmk_addons.plugins.smartzone.lib.ruckus import SmartZonePublicAPI

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LOGGING = logging.getLogger('agent_jb_fls')

ZONEPROPERTIES = (
    'zoneId', 'zoneName', 'totalAPs', 'connectedAPs', 'disconnectedAPs', 'rebootingAPs', 'clients'
)
APPROPERTIES = (
    'deviceName', 'model', 'description', 'status', 'configurationStatus', 'alerts',
    'noise24G', 'noise5G', 'noise6G',
    'airtime24G', 'airtime5G', 'airtime6G',
    'latency24G', 'latency50G', 'latency6G',
    'numClients24G', 'numClients5G', 'numClients6G',
    'firmwareVersion', 'zoneFirmwareVersion',
    'apGroupName', 'zoneName', 'lastSeen',
    'channel24gValue', 'channel50gValue', 'channel6gValue',
    'cumulativeTx24G', 'cumulativeTx5G', 'cumulativeTx6G',
    'cumulativeRx24G', 'cumulativeRx5G', 'cumulativeRx6G',
    'eirp24G', 'eirp50G', 'eirp6G',
)
WLANPROPERTIES = (
    'zoneName', 'name', 'ssid', 'availability',
    'authMethod', 'encryptionMethod', 'authType', 'availability',
    'trafficUplink', 'trafficDownlink',
    'numClients24G', 'numClients5G', 'numClients6G',
)
APWLANPROPERTIES = (
    'name', 'ssid', 'clients', 'totalNumClients',
    'rxBytes', 'txBytes', 'radioId',
)
RADIOPROPERTIES = (
    'radioId', 'txPower',
)


class AgentSmartZone:
    '''Checkmk special Agent for JetBrains Floating License Server'''

    def run(self, args=None):
        return special_agent_main(self.parse_arguments, self.main, args)

    def parse_arguments(self, argv: Optional[Sequence[str]]) -> Args:
        parser = create_default_argument_parser(description=self.__doc__)

        parser.add_argument('-U', '--url',
                            dest='url',
                            required=True,
                            help='Base-URL of the SmartZone Public API. (ex: https://HOST:8443/wsg/api/public)')
        parser.add_argument('-u', '--username',
                            dest='username',
                            required=True,
                            help='SmartZone user name.')
        parser.add_argument('-p', '--password',
                            dest='password',
                            required=True,
                            help='SmartZone password.')
        parser.add_argument('-t', '--timeout',
                            dest='timeout',
                            required=False,
                            default=10,
                            help='HTTP connection timeout. (Default: 10)')
        parser.add_argument('--ignore-cert',
                            dest='verify_cert',
                            action='store_false',
                            help='Do not verify the SSL cert from the REST andpoint.')

        return parser.parse_args(argv)

    @cached_property
    def api(self):
        return SmartZonePublicAPI(self.args.url, self.args.username, self.args.password, self.args.verify_cert)

    @cached_property
    def aps(self):
        return list(self.api.query('ap'))

    @cached_property
    def zones(self):
        return list(self.api.retrive_list('system/inventory'))

    @cached_property
    def wlans(self):
        return {
            wlan['wlanId']: wlan
            for wlan in self.api.query('wlan')
        }

    @cached_property
    def clients(self):
        for radioId in ('24G', '5G', '6G'):
            clients = []
            for client in self.api.query('client', json=dict(
                filters=[dict(type='DOMAIN', value='8b2081d5-9662-40d9-a3db-2a3cf4dde3f7')],
                extraFilters=[dict(type='RADIOID', value=radioId)],
            )):
                client.update(dict(radioId=radioId))
                clients.append(client)
            return clients

    def main(self, args: Args):
        self.args = args

        with SectionWriter('smartzone_zone') as section:
            for zone in self.zones:
                section.append_json({
                    key: zone.get(key)
                    for key in ZONEPROPERTIES
                    if key in zone
                })

        with SectionWriter('smartzone_ap') as section:
            for ap in self.aps:
                section.append_json({
                    key: ap.get(key)
                    for key in APPROPERTIES
                    if key in ap
                })

        with SectionWriter('smartzone_wlan') as section:
            for wlan in self.api.query('wlan'):

                wlan.update(dict(
                    numClients24G=self.api.query_count('client', json=dict(
                        filters=[dict(type='WLAN', value=wlan['wlanId'])],
                        extraFilters=[dict(type='RADIOID', value='2.4G')],
                    )),
                    numClients5G=self.api.query_count('client', json=dict(
                        filters=[dict(type='WLAN', value=wlan['wlanId'])],
                        extraFilters=[dict(type='RADIOID', value='5G')],
                    )),
                    numClients6G=self.api.query_count('client', json=dict(
                        filters=[dict(type='WLAN', value=wlan['wlanId'])],
                        extraFilters=[dict(type='RADIOID', value='6G')],
                    )),
                ))

                section.append_json({
                    key: wlan.get(key)
                    for key in WLANPROPERTIES
                    if key in wlan
                })

        for ap in self.aps:
            with ConditionalPiggybackSection(ap['deviceName']):
                with SectionWriter('smartzone_ap') as section:
                    section.append_json({
                        key: ap.get(key)
                        for key in APPROPERTIES
                        if key in ap
                    })

                with SectionWriter('smartzone_ap_alarm') as section:
                    for alarm in self.api.post('alert/alarm/list', json=dict(filters=[dict(type='AP', value=ap['apMac'])]))['list']:
                        if alarm['alarmState'] == 'Cleared':
                            continue
                        section.append_json(alarm)

                with SectionWriter('smartzone_ap_radio') as section:
                    for radio in self.api.retrive_list(f"aps/{ap['apMac']}/radios"):
                        section.append_json({
                            key: radio.get(key)
                            for key in RADIOPROPERTIES
                            if key in radio
                        })

                with SectionWriter('smartzone_ap_wlan') as section:
                    for wlan in self.api.retrive_list(f"aps/{ap['apMac']}/wlan"):
                        section.append_json({
                            key: wlan.get(key)
                            for key in APWLANPROPERTIES
                            if key in wlan
                        })
