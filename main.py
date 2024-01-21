from time import sleep
import shutil
import os
import keyboard
import mss
import cv2
import numpy
from time import time, sleep
import pyautogui
from random import randint
import math

DELAY_BETWEEN_COMMANDS = 1.00
sct = mss.mss()
mon = sct.monitors[0]

print("Select monitor number from below available monitors...")
counter = 0
for m in sct.monitors:
    print("Monitor: ",counter)
    counter += 1
num = input("Press Enter the number to continue...")
print("key presses: ", num)
mon = sct.monitors[int(num)]



second_roi = {
    "left": 0, 
    "top": 0, 
    "width": int(mon["width"]), 
    "height": int(mon["height"])
}

thresh = 0.85 


def main():
    # initialzing PyAutoGUI
    initializePyAutoGUI()
    # starting browser
    startBrowser()
    # sleep to load the browser
    sleep(3.0)
    # type text in browser's address bar
    typeTexts()
    #sleep(3.0)
    # this open new tab
    #startNewTab()

    print("Done")

def startBrowser():

    btn_start = cv2.imread('images/firefox.png')
    btn_start_offset_y = int(btn_start.shape[0])
    btn_start_offset_x = int(btn_start.shape[1] / 2)


    thresh = 0.85 
    frame_list = []
    btn_cnt = 1
    frame_id = 0
    while True:
        frame_id += 1
        second_roi_crop = numpy.array(sct.grab(second_roi))[:,:,:3]

        result_btn_start = cv2.matchTemplate(second_roi_crop, btn_start, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(result_btn_start)
        print(": startBrowser: ",max_val)


        speed = math.floor(math.log(frame_id)**2.4)
        frame_list.append(max_loc[0])
        if max_val > thresh:
            button_center = (max_loc[0] + btn_start_offset_x, max_loc[1] + btn_start_offset_y)
            abs_x_sec = second_roi["left"] + button_center[0]
            abs_y_sec = second_roi["top"] + button_center[1] + speed
            pyautogui.moveTo(abs_x_sec, abs_y_sec, 0.25)
            sleep(1.0)
            pyautogui.click()
            btn_cnt += 1
            break

        if keyboard.is_pressed('q'):
            break

def typeTexts():
    # give the text below to browse the text to the browser
    textStr = "Hellow World"
    pyautogui.typewrite(textStr)
    sleep(3.0)
    pyautogui.press('enter')

def startNewTab():

    btn_start = cv2.imread('images/firefox_plus_1.png')
    btn_start_offset_y = int(btn_start.shape[0])
    btn_start_offset_x = int(btn_start.shape[1] / 2)


    thresh = 0.85 
    frame_list = []
    btn_cnt = 1
    frame_id = 0
    while True:
        frame_id += 1
        second_roi_crop = numpy.array(sct.grab(second_roi))[:,:,:3]

        result_btn_start = cv2.matchTemplate(second_roi_crop, btn_start, cv2.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv2.minMaxLoc(result_btn_start)
        print(": startBrowser: ",max_val)


        speed = math.floor(math.log(frame_id)**2.4)
        frame_list.append(max_loc[0])
        if max_val > thresh:
            button_center = (max_loc[0] + btn_start_offset_x, max_loc[1] + btn_start_offset_y)
            abs_x_sec = second_roi["left"] + button_center[0]
            abs_y_sec = second_roi["top"] + button_center[1] + speed
            pyautogui.moveTo(abs_x_sec, abs_y_sec, 0.25)
            sleep(1.0)
            pyautogui.click()
            btn_cnt += 1
            break

        if keyboard.is_pressed('q'):
            break

def initializePyAutoGUI():
    # Initialized PyAutoGUI
    # https://pyautogui.readthedocs.io/en/latest/introduction.html
    # When fail-safe mode is True, moving the mouse to the upper-left corner will abort your program.
    pyautogui.FAILSAFE = True

if __name__ == "__main__":
    main()
