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
import subprocess
import time
import psutil

# --- ULTRA-PRO SETUP ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# CHAGUA SAUTI YA KIKE
# Kwenye Windows nyingi, voices[1] ndio David (Kiume) na voices[0] au [1] ni Zira (Kike).
# Ikishindwa, itatumia iliyopo.
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 190)  # Kasi ya sauti (Natural speed)
engine.setProperty('volume', 1.0) # Sauti iwe juu kabisa

def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[SERRA IS LISTENING...]")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        print("[ANALYZING...]")
        query = r.recognize_google(audio, language='en-in')
        print(f"User Request: {query}\n")
        return query.lower()
    except:
        return "none"

def run_serra():
    query = take_command()
    if query == "none": return

    # --- 1. SMART APP OPENER (PRO LEVEL) ---
    if 'open' in query:
        app_name = query.replace('open ', '').strip()
        speak(f"Searching for {app_name} in your system, Boss.")
        try:
            # Hii inafungua app yoyote hata kama haiko kwenye PATH
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(app_name)
            time.sleep(0.5)
            pyautogui.press('enter')
            speak(f"I have launched {app_name} for you.")
        except Exception as e:
            speak("I couldn't find the application, should I search for it on Google?")

    # --- 2. AI TYPING ASSISTANT (ANDIKA CHOCHOTE) ---
    elif 'type' in query or 'write' in query:
        speak("Ready to type. Please tell me the content, Boss.")
        content = take_command()
        if content != "none":
            speak("Starting to type in 3 seconds. Place your cursor where you want the text.")
            time.sleep(3)
            pyautogui.write(content, interval=0.02)
            speak("Content has been written successfully.")

    # --- 3. SYSTEM BRAIN (PC STATUS) ---
    elif 'battery' in query:
        battery = psutil.sensors_battery()
        speak(f"Your system has {battery.percent} percent battery remaining.")

    elif 'cpu' in query:
        usage = str(psutil.cpu_percent())
        speak(f"Your CPU is currently at {usage} percent usage.")

    # --- 4. WEB & KNOWLEDGE ---
    elif 'search' in query:
        search_query = query.replace('search', '')
        speak(f"Scanning the web for {search_query}...")
        pywhatkit.search(search_query)

    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Playing {song} on YouTube. Enjoy!")
        pywhatkit.playonyt(song)

    elif 'who is' in query or 'what is' in query:
        speak("Searching intelligence databases...")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak(results)
        except:
            speak("I couldn't find a direct answer. Let me search on Google for you.")
            pywhatkit.search(query)

    # --- 5. CONTROL & AUTOMATION ---
    elif 'screenshot' in query:
        speak("Capturing screen...")
        name = f"screenshot_{datetime.datetime.now().hour}{datetime.datetime.now().minute}.png"
        pyautogui.screenshot(name)
        speak(f"Snapshot saved as {name}.")

    elif 'volume up' in query:
        for _ in range(10): pyautogui.press("volumeup")
        speak("Volume increased.")

    elif 'volume down' in query:
        for _ in range(10): pyautogui.press("volumedown")

    elif 'minimize all' in query:
        pyautogui.hotkey('win', 'd')
        speak("Desktop cleared.")

    # --- 6. OFFLINE ---
    elif 'go to sleep' in query or 'exit' in query:
        speak("System going to sleep mode. Call me when you need me. Goodbye!")
        sys.exit()

if __name__ == "__main__":
    hour = int(datetime.datetime.now().hour)
    if hour < 12: speak("Good morning, Boss.")
    elif 12 <= hour < 18: speak("Good afternoon, Boss.")
    else: speak("Good evening, Boss.")
    
    speak("Serra Ultra-Pro is active. I am now using my high-performance female voice. How can I serve you?")
    
    while True:
        run_serra()
