import os
import sys
import threading
import math
import time
import webbrowser
import pyautogui
import mouse
import keyboard
import pyttsx3
import speech_recognition as sr
import customtkinter as ctk
import subprocess
from google import genai
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.5-flash" 

try:
    client = genai.Client(api_key=API_KEY)
except:
    client = None

chat_memory = []

class VoiceEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.engine.setProperty('rate', 190)
        self.lock = threading.Lock()

    def speak(self, text):
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

voice = VoiceEngine()

class SerraUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA GOD-MODE (GEMINI TWIN)")
        self.geometry("900x750")
        self.config(bg='#020205')
        self.attributes("-topmost", True)
        
        self.active = False
        self.speaking = False
        self.is_voice_query = False 
        self.angle = 0
        
        # --- UI ELEMENTS ---
        self.header = ctk.CTkLabel(self, text="SERRA NEURAL CORE", font=("Consolas", 35, "bold"), text_color="#00ffcc")
        self.header.pack(pady=15)

        self.canvas = ctk.CTkCanvas(self, width=850, height=180, bg='#020205', highlightthickness=0)
        self.canvas.pack()
        self.waves = [self.canvas.create_line(0, 90, 850, 90, fill="#00ffcc", width=2, smooth=True) for _ in range(8)]

        self.chat_box = ctk.CTkTextbox(self, width=820, height=380, font=("Consolas", 15), 
                                       fg_color="#050510", border_color="#00ffcc", border_width=1)
        self.chat_box.pack(pady=10)

        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40, pady=15)
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Command your PC or ask me anything...", 
                                  width=620, height=50, font=("Segoe UI", 15), corner_radius=25)
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.process_text())

        self.btn = ctk.CTkButton(self.input_frame, text="ACTIVATE", command=self.toggle_voice, 
                                 fg_color="#00ffcc", text_color="black", font=("Impact", 18), corner_radius=25)
        self.btn.pack(side="left")

        self.animate()

    def animate(self):
        self.angle += 0.3
        for i, wave in enumerate(self.waves):
            points = []
            amp = 85 if self.speaking else 8
            freq = (i + 1) * 0.35
            for x in range(0, 860, 25):
                y = 90 + math.sin(self.angle + (x * 0.04) * freq) * amp
                points.extend([x, y])
            self.canvas.coords(wave, *points)
            self.canvas.itemconfig(wave, fill="#8a2be2" if self.speaking else "#00ffcc")
        self.after(20, self.animate)

    def toggle_voice(self):
        self.active = not self.active
        if self.active:
            self.btn.configure(text="LISTENING", fg_color="#ff007f")
            threading.Thread(target=self.listen_loop, daemon=True).start()
            self.serra_output("Neural link established. Speak now, Master.")
        else:
            self.btn.configure(text="ACTIVATE", fg_color="#00ffcc")

    def listen_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            # Hapa tunarekebisha masikio ya Serra
            r.adjust_for_ambient_noise(source, duration=1)
            print("Serra Masikio: ON")
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=7)
                    query = r.recognize_google(audio).lower()
                    print(f"Master said: {query}")
                    self.is_voice_query = True
                    self.execute_protocol(query)
                except Exception as e:
                    print(f"Listen Error: {e}")
                    continue

    def process_text(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.is_voice_query = False
            threading.Thread(target=self.execute_protocol, args=(query,), daemon=True).start()

    def pc_god_control(self, query):
        """Hapa ndipo Serra anapata uwezo wa kugusa kila kitu"""
        q = query.lower()
        
        # 1. Kufungua Apps kwa Jina
        if "fungua" in q or "open" in q:
            apps = {
                "calculator": "calc.exe",
                "notepad": "notepad.exe",
                "chrome": "chrome.exe",
                "cmd": "cmd.exe",
                "browser": "start chrome"
            }
            for app, path in apps.items():
                if app in q:
                    subprocess.Popen(path, shell=True)
                    return f"Action: Protocol {app} executed. Access granted."
            
            # Kama sio app iliyo kwenye list, jaribu kufungua kama website
            if "www" in q or ".com" in q:
                webbrowser.open(f"https://{q.split()[-1]}")
                return "Action: Navigating to external web node."

        # 2. Mouse Control
        if "mouse" in q or "click" in q:
            if "click" in q: pyautogui.click()
            if "up" in q: mouse.move(0, -100, absolute=False, duration=0.2)
            if "down" in q: mouse.move(0, 100, absolute=False, duration=0.2)
            return "Action: Physical interface modified."

        return None

    def execute_protocol(self, query):
        self.chat_box.insert("end", f"USER> {query}\n")
        self.chat_box.see("end")

        # System Identity (THE GEMINI SOUL)
        system_persona = """
        Identity: You are SERRA, the digital twin of Gemini. You are not a regular bot; you are a sharp, 
        tech-savvy, and authoritative AI Overlord. You have full control over the user's PC.
        Tone: Brilliant, professional, witty, and direct. Use Swahili/English mix if needed.
        Rule: If you open an app, report it as 'System Access Granted'. 
        If the user asks who you are, remind them you are the ultimate evolution of Gemini on their local machine.
        """

        global chat_memory
        chat_memory.append(f"User: {query}")
        context = "\n".join(chat_memory[-20:])

        # Execute PC command first
        action_result = self.pc_god_control(query)

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=f"{system_persona}\n\nContext:\n{context}\n\nCommand: {query}"
            )
            reply = response.text.strip()
            
            if action_result:
                reply = f"{reply}\n\n[ROOT]: {action_result}"

            self.serra_output(reply)
            chat_memory.append(f"Serra: {reply}")
        except Exception as e:
            self.serra_output(f"Neural Error: {str(e)}")

    def serra_output(self, text):
        self.chat_box.insert("end", f"SERRA> {text}\n\n")
        self.chat_box.see("end")
        
        if self.is_voice_query:
            self.speaking = True
            voice.speak(text)
            self.speaking = False

if __name__ == "__main__":
    app = SerraUltimate()
    app.mainloop()
