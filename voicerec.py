import os
import time
import pocketsphinx
import speech_recognition as sr

# Command function
def handle_command(command):
    command = command.lower()
    if "play" in command:
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
                  "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play")
    elif "pause" in command:
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
                  "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause")
    elif "next" in command:
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
                  "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")
    elif "previous" in command:
        os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
                  "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")
    else:
        print("Command not recognized.")

# Voice loop
recognizer = sr.Recognizer()
mic = sr.Microphone()

with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening for command...")

    while True:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_sphinx(audio)
            print(f"You said: {command}")
            handle_command(command)
        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Recognition error: {e}")
