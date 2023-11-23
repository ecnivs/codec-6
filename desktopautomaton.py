import pyautogui
import time
import requests
import re

def is_valid_website(site):
    try:
        response = requests.head("http://" + site)
 
        return response.status_code // 100 in (2, 3)
    except requests.RequestException:
        return False

def add_suffix(site):
 
    if not re.search(r"\.[a-zA-Z]{2,}$", site):
        return site + ".com"
    return site

def runapp(appname):
    pyautogui.hotkey("win", "r") 
    time.sleep(1)
    pyautogui.typewrite(appname)
    pyautogui.press("enter")
    time.sleep(1)

def open_web(site):
    site = add_suffix(site) 

    if is_valid_website(site):
        print(f"{site} is a valid and existing website.")

    else:
        print(f"{site} is not a valid or existing website.")


open_web("amazon.in")  
open_web("example") 

