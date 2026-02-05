import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import os
import sys
import pyautogui
import webbrowser
import time
import psutil
import wikipedia
import google.generativeai as genai

# --- CONFIGURATION ---
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = "Your name is Serra AI. You are a professional female assistant. Always identify as Serra AI. Keep answers concise."

# SETUP SAUTI
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 165)

def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

# Model Selection
model = genai.GenerativeModel('gemini-1.5-flash')

def ask_gemini(prompt):
    try:
        full_prompt = f"{SYSTEM_PROMPT} User asks: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except:
        return "I'm having trouble connecting to my cloud brain, but I can still help with PC tasks."

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[SERRA IS LISTENING...]")
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1.0
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=8)
            query = r.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
        except:
            return ""

def execute_action(query):
    # 1. IDENTITY & TIME
    if 'name' in query or 'who are you' in query:
        speak("I am Serra AI, your dedicated assistant. How can I make your life easier today?")
    
    elif 'time' in query:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time_now}")

    # 2. WHATSAPP & MESSAGING
    elif 'send message' in query or 'whatsapp' in query:
        speak("Who should I message? Please tell me the number.")
        number = take_command().replace(" ", "")
        speak("What is the message?")
        msg = take_command()
        if number and msg:
            speak(f"Sending message to {number}")
            pywhatkit.sendwhatmsg_instantly(f"+{number}", msg)
            time.sleep(5)
            pyautogui.press('enter')

    # 3. INTERNET & SEARCH
    elif 'search' in query or 'google' in query:
        search_query = query.replace("search", "").replace("google", "")
        speak(f"Searching for {search_query} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    elif 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)

    # 4. SYSTEM CONTROL (HP Laptop Specials)
    elif 'battery' in query:
        battery = psutil.sensors_battery()
        speak(f"Your battery is at {battery.percent} percent.")

    elif 'minimize' in query or 'desktop' in query:
        speak("Minimizing windows.")
        pyautogui.hotkey('win', 'd')

    elif 'screenshot' in query:
        speak("Taking a screenshot.")
        img = pyautogui.screenshot()
        img.save("serra_screenshot.png")
        speak("Screenshot saved to your folder.")

    elif 'shutdown' in query:
        speak("Shutting down the system in 10 seconds. Save your work.")
        time.sleep(10)
        os.system("shutdown /s /t 1")

    # 5. OPEN APPS (Universal)
    elif 'open' in query:
        target = query.replace('open ', '').strip()
        speak(f"Launching {target}")
        pyautogui.press('win')
        time.sleep(0.5)
        pyautogui.write(target)
        time.sleep(1)
        pyautogui.press('enter')

    # 6. ENTERTAINMENT
    elif 'play' in query:
        song = query.replace('play', '')
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
        time.sleep(5)
        pyautogui.press('f') # Full screen

    # 7. CHAT (If no command matches)
    elif len(query) > 3:
        answer = ask_gemini(query)
        speak(answer)

if __name__ == "__main__":
    speak("Serra AI Pro is fully loaded with advanced commands. How can I help you, Boss?")
    while True:
        cmd = take_command()
        if 'exit' in cmd or 'sleep' in cmd or 'stop' in cmd:
            speak("Goodbye Boss! Serra is going offline.")
            break
        if cmd:
            execute_action(cmd)
