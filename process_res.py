import pandas as pd
from nltk import word_tokenize
import wikipedia
import requests
import re
import subprocess

# Download the 'punkt' resource
# nltk.download('punkt')

app_names = {
    "chrome": "Google Chrome",
    "firefox": "Mozilla Firefox",
    "notepad": "Notepad",
    "calculator": "Calculator",
    "spotify": "Spotify"
}

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

def match_app_name(partial_input):
    for key, value in app_names.items():
        if partial_input.lower() in key.lower():
            return value

    return None

def clean_user_input(user_input):
    prefixes_to_remove = ["run ", "start ", "open "]
    for prefix in prefixes_to_remove:
        if user_input.lower().startswith(prefix):
            user_input = user_input[len(prefix):].strip()
            break

    return user_input

def open_web_or_app(user_input):
    user_input = clean_user_input(user_input)
    matched_app_name = match_app_name(user_input)
    user_input = add_suffix(user_input)
    if matched_app_name:
        runapp(matched_app_name)

    elif is_valid_website(user_input):
        print(f"{user_input} is a valid and existing website.")
        # Open the website using a web browser
        subprocess.Popen(["start", "http://" + user_input], shell=True)

    else:
        print(f"{user_input} is not a valid or existing website or app.")


# Sample data
data = {'Query': ["What is the capital of France?", "Python programming language", "How does photosynthesis work?", "Tell me a joke", "should we go for a run?"]}
df = pd.DataFrame(data)

# Function to detect if a query is a question
def is_question(query):
    words = word_tokenize(query)
    # Check if the first word is a question word
    question_words = ['what', 'who',]
    return words[0].lower() in question_words

def get_first_word(input_string):
    words = input_string.split()
    if words:
        return words[0]
    else:
        return None

def process(query_text):

    if get_first_word(query_text) == "run" or get_first_word(query_text) == "start" or get_first_word(query_text) == "open":
        open_web_or_app(query_text)
        return("Okay")

    if is_question(query_text):
        query_text = query_text.replace("what is", "")
        query_text = query_text.replace("what is the", "")
        query_text = query_text.replace("what are", "")
        query_text = query_text.replace("who is", "")
        query_text = query_text.replace("who are", "")
        return(wikipedia.summary(query_text, sentences=2))
    else:
        return(False)
