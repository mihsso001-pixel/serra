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
# 1. BRAIN CONFIGURATION
# ==========================================================
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI" 

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Brain Error: {e}")
    model = None

# ==========================================================
# 2. THE ABSOLUTE VOICE ENGINE (FIXED)
# ==========================================================
# Tunatofautisha engine ya sauti ili isigome
def run_voice(text):
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        # Jaribu kutumia sauti ya kike (Zira) kama ipo, la sivyo tumia ya kwanza
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        engine.setProperty('rate', 180)
        engine.say(text)
        engine.runAndWait()
        # Tunafunga engine baada ya kuongea ili isikwame
        engine.stop()
    except Exception as e:
        print(f"Voice Error: {e}")

# ==========================================================
# 3. SERRA UI CLASS
# ==========================================================
class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - OVERLORD")
        self.geometry("500x700")
        self.attributes("-topmost", True)
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

        self.status = ctk.CTkLabel(self, text="SYSTEM READY", font=("Consolas", 14), text_color="#333")
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

    # Hapa ndipo tulifanya marekebisho ili aongee KWELI
    def speak(self, text):
        print(f"Serra: {text}")
        self.speaking = True
        # Tunatumia Thread mpya kutoa sauti ili UI isigande
        t = threading.Thread(target=run_voice, args=(text,))
        t.start()
        # Tunangoja kidogo kulingana na urefu wa maneno kabla ya kusema 'speaking ni False'
        wait_time = len(text.split()) * 0.4 
        def reset_speaking():
            time.sleep(wait_time)
            self.speaking = False
        threading.Thread(target=reset_speaking).start()

    def toggle(self):
        if not self.active:
            self.active = True
            self.status.configure(text="LISTENING...", text_color="#00f2ff")
            self.btn.configure(text="DISENGAGE", fg_color="#550000")
            threading.Thread(target=self.listen_loop, daemon=True).start()
            self.speak("System initialized. I am online and ready.")
        else:
            self.active = False
            self.status.configure(text="SYSTEM READY", text_color="#333")
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
        
        if 'open calculator' in query:
            self.speak("Opening calculator for you.")
            os.system("calc")
        elif 'open word' in query:
            self.speak("Launching Microsoft Word.")
            os.system("start winword")
        elif 'search' in query:
            topic = query.replace("search", "").strip()
            self.speak(f"Searching for {topic} on the web.")
            webbrowser.open(f"https://www.google.com/search?q={topic}")
        elif 'who are you' in query:
            self.speak("I am Serra, your personal system overlord. I manage your PC and your digital life.")
        elif 'hello' in query or 'hi' in query:
            self.speak("Hello boss. How can I help you today?")
        
        # --- GEMINI BRAIN ---
        else:
            if model:
                try:
                    self.status.configure(text="THINKING...", text_color="#ff007f")
                    response = model.generate_content(f"You are Serra AI, a powerful PC assistant. Answer very briefly: {query}")
                    self.speak(response.text)
                    self.status.configure(text="LISTENING...", text_color="#00f2ff")
                except Exception:
                    self.speak("Neural link timeout. Please check your connection.")
            else:
                self.speak("API key is not working.")

if __name__ == "__main__":
    app = SerraAI()
    app.mainloop()
