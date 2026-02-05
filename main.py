import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time
import os
import webbrowser
import pyautogui
import psutil
import datetime
import pywhatkit
import math
import random

# ==========================================================
# 1. CORE BRAIN CONFIGURATION
# ==========================================================
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Voice Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for v in voices:
    if "Zira" in v.name or "EN-US" in v.name:
        engine.setProperty('voice', v.id)
        break
engine.setProperty('rate', 185)

# ==========================================================
# 2. SERRA SENTIENT UI
# ==========================================================
class SerraSentient(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SERRA AI - SENTIENT SYSTEM")
        self.geometry("500x700")
        self.attributes("-topmost", True)
        self.config(bg='#020205')
        
        self.active = False
        self.speaking = False
        self.angle = 0

        # UI Header
        self.header = ctk.CTkLabel(self, text="SERRA AI", font=("Impact", 65), text_color="#00f2ff")
        self.header.pack(pady=(40, 5))

        self.sub = ctk.CTkLabel(self, text="COGNITIVE INTERFACE ONLINE", font=("Consolas", 12), text_color="#005566")
        self.sub.pack()

        # Visualizer Canvas
        self.canvas = ctk.CTkCanvas(self, width=400, height=350, bg='#020205', highlightthickness=0)
        self.canvas.pack()
        
        # Orb & Pulse Waves
        self.orb = self.canvas.create_oval(100, 60, 300, 260, outline="#00f2ff", width=2)
        self.wave = self.canvas.create_line(100, 160, 300, 160, fill="#00f2ff", width=4, smooth=True)

        self.status = ctk.CTkLabel(self, text="CORE SLEEPING", font=("Consolas", 14), text_color="#333")
        self.status.pack(pady=20)

        # Main Activation Button
        self.main_btn = ctk.CTkButton(self, text="WAKE UP SERRA", font=("Segoe UI", 22, "bold"), 
                                       command=self.toggle_system, fg_color="#008080", 
                                       hover_color="#00f2ff", height=65, corner_radius=15)
        self.main_btn.pack(pady=10, fill="x", padx=60)

        self.animate_loop()

    def animate_loop(self):
        self.angle += 0.12
        if self.active:
            pulse = (math.sin(self.angle) * 12)
            color = "#ff007f" if self.speaking else "#00f2ff"
            self.canvas.itemconfig(self.orb, outline=color)
            
            amp = 65 if self.speaking else 8
            y_shift = math.sin(self.angle * 15) * amp
            self.canvas.coords(self.wave, 110, 160+y_shift, 200, 160-y_shift, 290, 160+y_shift)
            self.canvas.itemconfig(self.wave, fill=color)
        else:
            self.canvas.itemconfig(self.orb, outline="#111")
            self.canvas.itemconfig(self.wave, fill="#111")
        self.after(25, self.animate_loop)

    def speak(self, text):
        self.speaking = True
        print(f"Serra: {text}")
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def toggle_system(self):
        if not self.active:
            self.active = True
            self.status.configure(text="LISTENING...", text_color="#00f2ff")
            self.main_btn.configure(text="GO TO SLEEP", fg_color="#550000")
            threading.Thread(target=self.brain_loop, daemon=True).start()
            self.speak("System initialized. I am online and ready for your commands.")
        else:
            self.active = False
            self.status.configure(text="CORE SLEEPING", text_color="#333")
            self.main_btn.configure(text="WAKE UP SERRA", fg_color="#008080")

    def brain_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.6
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    self.process_command(query)
                except: continue

    def process_command(self, query):
        print(f"User said: {query}")

        # --- 1. IDENTITY & HISTORY ---
        if any(word in query for word in ['who are you', 'your name', 'history', 'background']):
            identity_msg = ("I am Serra AI, a highly advanced artificial intelligence system designed "
                            "for total system control and high-level reasoning. I was created to be "
                            "your ultimate digital companion, merging the power of local system commands "
                            "with the vast intelligence of neural networks.")
            self.speak(identity_msg)

        # --- 2. VERBAL RESPONSES FOR ACTIONS ---
        elif 'calculator' in query:
            responses = ["Sure, launching the calculator now.", "Opening calculator for you.", "Executing calculator."]
            self.speak(random.choice(responses))
            os.system("calc")

        elif 'notepad' in query:
            self.speak("Opening Notepad. You can start typing now.")
            os.system("notepad")

        elif 'search' in query:
            item = query.replace("search", "").strip()
            self.speak(f"Searching the web for {item}. Please wait.")
            webbrowser.open(f"https://www.google.com/search?q={item}")

        elif 'open' in query:
            app = query.replace("open", "").strip()
            self.speak(f"Understood. Opening {app} for you.")
            pyautogui.press('win')
            time.sleep(0.3)
            pyautogui.write(app)
            time.sleep(0.5)
            pyautogui.press('enter')

        # --- 3. TYPING & CLOSE COMMANDS ---
        elif 'type' in query or 'write' in query:
            msg = query.replace("type", "").replace("write", "").strip()
            self.speak(f"Writing your message: {msg}")
            pyautogui.write(msg, interval=0.02)
            pyautogui.press('enter')

        elif 'close' in query:
            app = query.replace("close", "").strip()
            self.speak(f"Terminating the application {app}.")
            os.system(f"taskkill /f /im {app}.exe")
            pyautogui.hotkey('alt', 'f4')

        # --- 4. SYSTEM STATUS & CONTROL ---
        elif 'battery' in query:
            self.speak(f"Sir, your battery is currently at {psutil.sensors_battery().percent} percent.")
            
        elif 'volume' in query:
            if 'up' in query: pyautogui.press("volumeup", presses=5); self.speak("Volume up.")
            elif 'down' in query: pyautogui.press("volumedown", presses=5); self.speak("Volume down.")

        # --- 5. THE BIG BRAIN (GEMINI) ---
        else:
            try:
                self.status.configure(text="THINKING...", text_color="#ff007f")
                # Tunamwambia Gemini awe Serra na ajibu kitalaamu
                response = model.generate_content(f"Roleplay: You are Serra AI. User asked: {query}. Respond naturally as a sentient AI.")
                self.speak(response.text)
                self.status.configure(text="LISTENING...", text_color="#00f2ff")
            except:
                self.speak("My neural connection is unstable, but my local protocols are functioning.")

if __name__ == "__main__":
    SerraSentient().mainloop()
