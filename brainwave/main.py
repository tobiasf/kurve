import time
from time import sleep

import numpy as np
import serial

import subprocess

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


def start_loop(headset):
    print('Starting loop...')
    now = time.time()
    future = now + 60 * 10

    data = [50, 50, 50]
    prev_measure = 50
    while time.time() < future:
        time.sleep(T)  # T is your sleep duration in seconds

        attention = headset.attention
        # measure = 100 - attention
        waves = dict(headset.waves)
        #                         for i in ['delta', 'theta', 'low-alpha', 'high-alpha', 'low-beta', 'high-beta', 'low-gamma', 'mid-gamma']:
        # Potentials
        # theta: <= 10k under rest, skyter opp til 50k+ ved bevegelser i øyner etc
        # low-beta: <= 20k under rest, skyter opp til 50k+ ved bevegelser i øyner etc
        wave_name = 'low-beta'
        if wave_name not in waves:
            continue

        measure = waves[wave_name]

        if measure == prev_measure:
            continue

        print("%s" % measure)
        # print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))

        prev_measure = measure
        data.append(measure)

        latest_data = np.array(data[-3:])
        diffs = np.diff(latest_data)
        avg_diff = np.mean(diffs)

        print("Average difference:", avg_diff)
        if avg_diff < 0:
            print("Overall trend: Declining")
        elif avg_diff == 0:
            print("Overall trend: Flat")
        else:
            print("Overall trend: Increasing")


def __main__():
    trigger = input("Restart bluetooth and start MindWave? (y/n): ")
    if trigger.lower() != 'y':
        print("Exiting...")
        exit(0)

    subprocess.run(["sudo", "pkill", "bluetoothd"])
    sleep(3)

    headset = connect_to_mindwave()
    if not headset:
        print("Failed to connect to Mindwave after 5 retries")
        exit(1)

    print('Connected, waiting 10 seconds for data to start streaming')
    time.sleep(6)

    start_loop(headset)


__main__()
