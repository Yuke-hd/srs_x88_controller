from remote import Subscriber
import time
from threading import Thread
from queue import Queue
from method import *
import requests
import json
import math as m

'''
Menu
    L Power
    |   L Toggle
    |   L On
    |   L Off
    |   L Current
    L Volume
    |   L Current (level & mute)
    |   L Mute
    |   L +
    |   L -
    L Source
        L Current
'''
main_menu = ['Power', 'Volume', 'Source']

system_endpoint = '/system'
audio_endpoint = '/audio'
av_endpoint = '/avContent'

endpoints = {
    "power": system_endpoint,
    "volume": audio_endpoint
}

power_option = {
    "off": "off",
    "active": "active",
    "on": "active"
}
mute_option = {
    "mute": "on",
    "unmute": "off"
}
input_option = {
    "linein": "extInput:line?port=1",
    "bt": "extInput:btAudio",
    "usb": "storage:usb1",
    "dac": "extInput:usbDac",
    "network": "netService:audio?service=spotify&contentId=-1"
}
current = 0
queue = Queue(maxsize=5)
current_input = "init"


def power_func(command):
    endpoint = "http://" + target_url + "/sony" + system_endpoint
    result = ""
    try:
        if command == 'current':
            response = requests.post(endpoint, json=methods[command]).json()
            result = response["result"][0]["status"]
        else:
            methods["set_power_data"]["params"][0]["status"] = power_option[command]
            response = requests.post(endpoint, json=methods["set_power_data"])
            result = "success" if response.status_code == 200 else "failed"
    except KeyError as err:
        result = set_error_msg("unrecognized command", command, 6)
    return result


def input_func(command):
    endpoint = "http://" + target_url + "/sony" + av_endpoint
    result = ""
    global current_input
    try:
        if command == 'current':
            if queue.qsize() == 0:
                result = current_input
            else:
                result = queue.get()
                current_input = result
        else:
            methods["input"]["params"][0]["uri"] = input_option[command]
            response = requests.post(endpoint, json=methods["input"])
            result = "success" if response.status_code == 200 else "failed"
    except KeyError as err:
        result = set_error_msg("unrecognized command", command, 6)
    return result


def volume_func(command):
    endpoint = "http://" + target_url + "/sony" + audio_endpoint
    result = ""
    try:
        if command == 'mute' or command == 'unmute':
            methods["mute"]["params"][0]["mute"] = mute_option[command]
            print(methods["mute"]["params"][0]["mute"])
            response = requests.post(endpoint, json=methods["mute"])
            result = "success" if response.status_code == 200 else "failed"
        elif command == 'current':
            response = requests.post(
                endpoint, json=methods["current_volume"]).json()
            result = response["result"][0][0]["volume"]
        else:
            x = int(command)
            if x not in range(100):
                raise ValueError
            methods["volume"]["params"][0]["volume"] = command
            response = requests.post(endpoint, json=methods["volume"])
            result = "success" if response.status_code == 200 else "failed"
    except TypeError as err:
        result = set_error_msg("unrecognized command", command, 7)
    except ValueError as err2:
        result = set_error_msg("not a valid number", command, 7)
    return result


def set_error_msg(msg, command, index):
    errmsg = ''
    for i in range(index):
        errmsg += ' '
    errmsg += '^ ' + msg + ": \"%s\"" % (command)
    return errmsg


def help():
    msg = ("-help: show help message\n"
           "  -power: control the power of SRS-X88. arguments: current, off, on, active\n"
           "  -volume: control the volume of SRS-X88. arguments: mute, unmute, [volume](1-100)\n"
           "  -input: select the input source of SRS-X88. arguments: current, linein, bt, usb, dac, network\n"
           "  -exit: exit"
           )
    return msg


functions = {
    "exit": exit,
    "power": power_func,
    "input": input_func,
    "volume": volume_func,
    "help": help
}


def menu_selection(command1, command2):
    try:
        result = functions[command1](command2)
    except KeyError as err:
        result = set_error_msg("unrecognized command", command1, 0)
    return result


def system_menu(command1):
    try:
        result = functions[command1]()
    except KeyError as err:
        result = set_error_msg("unrecognized command", command1, 0)
    return result


def menu():
    print(
        '================================\n'
        '|                              |\n'
        '|    Welcome to SRS-X88 CLI    |\n'
        '|                              |\n'
        '================================'
    )
    input_subscriber = Subscriber(target_url)
    t1 = Thread(target=input_subscriber.run, args=(queue,))
    t1.start()
    print("connecting...")
    time.sleep(1)
    while True:
        try:
            x = ""
            command = input('> ').split()
            if len(command) == 1:
                x = system_menu(command[0])
            else:
                x = menu_selection(command[0], command[1])
            print("+", x)
        except KeyboardInterrupt:
            print("[Main] trying to stop other threads")
            input_subscriber.stop()
            t1.join()
            exit()

        except IndexError:
            print("> invalid augment numbers")


# try:
#     while True:
#         time.sleep(2)
#         print("[Main] Updating view, current output: " + str(current))
# except KeyboardInterrupt:
#     print("[Main] trying to stop other threads")
#     subscriber.stop()
#     t1.join()
menu()
print("[Main] This is the end of Main thread")
