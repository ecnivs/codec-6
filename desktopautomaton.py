import pyautogui
import time
import requests
import re

def is_valid_website(site):
    try:
        response = requests.head("http://" + site)
        # Check if the response status code is a success (2xx) or a redirection (3xx)
        return response.status_code // 100 in (2, 3)
    except requests.RequestException:
        return False

def add_suffix(site):
    # If the site doesn't have a valid suffix, add ".com"
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
    site = add_suffix(site)  # Add ".com" if no valid suffix is present

    if is_valid_website(site):
        print(f"{site} is a valid and existing website.")
        # You can add additional logic here if needed
    else:
        print(f"{site} is not a valid or existing website.")

# Examples
open_web("amazon.in")  # This will print that "facebook.com" is not a valid or existing website.
open_web("example")    # This will print that "example.com" is a valid and existing website.

