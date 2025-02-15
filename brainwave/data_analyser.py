import subprocess
import time
from time import sleep

import numpy as np
import pyautogui
import serial
from numpy.f2py.auxfuncs import isreal

import mindwave

fs = 100
T = 1 / fs


def connect_to_mindwave():
    print('Connecting to Mindwave...')
    headset = 0
    for _ in range(5):
        try:
            headset = mindwave.Headset('/dev/tty.MindWaveMobile')
            break
        except serial.serialutil.SerialException as _2:
            print("Failed, retrying...")
            sleep(3)

    return headset

data = []
def start_loop(headset):
    pyautogui.keyDown("left")

    print('Starting loop...')
    now = time.time()
    future = now + 40

    low = []
    high = []
    low2 = []
    high2 = []
    prev_measure = 0
    iteration = 0
    while time.time() < future:
        if time.time() > now + 10 and iteration < 1:
            iteration = 1
            print("HIGH!!!")
        if time.time() > now + 20 and iteration < 2:
            iteration = 2
            print("LOW!!!")
        if time.time() > now + 30 and iteration < 3:
            iteration = 3
            print("HIGH!!!")

        time.sleep(T)  # T is your sleep duration in seconds

        # measure = 100 - attention
        waves = dict(headset.waves)
        #                         for i in ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']:
        # Potentials
        # theta: <= 10k under rest, skyter opp til 50k+ ved bevegelser i øyner etc
        # low-beta: <= 15k under rest, skyter opp til 50k+ ved bevegelser i øyner etc
        wave_name = ('delta')
        if wave_name not in waves:
            continue

        measure = int(waves[wave_name])

        if measure == prev_measure:
            continue

        if iteration == 0:
            low.append(measure)
        elif iteration == 1:
            high.append(measure)
        elif iteration == 2:
            low2.append(measure)
        elif iteration == 3:
            high2.append(measure)

        data.append(measure)
        median = np.median(data[-3:])

        print("%s - %s" % (measure, median))
        # print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))

        prev_measure = measure

    return low, high, low2, high2


def __main__():
    trigger = input("Restart bluetooth and start MindWave? (n?): ")
    if trigger.lower() == "n":
        print("Exiting...")
        exit(0)

    subprocess.run(["sudo", "pkill", "bluetoothd"])
    sleep(3)

    headset = connect_to_mindwave()
    if not headset:
        print("Failed to connect to Mindwave after 5 retries")
        exit(1)

    print('Connected, waiting 10 seconds for data to start streaming')
    time.sleep(10)

    low, high, low2, high2 = start_loop(headset)
    print(low)
    print(high)
    print(low2)
    print(high2)


__main__()
