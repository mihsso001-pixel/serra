import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys
import pyautogui
import subprocess
import webbrowser

# SETUP
engine = pyttsx3.init()
def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Serra is listening...")
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except:
        return "none"

def run_serra():
    command = take_command()
    print(f"User command: {command}")

    # --- AMRI ZA MTANDAONI ---
    if 'play' in command:
        song = command.replace('play', '')
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    
    elif 'search' in command:
        item = command.replace('search', '')
        speak(f"Searching {item} on Google")
        pywhatkit.search(item)

    # --- AMRI ZA MFUMO WA PC (SYSTEM) ---
    elif 'open notepad' in command:
        os.system("notepad")
        
    elif 'close notepad' in command:
        os.system("taskkill /f /im notepad.exe")

    elif 'screenshot' in command:
        image = pyautogui.screenshot()
        image.save("serra_screenshot.png")
        speak("Screenshot saved, Boss.")

    elif 'shutdown' in command:
        speak("Shutting down the computer in 10 seconds")
        os.system("shutdown /s /t 10")

    elif 'restart' in command:
        os.system("shutdown /r /t 10")

    elif 'volume up' in command:
        pyautogui.press("volumeup")

    elif 'volume down' in command:
        pyautogui.press("volumedown")

    elif 'mute' in command:
        pyautogui.press("volumemute")

    # --- AMRI ZA MAISHA NA HABARI ---
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time}")

    elif 'who is' in command:
        person = command.replace('who is', '')
        speak(wikipedia.summary(person, 1))

    elif 'joke' in command:
        speak(pyjokes.get_joke())

    elif 'exit' in command or 'stop' in command:
        speak("Serra system offline. Goodbye!")
        sys.exit()

if __name__ == "__main__":
    speak("Serra Full System Online. Waiting for your orders.")
    while True:
        run_serra()
