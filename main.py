import tkinter as tk
from tkinter import scrolledtext
from ttkthemes import ThemedTk
from tkinter import ttk
from PIL import Image, ImageTk
from process_res import *
from speak import *
from dflow import *
from process_res import *

class PyBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.set_theme("default")  # Use the default dark theme
        self.master.title("PyBot Chat")
        self.master.geometry("600x400")  # Set the initial size of the window

        self.speaker_enabled = True  # Flag to track whether the speaker is enabled

        # Create a frame to hold the chat history with a border
        self.chat_frame = tk.Frame(master, relief=tk.GROOVE, borderwidth=2, bg='#333')  # Set the background color to dark
        self.chat_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Create and configure the chat history display with message bubbles
        self.chat_history = scrolledtext.ScrolledText(
            self.chat_frame, wrap=tk.WORD, width=50, height=15, font=("Helvetica", 12), bg='#333', fg='white', state=tk.DISABLED
        )  # Set the background color to dark and text color to white, make it read-only
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)

        # Create and configure the entry for user input with a larger font
        self.user_input = tk.Entry(master, width=40, font=("Helvetica", 14), bg='#333', fg='white')  # Set the background color to dark and text color to white
        self.user_input.grid(row=1, column=0, padx=10, pady=10, sticky="ew", columnspan=3)
        self.user_input.bind("<Key>", self.disable_entry_delete)  # Disable the ability to delete text
        self.user_input.bind("<Return>", lambda event: self.send_message())  # Bind the Enter key to send the message

        # Create the send button with a more vibrant color
        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        self.send_button.grid(row=1, column=3, padx=10, pady=10, sticky="ew")

        # Load the speaker and muted icons
        self.speaker_icon = ImageTk.PhotoImage(Image.open("resources/speaker_icon.png").resize((30, 30)))
        self.muted_icon = ImageTk.PhotoImage(Image.open("resources/muted_icon.png").resize((30, 30)))

        # Create the speaker button with the speaker icon
        self.speaker_button = tk.Button(master, image=self.speaker_icon, command=self.toggle_speaker, bg="#4CAF50", bd=0)
        self.speaker_button.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        # Configure row and column weights to make the chat frame expandable
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=1)
        master.columnconfigure(3, weight=0)  # Set weight to 0 to prevent the speaker button from expanding

        master.rowconfigure(0, weight=1)
        master.rowconfigure(1, weight=0)  # Set weight to 0 to prevent the user input and send button from expanding

        # Initialize the chat history with a welcome message
        self.display_message("PyBot: Welcome to PyBot Chat!\n")

    def send_message(self):
        # Get user input
        user_message = self.user_input.get()

        if user_message:
            # Display user message in the chat history
            self.display_message("You: " + user_message)

            # TODO: Process the user message with your chatbot logic here
            # For simplicity, let's just echo the user's message as the bot's response
            token = process(user_message)
                
            if token == False:
                bot_response = get_res(user_message)
                self.display_message(bot_response)
            else:
                self.display_message(token)


            # Clear the user input
            self.user_input.delete(0, tk.END)

            # If the speaker is enabled, speak the bot's response
            if self.speaker_enabled:
                self.speak(bot_response)

    def display_message(self, message):
        # Make the chat history writable temporarily to insert a new message
        self.chat_history.config(state=tk.NORMAL)
        # Insert a message into the chat history with a message bubble appearance
        self.chat_history.insert(tk.END, message + "\n", "message")
        # Disable the chat history to make it read-only again
        self.chat_history.config(state=tk.DISABLED)

        # Automatically scroll to the bottom to show the latest messages
        self.chat_history.yview(tk.END)


    def disable_entry_delete(self, event):
        # Disable the ability to delete text in the entry widget
        if event.keysym == 'Delete' or event.keysym == "Backspace":
            return 'break'


    def toggle_speaker(self):
        # Toggle the speaker functionality on and off
        self.speaker_enabled = not self.speaker_enabled

        # Update the speaker button image based on the toggle state
        if self.speaker_enabled:
            self.speaker_button.configure(image=self.speaker_icon)
        else:
            self.speaker_button.configure(image=self.muted_icon)

    def speak(self, text):
        # Add your text-to-speech implementation here
        if self.speaker_enabled == True:
            TTS(text)
        else:
            pass

def main():
    root = ThemedTk()  # Use ThemedTk from ttkthemes with the default dark theme
    pybot_gui = PyBotGUI(root)

    # Configure the appearance of the message bubbles
    root.option_add('*msg.message', {
        'background': '#333',  # Set the background color to dark
        'borderwidth': 1,
        'relief': 'solid',
        'wraplength': 300,
        'justify': 'left',
        'padding': 5,
        'foreground': 'white',  # Set the text color to white
    })

    root.mainloop()
    
if __name__ == "__main__":
    main()