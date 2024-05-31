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

from lib.agent import SmartZoneAgent


def agentoutput(str):
    return [
        line.strip()
        for line in str.splitlines()
        if line.strip()
    ]


def test_main(capsys, public_api):
    a = SmartZoneAgent('https://vsz:8443/wsg/api/public', 'admin', 'admin!234')
    a.run()

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.splitlines() == agentoutput(r'''
        <<<smartzone_ap>>>
        {"deviceName":"AP001","description":"Description","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP002","description":"Description","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP005","description":"Description","status":"Offline","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP006","description":"Description","status":"Offline","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP007","description":"Description","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP008","description":"Description","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP009","description":"Description","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP054","description":"iYip7ido","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
        {"deviceName":"AP055","description":"llEtjoXe","status":"Online","alerts":0,"noise24G":null,"noise5G":null,"airtime24G":null,"airtime5G":null,"airtime6G":null,"latency24G":null,"latency50G":null,"latency6G":null,"firmwareVersion":null,"zoneFirmwareVersion":"3.5.0.102.79"}
    ''')
