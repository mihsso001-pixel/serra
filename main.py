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

# --- CONFIGURATION YA AI ---
API_KEY = "AIzaSyBNHMWT6TH1J6xsiRCA-2X96wwSkZWmZUI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- SETUP SAUTI YA SERRA ---
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
for voice in voices:
    if "Zira" in voice.name or "Female" in voice.name:
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 170)

class SerraUltimateApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Muundo wa Dirisha
        self.title("Serra AI - Intelligent System")
        self.geometry("450x650")
        self.attributes("-topmost", True)
        self.config(bg='#050508') # Black-Blue Deep Theme
        
        # Variables
        self.active = False
        self.speaking = False
        self.listening = False
        self.angle = 0

        # --- UI ELEMENTS ---
        self.header = ctk.CTkLabel(self, text="SERRA AI", font=("Impact", 40), text_color="#00f2ff")
        self.header.pack(pady=(30, 5))

        self.sub_text = ctk.CTkLabel(self, text="PREMIUM ASSISTANT SYSTEM", font=("Segoe UI", 12), text_color="#336677")
        self.sub_text.pack(pady=(0, 20))

        # Canvas kwa ajili ya 3D Orb
        self.canvas = ctk.CTkCanvas(self, width=300, height=300, bg='#050508', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.create_orb_elements()
        
        self.status_label = ctk.CTkLabel(self, text="SYSTEM IDLE", font=("Consolas", 14), text_color="#555555")
        self.status_label.pack(pady=10)

        # Buttons (Modern Style)
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=20, fill="x", padx=50)

        self.start_btn = ctk.CTkButton(self.btn_frame, text="INITIALIZE SERRA", font=("Segoe UI", 18, "bold"), 
                                       command=self.start_system, fg_color="#008080", hover_color="#00aaaa", 
                                       height=50, corner_radius=25)
        self.start_btn.pack(pady=10, fill="x")

        self.stop_btn = ctk.CTkButton(self.btn_frame, text="TERMINATE", command=self.stop_system, 
                                      fg_color="#330000", hover_color="#880000", height=40, corner_radius=20)
        self.stop_btn.pack(pady=5, fill="x")

        # Start Animation
        self.animate_elements()

    def create_orb_elements(self):
        # Glow Effect
        self.aura = self.canvas.create_oval(50, 50, 250, 250, outline="#002233", width=1)
        # Inner 3D Orb
        self.orb_outer = self.canvas.create_oval(70, 70, 230, 230, fill="#080808", outline="#00f2ff", width=2)
        # Wave Core
        self.wave_line = self.canvas.create_line(70, 150, 230, 150, fill="#00f2ff", width=2, smooth=True)

    def animate_elements(self):
        self.angle += 0.05
        pulse = (math.sin(self.angle) * 8)
        
        if self.active:
            # Rangi zinabadilika kulingana na Status
            if self.speaking:
                color = "#ff007f" # Magenta (Anajibu)
                status = "SERRA IS SPEAKING..."
            elif self.listening:
                color = "#00f2ff" # Cyan (Anasikiliza)
                status = "SERRA IS LISTENING..."
            else:
                color = "#00f2ff"
                status = "SYSTEM ACTIVE"

            self.status_label.configure(text=status, text_color=color)
            
            # Orb Animation
            self.canvas.coords(self.orb_outer, 70-pulse, 70-pulse, 230+pulse, 230+pulse)
            self.canvas.itemconfig(self.orb_outer, outline=color)
            
            # Oscilloscope Wave Animation
            y_shift = math.sin(self.angle * 8) * (25 if self.speaking else 5)
            self.canvas.coords(self.wave_line, 80, 150+y_shift, 150, 150-y_shift, 220, 150+y_shift)
            self.canvas.itemconfig(self.wave_line, fill=color)
        else:
            self.canvas.itemconfig(self.orb_outer, outline="#222222")
            self.status_label.configure(text="SYSTEM IDLE", text_color="#444444")
            self.canvas.coords(self.wave_line, 80, 150, 150, 150, 220, 150) # Flatten wave

        self.after(30, self.animate_elements)

    def speak_text(self, text):
        self.speaking = True
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def start_system(self):
        if not self.active:
            self.active = True
            threading.Thread(target=self.main_loop, daemon=True).start()

    def stop_system(self):
        self.active = False

    def main_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while self.active:
                self.listening = True
                r.adjust_for_ambient_noise(source, duration=0.8)
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=6)
                    self.listening = False
                    query = r.recognize_google(audio).lower()
                    print(f"User: {query}")
                    self.process_command(query)
                except:
                    self.listening = False
                    continue

    def process_command(self, query):
        # 1. IDENTITY & SYSTEM INFO
        if 'name' in query or 'who are you' in query:
            self.speak_text("I am Serra AI, your premium intelligence system. I am glad to be back.")

        elif 'battery' in query:
            batt = psutil.sensors_battery()
            self.speak_text(f"Boss, your battery is currently at {batt.percent} percent.")

        elif 'time' in query:
            time_now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak_text(f"The current time is {time_now}")

        # 2. MEDIA & INTERNET
        elif 'play' in query:
            song = query.replace("play", "")
            self.speak_text(f"Searching for {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif 'open' in query:
            app = query.replace("open", "").strip()
            self.speak_text(f"Launching {app}")
            pyautogui.press('win')
            time.sleep(0.4)
            pyautogui.write(app)
            pyautogui.press('enter')

        # 3. AI REASONING (GEMINI)
        else:
            try:
                response = model.generate_content(f"Your name is Serra AI. Answer briefly: {query}")
                self.speak_text(response.text)
            except:
                self.speak_text("My neural link is weak, but my local protocols are online.")

if __name__ == "__main__":
    app = SerraUltimateApp()
    app.mainloop()
