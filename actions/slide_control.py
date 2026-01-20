import pyautogui
import time

def next_slide():
    print("[Slide] Next Slide")
    pyautogui.press("right")
    time.sleep(0.25)

def previous_slide():
    print("[Slide] Previous Slide")
    pyautogui.press("left")
    time.sleep(0.25)

def start_presentation():
    print("[Slide] Start Presentation")
    pyautogui.press("f5")
    time.sleep(0.3)

def exit_presentation():
    print("[Slide] Exit Presentation")
    pyautogui.press("esc")
    time.sleep(0.3)
