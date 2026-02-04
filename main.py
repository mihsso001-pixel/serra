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

# --- CONFIGURATION YA GEMINI (KEY MPYA KUTOKA KWENYE PICHA) ---
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SETUP SAUTI YA KIKE ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 190)

def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

def ask_gemini(prompt):
    try:
        response = model.generate_content(f"You are Serra, a pro AI assistant. Keep it short: {prompt}")
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "My cloud brain is still warming up, but I can help you with PC commands."

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[LISTENING...]")
        r.pause_threshold = 0.8
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"Boss: {query}")
        return query.lower()
    except:
        return "none"

def run_serra():
    query = take_command()
    if query == "none": return

    # 1. KUELEWA CHOCHOTE (GEMINI POWER)
    if 'who' in query or 'what' in query or 'tell me' in query or 'how' in query:
        speak("Let me think...")
        answer = ask_gemini(query)
        speak(answer)

    # 2. KUANDIKA (SECRETARY MODE)
    elif 'type' in query or 'write' in query:
        speak("I'm ready. What should I write?")
        content = take_command()
        if content != "none":
            speak("Typing in 5 seconds. Focus your window.")
            time.sleep(5)
            pyautogui.write(content, interval=0.05)
            speak("Done writing, Boss.")

    # 3. KUFUNGUA APP (INGIA KOKOTE)
    elif 'open' in query:
        app = query.replace('open ', '').strip()
        speak(f"Launching {app} immediately.")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(app)
        time.sleep(0.5)
        pyautogui.press('enter')

    # 4. YOUTUBE
    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Playing {song} on YouTube. Enjoy!")
        pywhatkit.playonyt(song)

    # 5. CONTROL & EXIT
    elif 'status' in query:
        battery = psutil.sensors_battery().percent
        speak(f"Battery is at {battery} percent. System is healthy.")

    elif 'exit' in query or 'sleep' in query:
        speak("Goodbye Boss! Serra is going offline.")
        sys.exit()

if __name__ == "__main__":
    speak("Serra Ultra-Pro is now fully synchronized with Gemini. My brain is online. How can I serve you?")
    while True:
        run_serra()
