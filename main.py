import tkinter as tk
from tkinter import scrolledtext
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import speech_recognition as sr
from process_res import *
from speak import *
from dflow import *
from process_res import *

class PyBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.set_theme("arc")  # Change the theme to 'arc'
        self.master.title("PyBot Chat")
        self.master.geometry("800x600")

        self.speaker_enabled = True

        self.chat_frame = tk.Frame(master, relief=tk.GROOVE, borderwidth=2, bg='#282c34')  # Dark background
        self.chat_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        self.chat_history = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, width=80, height=25, font=("Arial", 12), bg='#282c34', fg='#b4b4b4', state=tk.DISABLED  # Adjust font and colors
        )
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)

        self.user_input = tk.Entry(master, width=40, font=("Arial", 14), bg='#282c34', fg='#34b7f1')  # Adjust font and colors
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=2)
        self.user_input.bind("<Key>", self.disable_entry_delete)
        self.user_input.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#34b7f1", fg="white", font=("Arial", 12, 'bold'))  # Blue color for the Send button
        self.send_button.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.voice_button = tk.Button(master, text="Voice", command=self.start_voice_input, bg="#34b7f1", fg="white", font=("Arial", 12, 'bold'))  # Blue color for the Voice button
        self.voice_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        self.speaker_icon = ImageTk.PhotoImage(Image.open("resources/speaker_icon.png").resize((30, 30)))
        self.muted_icon = ImageTk.PhotoImage(Image.open("resources/muted_icon.png").resize((30, 30)))

        self.speaker_button = tk.Button(master, image=self.speaker_icon, command=self.toggle_speaker, bg="#34b7f1", bd=0)  # Blue color for the speaker button
        self.speaker_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=0)

        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=0)

        self.display_message("PyBot: Welcome to PyBot Chat!\n")

        # Initialize SpeechRecognition
        self.recognizer = sr.Recognizer()

    def send_message(self):
        user_message = self.user_input.get()

        if user_message:
            self.display_message("You: " + user_message, user=True)

            token = process(user_message)

            if token == False:
                bot_response = get_res(user_message)
                self.display_message(bot_response)
            else:
                self.display_message(token)

            self.user_input.delete(0, tk.END)

            if self.speaker_enabled:
                self.speak(bot_response)

    def start_voice_input(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.display_message("PyBot: Listening for voice input...", user=False)

                audio = self.recognizer.listen(source, timeout=5)

                self.display_message("PyBot: Processing voice input...", user=False)

                user_message = self.recognizer.recognize_google(audio)
                self.display_message("You (Voice): " + user_message, user=True)

                token = process(user_message)

                if token == False:
                    bot_response = get_res(user_message)
                    self.display_message(bot_response)
                else:
                    self.display_message(token)

                if self.speaker_enabled:
                    self.speak(bot_response)

        except sr.UnknownValueError:
            self.display_message("PyBot: Sorry, I could not understand the voice input.", user=False)
        except sr.RequestError as e:
            self.display_message(f"PyBot: Error with the voice recognition service: {e}", user=False)

    def display_message(self, message, user=False):
        self.chat_history.config(state=tk.NORMAL)
        if user:
            self.chat_history.insert(tk.END, message + "\n", "user_message")
        else:
            self.chat_history.insert(tk.END, message + "\n", "bot_message")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview(tk.END)

    def disable_entry_delete(self, event):
        if event.keysym == 'Delete':
            return 'break'

    def toggle_speaker(self):
        self.speaker_enabled = not self.speaker_enabled
        if self.speaker_enabled:
            self.speaker_button.configure(image=self.speaker_icon)
        else:
            self.speaker_button.configure(image=self.muted_icon)

    def speak(self, text):
        if self.speaker_enabled == True:
            TTS(text)
        else:
            pass

def main():
    root = ThemedTk()
    pybot_gui = PyBotGUI(root)

    root.option_add('*msg.message', {
        'background': '#282c34',
        'borderwidth': 1,
        'relief': 'solid',
        'wraplength': 700,
        'justify': 'left',
        'padding': 5,
        'foreground': '#b4b4b4',
    })

    root.option_add('*user_message.TButton', {'font': ('Arial', 12, 'bold'), 'foreground': '#34b7f1', 'background': '#282c34'})  # Blue for user messages
    root.option_add('*bot_message.TButton', {'font': ('Arial', 12, 'bold'), 'foreground': '#34b7f1', 'background': '#282c34'})  # Green for PyBot messages

    root.mainloop()

if __name__ == "__main__":
    main()
