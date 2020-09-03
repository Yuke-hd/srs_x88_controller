# Sony SRS-X88 controller over wifi
A python implementation of (part of) the [Sony Audio Control API](https://developer.sony.com/develop/audio-control-api/)

## Setup
In `method.py`: replace `target_url` with your own device's ip address

Refer to [this link](https://developer.sony.com/develop/audio-control-api/hardware-overview/discovery-process) for device discovery process

Run `main.py`

## Commands
### Currently supported functions
- `exit`
 - `help` : show the help message
 - `power`:
	 - `on/active` : turn on the device (put the device in active mode)
	 - `off` : put the device in stanby mode
	 - `current` : get the current power status of the device
- `volume` :
	- `mute/unmute` : toggle mute on the device (buggy, according to sony's api, it should actually mute or unmute device instead toggling)
	- `[volume]` : set the volume level, takes an integer from `0-100` 
	- `current`: get the current volume level of the device
- `input`
	- `[source]`: set the audio source, SRS-X88 supported source: `linein, bt, usb, dac, network`  
	- `current`: get the current audio source of the device

**Not all methods from sony's documents will be supported due to the SRS-X88 is not offically supported by sony to use their Audio Control API**
### Usage
`> power on`
`> input dac`

## Requirements
- Python 3.8

## What's next?
- improve the thread handling
- try to support more methods
- try to develop a GUI (i'm new to python and python gui programming. please contact me if you are able to help)
