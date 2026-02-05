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
import math

# ==========================================================
# 1. THE BRAIN (API CONFIGURATION)
# ==========================================================
# API Key yako mpya nimeiweka hapa
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI" 

try:
    genai.configure(api_key=API_KEY)
    # Tunatumia Gemini 1.5 Flash kwa sababu ni faster na haigomi hovyo
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Brain Error: {e}")
    model = None

# Voice Setup
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty('rate', 190)

class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - OVERLORD")
        self.geometry("500x700")
        self.attributes("-topmost", True) # Inakaa juu ya apps zingine
        self.config(bg='#020205')
        
        self.active = False
        self.speaking = False
        self.angle = 0

        # UI Design
        self.header = ctk.CTkLabel(self, text="SERRA", font=("Impact", 80), text_color="#00f2ff")
        self.header.pack(pady=40)

        self.canvas = ctk.CTkCanvas(self, width=400, height=350, bg='#020205', highlightthickness=0)
        self.canvas.pack()
        self.orb = self.canvas.create_oval(100, 50, 300, 250, outline="#00f2ff", width=2)
        self.wave = self.canvas.create_line(100, 150, 300, 150, fill="#00f2ff", width=4, smooth=True)

        self.status = ctk.CTkLabel(self, text="SYSTEM READY", font=("Consolas", 14), text_color="#222")
        self.status.pack(pady=20)

        self.btn = ctk.CTkButton(self, text="ENGAGE CORE", font=("Segoe UI", 22, "bold"), 
                                 command=self.toggle, fg_color="#008080", height=65, corner_radius=15)
        self.btn.pack(pady=10, fill="x", padx=70)
        self.animate()

    def animate(self):
        self.angle += 0.15
        if self.active:
            color = "#ff007f" if self.speaking else "#00f2ff"
            self.canvas.itemconfig(self.orb, outline=color)
            amp = 65 if self.speaking else 10
            y_shift = math.sin(self.angle * 18) * amp
            self.canvas.coords(self.wave, 110, 150+y_shift, 200, 150-y_shift, 290, 150+y_shift)
            self.canvas.itemconfig(self.wave, fill=color)
        self.after(20, self.animate)

    def speak(self, text):
        self.speaking = True
        print(f"Serra: {text}")
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def toggle(self):
        if not self.active:
            self.active = True
            self.status.configure(text="LISTENING...", text_color="#00f2ff")
            self.btn.configure(text="DISENGAGE", fg_color="#550000")
            threading.Thread(target=self.listen_loop, daemon=True).start()
            self.speak("System initialized. I am online.")
        else:
            self.active = False
            self.status.configure(text="SYSTEM READY", text_color="#222")
            self.btn.configure(text="ENGAGE CORE", fg_color="#008080")

    def listen_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.dynamic_energy_threshold = True
            r.pause_threshold = 0.6
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    self.execute(query)
                except: continue

    def execute(self, query):
        print(f"Master: {query}")
        
        # --- 1. LOCAL COMMANDS (Always fast) ---
        if 'open calculator' in query:
            self.speak("Opening calculator.")
            os.system("calc")
        elif 'open word' in query:
            self.speak("Launching Microsoft Word.")
            os.system("start winword")
        elif 'search' in query:
            topic = query.replace("search", "").strip()
            self.speak(f"Searching for {topic}")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        elif 'who are you' in query:
            self.speak("I am Serra AI. Your personal system overlord, built to manage your digital life.")

        # --- 2. THE BIG BRAIN (GEMINI) ---
        else:
            if model:
                try:
                    self.status.configure(text="THINKING...", text_color="#ff007f")
                    # Tunamwambia ajibu kama Serra
                    response = model.generate_content(f"You are Serra AI, a powerful PC assistant. Answer briefly: {query}")
                    self.speak(response.text)
                    self.status.configure(text="LISTENING...", text_color="#00f2ff")
                except Exception as e:
                    self.speak("Neural link timeout. Please check your internet.")
            else:
                self.speak("API configuration missing.")

if __name__ == "__main__":
    SerraAI().mainloop()
