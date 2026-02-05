import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
import google.generativeai as genai
import time
import os
import webbrowser
import math
import sys

# ==========================================================
# 1. BRAIN CONFIGURATION (MODEL NAME FIXED)
# ==========================================================
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI" 

try:
    genai.configure(api_key=API_KEY)
    # Tumetumia jina la model ambalo ni stable zaidi kuzuia 404 error
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"API Configuration Error: {e}")
    model = None

# ==========================================================
# 2. THE STABLE VOICE ENGINE (THREAD-SAFE)
# ==========================================================
class VoiceSystem:
    def __init__(self):
        self.lock = threading.Lock()
        
    def speak(self, text):
        # Tunatumia Lock kuhakikisha sauti hazipigani (No "run loop" error)
        with self.lock:
            try:
                print(f"Serra: {text}")
                # Kila mara tunatengeneza engine mpya na kuifuta ili kuzuia kulegalega
                temp_engine = pyttsx3.init('sapi5')
                voices = temp_engine.getProperty('voices')
                temp_engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
                temp_engine.setProperty('rate', 185)
                temp_engine.say(text)
                temp_engine.runAndWait()
                temp_engine.stop()
                del temp_engine # Inafuta engine kwenye memory
            except Exception as e:
                print(f"Voice Error: {e}")

voice_box = VoiceSystem()

# ==========================================================
# 3. MAIN INTERFACE
# ==========================================================
class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - THE ULTIMATE")
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
            r.pause_threshold = 0.5
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    self.execute(query)
                except: continue

    def execute(self, query):
        print(f"Master: {query}")
        
        # 1. DIRECT COMMANDS (Fastest)
        if 'calculator' in query:
            threading.Thread(target=self.trigger_speech, args=("Opening calculator.",)).start()
            os.system("calc")
        elif 'google' in query or 'search' in query:
            item = query.replace("google", "").replace("search", "").strip()
            threading.Thread(target=self.trigger_speech, args=(f"Searching {item}",)).start()
            webbrowser.open(f"https://www.google.com/search?q={item}")
        elif 'word' in query:
            threading.Thread(target=self.trigger_speech, args=("Launching Word.",)).start()
            os.system("start winword")
        elif 'who are you' in query:
            threading.Thread(target=self.trigger_speech, args=("I am Serra AI. An advanced system overlord. I control this PC with absolute efficiency.",)).start()

        # 2. AI BRAIN (With 404 Protection)
        else:
            if model:
                try:
                    self.status.configure(text="THINKING...", text_color="#ff007f")
                    # Tumeseti model kwa jina kamili kuzuia 404
                    response = model.generate_content(f"You are Serra AI. Be very brief: {query}")
                    threading.Thread(target=self.trigger_speech, args=(response.text,)).start()
                    self.status.configure(text="LISTENING...", text_color="#00f2ff")
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    threading.Thread(target=self.trigger_speech, args=("Neural connection unstable. Check your network or API quota.",)).start()
            else:
                threading.Thread(target=self.trigger_speech, args=("Brain module not loaded.",)).start()

if __name__ == "__main__":
    try:
        app = SerraAI()
        app.mainloop()
    except KeyboardInterrupt:
        sys.exit()
