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

# --- CONFIGURATION YA GEMINI ---
API_KEY = "AIzaSyBlxCHYr2nriXeLsI969JcylU9EbmW_VT4"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash') # Toleo la kasi zaidi

# --- SETUP SAUTI (FEMALE PRO) ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Tafuta sauti ya kike (Zira), kama haipo tumia iliyopo
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
        print("\n[SERRA IS LISTENING...]")
        r.pause_threshold = 0.8
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        print("[PROCESSING...]")
        query = r.recognize_google(audio, language='en-in')
        print(f"Boss: {query}")
        return query.lower()
    except:
        return "none"

def ask_gemini(prompt):
    """Inatumia akili ya Gemini kujibu maswali magumu"""
    try:
        response = model.generate_content(f"Keep the answer short and professional for a voice assistant: {prompt}")
        return response.text
    except Exception as e:
        return "I am having trouble connecting to my brain, but I can still perform PC tasks."

def run_serra():
    query = take_command()
    if query == "none": return

    # 1. SMART TYPING (SECRETARY MODE)
    if 'write' in query or 'type' in query:
        speak("Ready to take dictation. What exactly should I type for you, Boss?")
        content = take_command()
        if content != "none":
            speak("Understood. I'll start typing in 5 seconds. Place your cursor in the document.")
            time.sleep(5)
            pyautogui.write(content, interval=0.03)
            speak("Done! I've typed it out as you requested.")

    # 2. APP CONTROL & NAVIGATION
    elif 'open' in query:
        app = query.replace('open ', '').strip()
        speak(f"Searching and launching {app} now.")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app)
        time.sleep(0.5)
        pyautogui.press('enter')

    # 3. MOUSE CONTROL (PRO)
    elif 'click' in query:
        speak("Clicking now.")
        pyautogui.click()
        
    elif 'scroll down' in query:
        speak("Scrolling down.")
        pyautogui.scroll(-800)

    # 4. YOUTUBE (SMART PLAY)
    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Opening YouTube to play {song}. Sit back and relax.")
        pywhatkit.playonyt(song)

    # 5. SYSTEM STATUS
    elif 'system status' in query or 'pc status' in query:
        battery = psutil.sensors_battery().percent
        cpu = psutil.cpu_percent()
        speak(f"Boss, your battery is at {battery} percent, and CPU usage is at {cpu} percent. Everything looks stable.")

    # 6. SHUTDOWN/RESTART
    elif 'shutdown' in query:
        speak("System will shutdown in 10 seconds. Goodbye Boss.")
        os.system("shutdown /s /t 10")
        
    elif 'screenshot' in query:
        speak("Taking a snapshot.")
        pyautogui.screenshot("serra_capture.png")

    # 7. CHAT & KNOWLEDGE (GEMINI BRAIN)
    else:
        # Hapa sasa ndipo Gemini anafanya kazi yake ya kujibu lolote
        answer = ask_gemini(query)
        speak(answer)

if __name__ == "__main__":
    hour = int(datetime.datetime.now().hour)
    if hour < 12: speak("Good morning, Boss.")
    elif 12 <= hour < 18: speak("Good afternoon, Boss.")
    else: speak("Good evening, Boss.")
    
    speak("Serra Intelligence is synchronized with Gemini. I am now your most powerful tool. How can I help you today?")
    
    while True:
        run_serra()
