import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
from google import genai  # Library ya kisasa zaidi (v3)
import time
import os
import webbrowser
import math
import sys

# ==========================================================
# 1. BRAIN CONFIGURATION (UPDATED FOR 2026 SDK)
# ==========================================================
API_KEY = "AIzaSyDyALjWG3yA0tshV3InvZCRADpPcyHa_VE" 

try:
    # Tunatumia Client ya kisasa
    client = genai.Client(api_key=API_KEY)
    # Model uliyoipata kwenye list yako
    MODEL_NAME = "gemini-2.5-flash" 
except Exception as e:
    print(f"API Configuration Error: {e}")
    client = None

# ==========================================================
# 2. THE STABLE VOICE ENGINE (THREAD-SAFE)
# ==========================================================
class VoiceSystem:
    def __init__(self):
        self.lock = threading.Lock()
        
    def speak(self, text):
        with self.lock:
            try:
                print(f"Serra: {text}")
                temp_engine = pyttsx3.init()
                voices = temp_engine.getProperty('voices')
                # Chagua sauti ya kike (kawaida ni index 1)
                temp_engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
                temp_engine.setProperty('rate', 185)
                temp_engine.say(text)
                temp_engine.runAndWait()
                temp_engine.stop()
            except Exception as e:
                print(f"Voice Error: {e}")

voice_box = VoiceSystem()

# ==========================================================
# 3. MAIN INTERFACE (SERRA UI)
# ==========================================================
class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - OVERLORD v3")
        self.geometry("500x700")
        self.attributes("-topmost", True)
        self.config(bg='#010103')
        
        self.active = False
        self.speaking_state = False
        self.angle = 0

        # UI Visuals
        self.header = ctk.CTkLabel(self, text="SERRA", font=("Impact", 80), text_color="#00f2ff")
        self.header.pack(pady=40)
        
        self.canvas = ctk.CTkCanvas(self, width=400, height=350, bg='#010103', highlightthickness=0)
        self.canvas.pack()
        
        self.orb = self.canvas.create_oval(100, 50, 300, 250, outline="#00f2ff", width=2)
        self.wave = self.canvas.create_line(100, 150, 300, 150, fill="#00f2ff", width=4, smooth=True)
        
        self.status = ctk.CTkLabel(self, text="READY", font=("Consolas", 14), text_color="#333")
        self.status.pack(pady=20)
        
        self.btn = ctk.CTkButton(self, text="INITIALIZE CORE", font=("Segoe UI", 22, "bold"), 
                                 command=self.toggle, fg_color="#008080", height=65, corner_radius=15)
        self.btn.pack(pady=10, fill="x", padx=70)
        
        self.animate()

    def animate(self):
        self.angle += 0.15
        if self.active:
            color = "#ff007f" if self.speaking_state else "#00f2ff"
            self.canvas.itemconfig(self.orb, outline=color)
            amp = 65 if self.speaking_state else 10
            y_shift = math.sin(self.angle * 18) * amp
            self.canvas.coords(self.wave, 110, 150+y_shift, 200, 150-y_shift, 290, 150+y_shift)
            self.canvas.itemconfig(self.wave, fill=color)
        self.after(20, self.animate)

    def trigger_speech(self, text):
        self.speaking_state = True
        voice_box.speak(text)
        self.speaking_state = False

    def toggle(self):
        if not self.active:
            self.active = True
            self.status.configure(text="LISTENING...", text_color="#00f2ff")
            self.btn.configure(text="DISENGAGE", fg_color="#550000")
            threading.Thread(target=self.listen_loop, daemon=True).start()
            threading.Thread(target=self.trigger_speech, args=("Serra core initialized. Online and ready.",)).start()
        else:
            self.active = False
            self.status.configure(text="READY", text_color="#333")
            self.btn.configure(text="INITIALIZE CORE", fg_color="#008080")

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
        
        # 1. DIRECT COMMANDS
        if 'calculator' in query:
            threading.Thread(target=self.trigger_speech, args=("Launching calculator.",)).start()
            os.system("calc")
        elif 'google' in query or 'search' in query:
            item = query.replace("google", "").replace("search", "").strip()
            threading.Thread(target=self.trigger_speech, args=(f"Searching {item}",)).start()
            webbrowser.open(f"https://www.google.com/search?q={item}")
        elif 'who are you' in query:
            threading.Thread(target=self.trigger_speech, args=("I am Serra. Your system's neural interface.",)).start()

        # 2. AI BRAIN (2026 SDK Method)
        else:
            if client:
                try:
                    self.status.configure(text="THINKING...", text_color="#ff007f")
                    response = client.models.generate_content(
                        model=MODEL_NAME, 
                        contents=f"You are Serra AI, a direct and sharp system assistant. Answer briefly: {query}"
                    )
                    threading.Thread(target=self.trigger_speech, args=(response.text,)).start()
                    self.status.configure(text="LISTENING...", text_color="#00f2ff")
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    threading.Thread(target=self.trigger_speech, args=("Brain link failed. Check API status.",)).start()
            else:
                threading.Thread(target=self.trigger_speech, args=("Brain module not configured.",)).start()

if __name__ == "__main__":
    try:
        app = SerraAI()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit()
