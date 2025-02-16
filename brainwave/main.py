import subprocess
import time
from time import sleep

import numpy as np
import pyautogui
import serial

import mindwave

fs = 100
T = 1 / fs

isLeft = False
isDown = False


def start_pressing_left():
    global isLeft, isDown
    if isLeft:
        return

    isLeft = True
    isDown = False
    pyautogui.keyUp("down")
    pyautogui.keyDown("left")


def stop_pressing_left():
    global isLeft
    if not isLeft:
        return

    isLeft = False
    pyautogui.keyUp("left")


def all_keys_up():
    global isLeft, isDown
    pyautogui.keyUp("left")
    pyautogui.keyUp("down")
    isLeft = False
    isDown = False


def start_pressing_down():
    global isDown, isLeft
    if isDown:
        return

    isLeft = False
    isDown = True
    pyautogui.keyUp("left")
    pyautogui.keyDown("down")


def stop_pressing_down():
    global isDown
    if not isDown:
        return

    isDown = True
    pyautogui.keyUp("down")


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
    pyautogui.keyDown("left")

    print('Starting loop...')
    now = time.time()
    future = now + 60 * 10

    data = [50, 50, 50]
    prev_measure = 50
    while time.time() < future:
        time.sleep(T)  # T is your sleep duration in seconds

        waves = dict(headset.waves)

        wave_name = 'delta'
        if wave_name not in waves:
            continue

        measure = int(waves[wave_name])

        if measure == prev_measure:
            continue

        # print ("Raw value: %s, Attention: %s, Meditation: %s" % (headset.raw_value, headset.attention, headset.meditation))

        prev_measure = measure

        upper_threshold = 350_000
        data.append(measure)
        median = np.median(data[-3:])

        print("%s - Med: %s" % (measure, median))
        if measure > upper_threshold:
            start_pressing_down()
            print("Right")
        else:
            start_pressing_left()
            print("Left")

        #
        # latest_data = np.array(data[-2:])
        # diffs = np.diff(latest_data)
        # avg_diff = np.mean(diffs)
        #
        # print("Average difference:", avg_diff)
        # if avg_diff < 0:
        #     stop_pressing_down()
        #     print("Declining / Left")
        # elif avg_diff == 0:
        #     print("Overall trend: Flat")
        # else:
        #     print("Increasing / Right")
        #     start_pressing_down()


def __main__():
    trigger = input("Restart bluetooth and start MindWave? (n?): ")
    if trigger.lower() == 'n':
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
