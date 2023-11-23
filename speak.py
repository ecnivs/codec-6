import pyttsx3
from time import sleep

# Set Voice
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    engine.setProperty('voice',voices[0].id)

def TTS(audio): # Voice Output
    sleep(0.1)
    engine.say(audio)
    engine.runAndWait()