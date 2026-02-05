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
import google.generativeai as genai

# --- CONFIGURATION ---
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)

# --- SETUP SAUTI YA MDADA (SMOOTH & CLEAR) ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break

engine.setProperty('rate', 160) # Kasi tulivu sana
engine.setProperty('volume', 1.0)

def speak(text):
    # Kusafisha maandishi (kutoa alama za ajabu kwa sauti bora)
    clean_text = text.replace('*', '').replace('#', '')
    print(f"Serra: {clean_text}")
    engine.say(clean_text)
    engine.runAndWait()

def get_working_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        return genai.GenerativeModel('gemini-pro')

serra_brain = get_working_model()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[SERRA IS LISTENING...]")
        r.pause_threshold = 1.0
        r.adjust_for_ambient_noise(source, duration=0.8)
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
        return query.lower()
    except:
        return ""

def execute_action(query):
    # 1. IDENTITY
    if 'your name' in query or 'who are you' in query:
        speak("I am Serra AI, your highly advanced personal assistant. I can control your PC and answer any question you have.")
        return

    # 2. MASTER APP OPENER (Hii inafungua Apps mamilioni)
    elif 'open' in query:
        target = query.replace('open ', '').strip()
        speak(f"Accessing {target} for you.")
        if 'google' in target or 'youtube' in target or '.' in target:
            url = target if '.' in target else f"{target}.com"
            webbrowser.open(url)
        else:
            # Inatafuta app yoyote kwenye Windows
            pyautogui.press('win')
            time.sleep(0.5)
            pyautogui.write(target)
            time.sleep(1)
            pyautogui.press('enter')
        return

    # 3. YOUTUBE AUTOMATION
    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Playing {song} on YouTube in full screen mode.")
        pywhatkit.playonyt(song)
        time.sleep(7)
        pyautogui.press('f')
        return

    # 4. SECRETARY MODE (Kuandika chochote)
    elif 'type' in query or 'write' in query:
        speak("I am ready. Tell me the content.")
        content = take_command()
        if content:
            speak("Understood. I'll start typing in 5 seconds.")
            time.sleep(5)
            pyautogui.write(content, interval=0.05)
            speak("Done writing, Boss.")
        return

    # 5. PC CONTROL (Mamilioni ya amri za mfumo)
    elif 'time' in query:
        speak(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}")
        return
    elif 'screenshot' in query:
        pyautogui.screenshot(f"Serra_Shot_{int(time.time())}.png")
        speak("Screenshot taken and saved.")
        return
    elif 'volume up' in query:
        pyautogui.press("volumeup", presses=5)
        speak("Volume increased.")
        return
    elif 'minimize' in query:
        pyautogui.hotkey('win', 'd')
        speak("Minimizing all windows.")
        return

    # 6. UNLIMITED KNOWLEDGE (GEMINI AI)
    # Hapa ndipo "Mamilioni" ya majibu yanapotoka
    if len(query) > 0:
        speak("Processing your request...")
        try:
            # Gemini anapewa maelekezo ya kuwa Serra AI
            response = serra_brain.generate_content(
                f"Your name is Serra AI. Be very helpful, professional and concise. Answer in the language the user used: {query}"
            )
            speak(response.text)
        except:
            speak("I am connected, but I hit a small snag. Can you repeat that?")

if __name__ == "__main__":
    speak("Serra AI Pro System initialized. I am ready to handle your PC and all your questions.")
    
    while True:
        command = take_command()
        if not command:
            continue
            
        if 'exit' in command or 'stop' in command or 'goodbye' in command:
            speak("Going to sleep now. See you later, Boss!")
            sys.exit()
            
        execute_action(command)
