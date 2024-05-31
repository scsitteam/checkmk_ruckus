import json
from lib.ruckus import SmartZonePublicAPI

APPROPERTIES = (
    'deviceName', 'description', 'status', 'alerts',
    'noise24G', 'noise5G', 'noise6G',
    'airtime24G', 'airtime5G', 'airtime6G',
    'latency24G', 'latency50G', 'latency6G',
    'firmwareVersion', 'zoneFirmwareVersion',
)


class SmartZoneAgent:
    def __init__(self, prefix, username, password):
        self.api = SmartZonePublicAPI(prefix, username, password)

    def run(self):
        print('<<<smartzone_ap>>>')
        for ap in self.api.post('query/ap')['list']:
            print(json.dumps({
                key: ap.get(key)
                for key in APPROPERTIES
                if key in ap
            }, separators=(',', ':')))
