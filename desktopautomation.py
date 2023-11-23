
import pyautogui
import time

def runapp(appname):
    pyautogui.hotkey("win", "r") 
    time.sleep(1)
    pyautogui.typewrite(appname)
    pyautogui.press("enter")
    time.sleep(1)

runapp(input("APPNAME: "))


