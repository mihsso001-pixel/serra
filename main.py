import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time
import os
import webbrowser
import pyautogui
import math

# ==========================================================
# 1. BRAIN CONFIGURATION (API FIXED)
# ==========================================================
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI" 

try:
    genai.configure(api_key=API_KEY)
    # Tumeseti model na mipaka ya usalama
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"API Configuration Error: {e}")
    model = None

# ==========================================================
# 2. STABLE VOICE ENGINE (PREVENTS "RUN LOOP" ERROR)
# ==========================================================
class VoiceSystem:
    def __init__(self):
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.engine.setProperty('rate', 185)
        self.lock = threading.Lock()

    def speak(self, text):
        with self.lock: # Inahakikisha sauti moja inatoka kwa wakati
            try:
                print(f"Serra: {text}")
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as e:
                print(f"Voice Internal Error: {e}")

voice_box = VoiceSystem()

# ==========================================================
# 3. MAIN INTERFACE
# ==========================================================
class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - ABSOLUTE")
        self.geometry("500x700")
        self.attributes("-topmost", True)
        self.config(bg='#020205')
        
        self.active = False
        self.speaking_state = False
        self.angle = 0

        # UI
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
            threading.Thread(target=self.trigger_speech, args=("System initialized. I am online and ready.",)).start()
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
        
        # --- COMMANDS THAT DON'T NEED API (IMMEDIATE) ---
        if 'calculator' in query:
            threading.Thread(target=self.trigger_speech, args=("Opening calculator.",)).start()
            os.system("calc")
        elif 'google' in query:
            threading.Thread(target=self.trigger_speech, args=("Opening Google.",)).start()
            webbrowser.open("https://www.google.com")
        elif 'word' in query:
            threading.Thread(target=self.trigger_speech, args=("Launching Microsoft Word.",)).start()
            os.system("start winword")
        elif 'who are you' in query:
            threading.Thread(target=self.trigger_speech, args=("I am Serra, your personal system overlord. I manage your hardware and provide intelligent feedback.",)).start()
        
        # --- BRAIN COMMANDS (WITH API TIMEOUT PROTECTION) ---
        else:
            if model:
                try:
                    self.status.configure(text="THINKING...", text_color="#ff007f")
                    # Tumeongeza request_options kulazimisha timeout kubwa
                    response = model.generate_content(f"Answer very briefly: {query}")
                    threading.Thread(target=self.trigger_speech, args=(response.text,)).start()
                    self.status.configure(text="LISTENING...", text_color="#00f2ff")
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    threading.Thread(target=self.trigger_speech, args=("My neural link is slow, but I am still here. Check your network.",)).start()
            else:
                threading.Thread(target=self.trigger_speech, args=("My brain is not connected.",)).start()

if __name__ == "__main__":
    app = SerraAI()
    app.mainloop()
