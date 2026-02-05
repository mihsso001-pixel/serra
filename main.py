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
import wikipedia

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

        # Muonekano wa Dirisha (Futuristic UI)
        self.title("Serra AI - Ultimate Edition")
        self.geometry("400x550")
        self.attributes("-topmost", True)
        self.config(bg='#050505')
        ctk.set_appearance_mode("dark")

        # Variables
        self.active = False
        self.speaking = False

        # --- UI ELEMENTS ---
        self.logo_label = ctk.CTkLabel(self, text="SERRA INTELLIGENCE", font=("Impact", 32), text_color="#00f2ff")
        self.logo_label.pack(pady=20)

        # Canvas ya Orb
        self.canvas = ctk.CTkCanvas(self, width=250, height=250, bg='#050505', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Orb Layers (Glow Effect)
        self.orb_bg = self.canvas.create_oval(50, 50, 200, 200, fill="#001a1a", outline="#00f2ff", width=1)
        self.orb = self.canvas.create_oval(70, 70, 180, 180, fill="#111", outline="#00f2ff", width=3)
        
        self.status_label = ctk.CTkLabel(self, text="STATUS: OFFLINE", font=("Consolas", 16), text_color="red")
        self.status_label.pack(pady=5)

        # Buttons
        self.start_btn = ctk.CTkButton(self, text="INITIALIZE SERRA", font=("Segoe UI", 16, "bold"), 
                                       command=self.start_system, fg_color="#008080", hover_color="#00aaaa", height=45)
        self.start_btn.pack(pady=10, padx=20, fill="x")

        self.stop_btn = ctk.CTkButton(self, text="TERMINATE", command=self.stop_system, 
                                      fg_color="#440000", hover_color="#880000")
        self.stop_btn.pack(pady=5)

        # Info Box
        self.info_box = ctk.CTkLabel(self, text="Commands: Open, Play, Battery, Time, WhatsApp, Ask Anything", 
                                     font=("Arial", 10), text_color="gray")
        self.info_box.pack(side="bottom", pady=10)

        # Animation logic
        self.glow_val = 0
        self.glow_dir = 1
        self.animate_orb()

    def animate_orb(self):
        if self.active:
            # Rangi zinabadilika kulingana na kazi
            current_color = "#00f2ff" if not self.speaking else "#ff007f"
            if self.glow_val > 25: self.glow_dir = -2
            elif self.glow_val < 0: self.glow_dir = 2
            
            self.glow_val += self.glow_dir
            self.canvas.coords(self.orb, 70-self.glow_val, 70-self.glow_val, 180+self.glow_val, 180+self.glow_val)
            self.canvas.itemconfig(self.orb, outline=current_color, width=2 + (self.glow_val/4))
        else:
            self.canvas.itemconfig(self.orb, outline="#222")
            
        self.after(40, self.animate_orb)

    def speak_text(self, text):
        self.speaking = True
        print(f"Serra: {text}")
        engine.say(text)
        engine.runAndWait()
        self.speaking = False

    def start_system(self):
        if not self.active:
            self.active = True
            self.status_label.configure(text="STATUS: LISTENING...", text_color="#00f2ff")
            threading.Thread(target=self.main_loop, daemon=True).start()

    def stop_system(self):
        self.active = False
        self.status_label.configure(text="STATUS: OFFLINE", text_color="red")

    def main_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while self.active:
                r.adjust_for_ambient_noise(source, duration=0.8)
                try:
                    audio = r.listen(source, timeout=5, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    print(f"User: {query}")
                    self.process_command(query)
                except:
                    continue

    def process_command(self, query):
        # 1. TIME & IDENTITY
        if 'name' in query or 'who are you' in query:
            self.speak_text("I am Serra AI, your ultimate personal assistant.")

        elif 'time' in query:
            now = datetime.datetime.now().strftime("%I:%M %p")
            self.speak_text(f"The time is {now}")

        # 2. SYSTEM CONTROLS
        elif 'battery' in query:
            batt = psutil.sensors_battery()
            self.speak_text(f"Boss, your battery is at {batt.percent} percent.")

        elif 'screenshot' in query:
            self.speak_text("Taking screenshot.")
            pyautogui.screenshot(f"serra_shot_{int(time.time())}.png")

        elif 'minimize' in query or 'desktop' in query:
            pyautogui.hotkey('win', 'd')
            self.speak_text("Done.")

        # 3. OPEN APPS & WEBSITES
        elif 'open' in query:
            app = query.replace("open", "").strip()
            self.speak_text(f"Opening {app}")
            if 'google' in app: webbrowser.open("google.com")
            else:
                pyautogui.press('win')
                time.sleep(0.4)
                pyautogui.write(app)
                pyautogui.press('enter')

        # 4. MEDIA & WHATSAPP
        elif 'play' in query:
            song = query.replace("play", "")
            self.speak_text(f"Searching {song} on YouTube.")
            pywhatkit.playonyt(song)

        elif 'whatsapp' in query:
            self.speak_text("Who is the receiver? Tell me the number.")
            # Hapa unaweza kuongeza logic ya kurekodi namba
            webbrowser.open("https://web.whatsapp.com")

        # 5. GEMINI AI (Kama si amri ya PC)
        else:
            self.status_label.configure(text="STATUS: THINKING...")
            try:
                response = model.generate_content(f"You are Serra AI. User asked: {query}. Answer briefly.")
                self.status_label.configure(text="STATUS: SPEAKING...")
                self.speak_text(response.text)
                self.status_label.configure(text="STATUS: LISTENING...")
            except:
                self.speak_text("I could not process that with my brain, but I am still online.")

if __name__ == "__main__":
    app = SerraUltimateApp()
    app.mainloop()
