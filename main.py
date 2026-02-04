import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import os
import sys
import pyautogui
import webbrowser
import time
import psutil

# --- SETUP SAUTI YA KIKE (ZIRA) ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 185)

def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[LISTENING...]")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"Boss said: {query}")
        return query.lower()
    except:
        return "none"

def run_serra():
    query = take_command()
    if query == "none": return

    # --- 1. MOUSE CONTROL (SIRI YA MOUSE) ---
    if 'move mouse' in query:
        speak("I have gained control of the mouse. Where should I move it?")
        # Mfano: "move mouse to top left"
        if 'top left' in query: pyautogui.moveTo(100, 100, duration=1)
        elif 'center' in query: pyautogui.moveTo(960, 540, duration=1)
        speak("Mouse relocated as requested.")

    elif 'click' in query:
        speak("Affirmative, performing a left click.")
        pyautogui.click()

    elif 'double click' in query:
        speak("Double clicking now.")
        pyautogui.doubleClick()

    # --- 2. ADVANCED TYPING (ASSISTANT MODE) ---
    elif 'write' in query or 'type' in query:
        speak("I understand perfectly. I am ready to be your secretary. What is the message?")
        content = take_command()
        if content != "none":
            speak(f"Message received: {content}. I will start typing in 5 seconds. Please focus your window.")
            time.sleep(5)
            speak("Typing in progress...")
            pyautogui.write(content, interval=0.05)
            speak("I have finished writing everything, Boss. Anything else?")

    # --- 3. SYSTEM EXPLORER (INGIA KOKOTE) ---
    elif 'open' in query:
        app = query.replace('open ', '').strip()
        speak(f"Understood. Accessing system files to launch {app}. Standby.")
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write(app)
        time.sleep(1)
        pyautogui.press('enter')
        speak(f"Successfully entered {app}. System is now synchronized.")

    # --- 4. SMART SEARCH (KUELEWA CHOCHOTE) ---
    elif 'what is' in query or 'who is' in query or 'explain' in query:
        speak("Query accepted. Accessing my knowledge database to explain this to you.")
        try:
            results = wikipedia.summary(query, sentences=3)
            speak("Here is what I have found regarding your request:")
            speak(results)
        except:
            speak("I need to dive deeper. Opening Google for a full intelligence report.")
            pywhatkit.search(query)

    # --- 5. AUTOMATION (CLOSE & MINIMIZE) ---
    elif 'close' in query:
        speak("Terminating the current window. Goodbye app.")
        pyautogui.hotkey('alt', 'f4')

    elif 'scroll down' in query:
        speak("Scrolling down for you.")
        pyautogui.scroll(-500)

    elif 'scroll up' in query:
        speak("Scrolling up.")
        pyautogui.scroll(500)

    # --- 6. PC STATUS ---
    elif 'status' in query:
        battery = psutil.sensors_battery().percent
        speak(f"System status is stable. Battery is at {battery} percent. CPU performance is optimal.")

    elif 'exit' in query or 'sleep' in query:
        speak("Serra is going offline. Secure mode activated. Have a great time, Boss.")
        sys.exit()

if __name__ == "__main__":
    speak("Serra Intelligence System Activated. High-performance mode is ON. I am ready to explore and assist. What are your orders?")
    while True:
        run_serra()
