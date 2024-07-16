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

from cmk_addons.plugins.smartzone.lib.agent import AgentSmartZone


def agentoutput(str):
    return [
        line.strip()
        for line in str.splitlines()
        if line.strip()
    ]


def test_main(capsys, public_api):
    agent = AgentSmartZone()
    agent.run(['--debug', '-U', 'https://vsz:8443/wsg/api/public', '-u', 'admin', '-p', 'admin!234'])

    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out.splitlines() == agentoutput(r'''
        <<<smartzone_zone:sep(0)>>>
        {"clients": 0, "connectedAPs": 0, "disconnectedAPs": 0, "rebootingAPs": 0, "totalAPs": 0, "zoneId": "f77a8816-3049-40cd-8484-82919275ddc3", "zoneName": "Default Zone"}
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP001", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP002", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP005", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Offline", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP006", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Offline", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP007", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP008", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP009", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "iYip7ido", "deviceName": "AP054", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "description": "llEtjoXe", "deviceName": "AP055", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_wlan:sep(0)>>>
        {"authMethod": "OPEN", "availability": 1, "encryptionMethod": "NONE", "name": "None", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "None", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}
        {"authMethod": "OPEN", "encryptionMethod": "WEP", "name": "WEP128", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WEP128", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}
        {"authMethod": "OPEN", "encryptionMethod": "WEP", "name": "WEP64", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WEP64", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}
        {"authMethod": "OPEN", "encryptionMethod": "WPA", "name": "WPA-Mixed", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "WPA-Mixed", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}
        {"authMethod": "OPEN", "encryptionMethod": "WPA", "name": "wpa2", "numClients24G": 2, "numClients5G": 2, "numClients6G": 2, "ssid": "wpa2", "trafficDownlink": null, "trafficUplink": null, "zoneName": "public-api-zone-ipv6"}
        <<<<AP001>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP001", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP002>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP002", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP005>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP005", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Offline", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP006>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP006", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Offline", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP007>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP007", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP008>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP008", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP009>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "Description", "deviceName": "AP009", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP054>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "cumulativeRx24G": 530656, "cumulativeRx5G": 605, "cumulativeRx6G": 0, "cumulativeTx24G": 9696427, "cumulativeTx5G": 230, "cumulativeTx6G": 0, "description": "iYip7ido", "deviceName": "AP054", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
        <<<<AP055>>>>
        <<<smartzone_ap:sep(0)>>>
        {"airtime24G": null, "airtime5G": null, "airtime6G": null, "alerts": 0, "apGroupName": null, "configurationStatus": null, "description": "llEtjoXe", "deviceName": "AP055", "eirp24G": 20, "eirp50G": 24, "eirp6G": 24, "firmwareVersion": null, "lastSeen": null, "latency24G": null, "latency50G": null, "latency6G": null, "model": null, "noise24G": null, "noise5G": null, "numClients24G": 0, "numClients5G": 0, "numClients6G": 0, "status": "Online", "zoneFirmwareVersion": "3.5.0.102.79", "zoneName": null}
        <<<smartzone_ap_alarm:sep(0)>>>
        <<<smartzone_ap_radio:sep(0)>>>
        {"radioId": "0", "txPower": "max"}
        {"radioId": "1", "txPower": "max"}
        {"radioId": "2", "txPower": "-1 dB"}
        <<<smartzone_ap_wlan:sep(0)>>>
        {"radioId": "0", "rxBytes": "530656", "ssid": "None", "totalNumClients": "0", "txBytes": "9702674"}
        <<<<>>>>
    ''')  # noqa: E501
