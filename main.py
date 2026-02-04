import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys
import pyautogui
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
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except Exception as e:
        return "none"

def run_serra():
    command = take_command()
    print(f"User command: {command}")

    if command == "none":
        return

    # --- AMRI ZA MTANDAONI (BROWSERS) ---
    if 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif 'open chrome' in command:
        speak("Opening Chrome")
        # Kama unataka kufungua app yenyewe ya Chrome:
        webbrowser.open("https://www.google.com")

    elif 'open whatsapp' in command:
        speak("Opening WhatsApp Web")
        webbrowser.open("https://web.whatsapp.com")

    elif 'play' in command:
        song = command.replace('play', '')
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    
    elif 'search' in command:
        item = command.replace('search', '')
        speak(f"Searching {item} on Google")
        pywhatkit.search(item)

    # --- AMRI ZA MFUMO WA PC (SYSTEM) ---
    elif 'open notepad' in command:
        speak("Opening Notepad")
        os.system("notepad")
        
    elif 'close notepad' in command:
        os.system("taskkill /f /im notepad.exe")

    elif 'screenshot' in command:
        image = pyautogui.screenshot()
        image.save("serra_screenshot.png")
        speak("Screenshot saved, Boss.")

    elif 'volume up' in command:
        pyautogui.press("volumeup")

    elif 'volume down' in command:
        pyautogui.press("volumedown")

    # --- AMRI ZA HABARI ---
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}")

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
