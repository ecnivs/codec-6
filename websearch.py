import pyautogui
import time
import requests
import re
import subprocess

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
    try:
        subprocess.Popen(appname)
        print(f"{appname} is opened.")
    except FileNotFoundError:
        print(f"{appname} not found.")

def open_web_or_app(user_input):
    user_input = add_suffix(user_input)

    if is_valid_website(user_input):
        print(f"{user_input} is a valid and existing website.")
        # Open the website using a web browser
        subprocess.Popen(["start", "http://" + user_input], shell=True)
    else:
        print(f"{user_input} is not a valid or existing website.")
        # Assuming user_input is an app, try to open it
        runapp(user_input)

# Example usage:
user_input = input("Enter the website or app name: ")
open_web_or_app(user_input)
