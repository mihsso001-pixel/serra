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
import subprocess
import ctypes
import pyperclip # pip install pyperclip

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
engine.setProperty('rate', 200)

# ==========================================================
# 2. SERRA ULTIMATE INTERFACE (NEON BEAST)
# ==========================================================
class SerraMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("SERRA AI - ABSOLUTE CONTROL")
        self.geometry("500x750")
        self.attributes("-topmost", True)
        self.config(bg='#020205')
        
        self.active = False
        self.speaking = False
        self.angle = 0

        # UI Header
        self.header = ctk.CTkLabel(self, text="SERRA", font=("Impact", 80), text_color="#00f2ff")
        self.header.pack(pady=(40, 0))

        # Visualizer Canvas
        self.canvas = ctk.CTkCanvas(self, width=400, height=350, bg='#020205', highlightthickness=0)
        self.canvas.pack()
        
        # Orbital Rings (Glow Effect)
        self.canvas.create_oval(80, 40, 320, 280, outline="#001a1a", width=2)
        self.orb = self.canvas.create_oval(100, 60, 300, 260, outline="#00f2ff", width=3)
        self.wave = self.canvas.create_line(100, 160, 300, 160, fill="#00f2ff", width=4, smooth=True)

        self.status = ctk.CTkLabel(self, text="NEURAL LINK DISCONNECTED", font=("Consolas", 14), text_color="#222")
        self.status.pack(pady=20)

        # Control Center
        self.main_btn = ctk.CTkButton(self, text="INITIALIZE CORE", font=("Segoe UI", 25, "bold"), 
                                       command=self.toggle_system, fg_color="#008080", 
                                       hover_color="#00f2ff", height=70, corner_radius=15)
        self.main_btn.pack(pady=10, fill="x", padx=60)

        self.info_label = ctk.CTkLabel(self, text="SYSTEM MONITOR: STABLE", font=("Arial", 10), text_color="#444")
        self.info_label.pack(side="bottom", pady=10)

        self.animate_loop()

    # 3. ADVANCED VISUALS
    def animate_loop(self):
        self.angle += 0.15
        if self.active:
            pulse = (math.sin(self.angle) * 15)
            color = "#ff007f" if self.speaking else "#00f2ff"
            self.canvas.itemconfig(self.orb, outline=color, width=3 if self.speaking else 2)
            
            # Oscilloscope Simulation
            amp = 70 if self.speaking else 10
            y_shift = math.sin(self.angle * 18) * amp
            self.canvas.coords(self.wave, 110, 160+y_shift, 200, 160-y_shift, 290, 160+y_shift)
            self.canvas.itemconfig(self.wave, fill=color)
        else:
            self.canvas.itemconfig(self.orb, outline="#111")
            self.canvas.itemconfig(self.wave, fill="#111")
        self.after(20, self.animate_loop)

    # 4. SPEECH & BRAIN
    def speak(self, text):
        self.speaking = True
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def toggle_system(self):
        if not self.active:
            self.active = True
            self.status.configure(text="NEURAL LINK ACTIVE", text_color="#00f2ff")
            self.main_btn.configure(text="SHUTDOWN", fg_color="#440000")
            threading.Thread(target=self.brain_loop, daemon=True).start()
        else:
            self.active = False
            self.status.configure(text="NEURAL LINK DISCONNECTED", text_color="#222")
            self.main_btn.configure(text="INITIALIZE CORE", fg_color="#008080")

    def brain_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.5
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    self.execute_god_mode(query)
                except: continue

    # 5. THE ULTIMATE EXECUTION ENGINE
    def execute_god_mode(self, query):
        print(f"Master: {query}")

        # --- PERSISTENT TYPING & CLIPBOARD ---
        if 'type' in query or 'write' in query:
            msg = query.replace("type", "").replace("write", "").strip()
            self.speak(f"Writing: {msg}")
            pyautogui.write(msg, interval=0.01)
            pyautogui.press('enter')

        elif 'copy' in query:
            pyautogui.hotkey('ctrl', 'c')
            self.speak("Copied to clipboard.")

        elif 'paste' in query:
            pyautogui.hotkey('ctrl', 'v')
            self.speak("Pasted.")

        # --- SYSTEM PERSISTENCE (LOCK, VOLUME, STATS) ---
        elif 'lock' in query:
            self.speak("Locking system.")
            ctypes.windll.user32.LockWorkStation()

        elif 'volume up' in query:
            pyautogui.press("volumeup", presses=5)
        elif 'volume down' in query:
            pyautogui.press("volumedown", presses=5)
        elif 'mute' in query:
            pyautogui.press("volumemute")

        elif 'pc status' in query or 'cpu' in query:
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            self.speak(f"CPU is at {cpu} percent and RAM usage is at {ram} percent.")

        # --- MEDIA CONTROL ---
        elif 'pause' in query or 'stop music' in query:
            pyautogui.press('playpause')
            self.speak("Media paused.")
        elif 'next' in query:
            pyautogui.press('nexttrack')
            self.speak("Skipping.")

        # --- APP MANAGEMENT (KILL & LAUNCH) ---
        elif 'close' in query:
            app = query.replace("close", "").strip()
            self.speak(f"Terminating {app}.")
            os.system(f"taskkill /f /im {app}.exe")
            pyautogui.hotkey('alt', 'f4')

        elif 'open' in query:
            app = query.replace("open", "").strip()
            self.speak(f"Opening {app} right away.")
            pyautogui.press('win')
            time.sleep(0.3)
            pyautogui.write(app)
            time.sleep(0.4)
            pyautogui.press('enter')

        # --- FILE EXPLORER ---
        elif 'documents' in query:
            os.startfile(os.path.expanduser("~/Documents"))
        elif 'downloads' in query:
            os.startfile(os.path.expanduser("~/Downloads"))

        # --- AI KNOWLEDGE (GEMINI 1.5 FLASH) ---
        else:
            try:
                self.status.configure(text="PROCESSING...", text_color="#ff007f")
                response = model.generate_content(f"You are Serra AI, a PC overlord. Be fast, professional, English: {query}")
                self.speak(response.text)
                self.status.configure(text="NEURAL LINK ACTIVE", text_color="#00f2ff")
            except:
                self.speak("Neural link timeout.")

# ==========================================================
# RUN THE ENGINE
# ==========================================================
if __name__ == "__main__":
    SerraMaster().mainloop()
