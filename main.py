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
import sys

# ==========================================================
# 1. CORE CONFIGURATION
# ==========================================================
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize Voice Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# Set to English Female (Zira or similar)
for v in voices:
    if "Zira" in v.name or "Female" in v.name or "EN-US" in v.name:
        engine.setProperty('voice', v.id)
        break
engine.setProperty('rate', 185) # Pro speed

# ==========================================================
# 2. UI DESIGN (SERRA PRO INTERFACE)
# ==========================================================
class SerraUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - ULTIMATE CORE")
        self.geometry("450x650")
        self.attributes("-topmost", True)
        self.config(bg='#020205')
        
        self.active = False
        self.speaking = False
        self.angle = 0

        # Header
        self.header = ctk.CTkLabel(self, text="SERRA AI", font=("Impact", 55), text_color="#00f2ff")
        self.header.pack(pady=(30, 0))

        self.sub = ctk.CTkLabel(self, text="ACTIVE NEURAL LINK", font=("Consolas", 12), text_color="#005566")
        self.sub.pack(pady=(0, 20))

        # 3. THE 3D ANIMATED ORB CANVAS
        self.canvas = ctk.CTkCanvas(self, width=320, height=320, bg='#020205', highlightthickness=0)
        self.canvas.pack()
        
        # Orbital Rings & Core Wave
        self.ring = self.canvas.create_oval(60, 60, 260, 260, outline="#003344", width=1)
        self.orb = self.canvas.create_oval(80, 80, 240, 240, outline="#00f2ff", width=3)
        self.wave = self.canvas.create_line(80, 160, 240, 160, fill="#00f2ff", width=2, smooth=True)

        self.status = ctk.CTkLabel(self, text="STATUS: STANDBY", font=("Consolas", 16), text_color="#444")
        self.status.pack(pady=20)

        # Control Buttons
        self.action_btn = ctk.CTkButton(self, text="INITIALIZE CORE", font=("Segoe UI", 20, "bold"), 
                                        command=self.toggle_system, fg_color="#008080", 
                                        hover_color="#00aaaa", height=55, corner_radius=15)
        self.action_btn.pack(pady=10, fill="x", padx=60)

        self.exit_btn = ctk.CTkButton(self, text="EXIT SYSTEM", command=sys.exit, 
                                      fg_color="transparent", text_color="red", hover_color="#220000")
        self.exit_btn.pack(pady=5)

        self.animate_loop()

    # ==========================================================
    # 4. ANIMATION LOGIC (Visual Feedback)
    # ==========================================================
    def animate_loop(self):
        self.angle += 0.07
        if self.active:
            pulse = (math.sin(self.angle) * 12)
            color = "#ff007f" if self.speaking else "#00f2ff"
            
            # Orbit Pulse
            self.canvas.coords(self.orb, 80-pulse, 80-pulse, 240+pulse, 240+pulse)
            self.canvas.itemconfig(self.orb, outline=color)
            
            # Oscilloscope Wave logic
            y_shift = math.sin(self.angle * 10) * (40 if self.speaking else 10)
            self.canvas.coords(self.wave, 90, 160+y_shift, 160, 160-y_shift, 230, 160+y_shift)
            self.canvas.itemconfig(self.wave, fill=color)
        else:
            self.canvas.itemconfig(self.orb, outline="#111")
            self.canvas.itemconfig(self.wave, fill="#111")
            
        self.after(30, self.animate_loop)

    # ==========================================================
    # 5. BRAIN & SPEECH LOGIC
    # ==========================================================
    def speak(self, text):
        self.speaking = True
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def toggle_system(self):
        if not self.active:
            self.active = True
            self.status.configure(text="STATUS: LISTENING", text_color="#00f2ff")
            self.action_btn.configure(text="KILL SYSTEM", fg_color="#550000")
            threading.Thread(target=self.listener_thread, daemon=True).start()
        else:
            self.active = False
            self.status.configure(text="STATUS: STANDBY", text_color="#444")
            self.action_btn.configure(text="INITIALIZE CORE", fg_color="#008080")

    def listener_thread(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.7)
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=5)
                    query = r.recognize_google(audio).lower()
                    self.execute_command(query)
                except: continue

    # ==========================================================
    # 6. ACTION EXECUTION (The Real Deal)
    # ==========================================================
    def execute_command(self, query):
        print(f"Command Received: {query}")
        
        # A. Identity
        if 'who are you' in query or 'your name' in query:
            self.speak("I am Serra. Your high-performance AI assistant.")

        # B. PC Operations
        elif 'calculator' in query:
            self.speak("Opening Calculator now.")
            os.system("calc")

        elif 'notepad' in query:
            self.speak("Right away. Opening Notepad.")
            os.system("notepad")

        elif 'chrome' in query or 'google' in query:
            self.speak("Launching Chrome browser.")
            webbrowser.open("https://www.google.com")

        elif 'youtube' in query and 'play' not in query:
            self.speak("Navigating to YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif 'time' in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}")

        elif 'battery' in query:
            pct = psutil.sensors_battery().percent
            self.speak(f"The system battery is at {pct} percent.")

        elif 'play' in query:
            song = query.replace("play", "").strip()
            self.speak(f"Streaming {song} on YouTube.")
            pywhatkit.playonyt(song)
        
        elif 'screenshot' in query:
            self.speak("Screen captured successfully.")
            pyautogui.screenshot(f"SerraShot_{int(time.time())}.png")

        # C. General Knowledge (Gemini)
        else:
            self.status.configure(text="STATUS: PROCESSING", text_color="#ff007f")
            try:
                # Direct English response
                response = model.generate_content(f"You are Serra AI. Be pro, be brief, and answer in English: {query}")
                self.speak(response.text)
                self.status.configure(text="STATUS: LISTENING", text_color="#00f2ff")
            except Exception as e:
                self.speak("Connection error. Please check your network.")

# ==========================================================
# 7. MAIN EXECUTION
# ==========================================================
if __name__ == "__main__":
    app = SerraUltimate()
    app.mainloop()
