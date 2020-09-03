'''
these methods have been tested and have been proven to work with SRS-X88
for more details, visit:
https://developer.sony.com/develop/audio-control-api/api-references/api-overview-2
'''
target_url = "192.168.0.34:54480"

methods = {
    "set_power_data": {
        "method": "setPowerStatus",
        "id": 10,
        "params": [
            {
                "status": ""
            }
        ],
        "version": "1.1"
    },
    "current": {
        "method": "getPowerStatus",
        "id": 50,
        "params": [],
        "version": "1.1"
    },
    "volume": {
        "method": "setAudioVolume",
        "id": 98,
        "params": [
            {
                "volume": "30"
            }
        ],
        "version": "1.1"
    },
    "current_volume": {
        "method": "getVolumeInformation",
        "id": 33,
        "params": [{}],
        "version": "1.1"
    },
    "mute": {
        "method": "setAudioMute",
        "id": 601,
        "params": [
            {
                "mute": ""
            }
        ],
        "version": "1.1"
    },
    "input": {
        "method": "setPlayContent",
        "id": 47,
        "params": [
            {
                "uri": ""
            }
        ],
        "version": "1.2"
    }
}
