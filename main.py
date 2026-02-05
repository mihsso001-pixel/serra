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

# --- INITIALIZATION ---
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
        # Sauti ya kike ya kisasa
        self.engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
        self.engine.setProperty('rate', 195)
        self.lock = threading.Lock()

    def speak(self, text):
        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()

voice = VoiceEngine()

class SerraOverlord(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA NEURAL INTERFACE v5 - GOD MODE")
        self.geometry("900x700")
        self.config(bg='#000000')
        self.attributes("-topmost", True)
        
        self.active = False
        self.speaking = False
        self.is_voice_query = False # Tofauti ya maandishi na sauti
        self.angle = 0
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkLabel(self, text="SERRA OVERLORD", font=("Orbitron", 40, "bold"), text_color="#00f2ff")
        self.header.pack(pady=10)

        # Waves Animation Canvas
        self.canvas = ctk.CTkCanvas(self, width=800, height=150, bg='#000000', highlightthickness=0)
        self.canvas.pack()
        self.waves = [self.canvas.create_line(0, 75, 800, 75, fill="#00f2ff", width=2, smooth=True) for _ in range(6)]

        # Chat Area
        self.chat_box = ctk.CTkTextbox(self, width=800, height=350, font=("Consolas", 15), fg_color="#050505", border_color="#00f2ff", border_width=1)
        self.chat_box.pack(pady=10)

        # Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=50, pady=10)
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type command or protocol...", width=600, height=45, font=("Consolas", 14))
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.process_text())

        self.btn = ctk.CTkButton(self.input_frame, text="CORE IDLE", command=self.toggle_voice, fg_color="#004444", font=("Orbitron", 12))
        self.btn.pack(side="left")

        self.animate()

    def animate(self):
        self.angle += 0.25
        for i, wave in enumerate(self.waves):
            points = []
            amp = 70 if self.speaking else 5
            freq = (i + 1) * 0.4
            for x in range(0, 820, 20):
                y = 75 + math.sin(self.angle + (x * 0.03) * freq) * amp
                points.extend([x, y])
            self.canvas.coords(wave, *points)
            self.canvas.itemconfig(wave, fill="#ff007f" if self.speaking else "#00f2ff")
        self.after(25, self.animate)

    def toggle_voice(self):
        self.active = not self.active
        if self.active:
            self.btn.configure(text="LISTENING", fg_color="#00f2ff", text_color="black")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.btn.configure(text="CORE IDLE", fg_color="#440000")

    def listen_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.dynamic_energy_threshold = True
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=6)
                    query = r.recognize_google(audio).lower()
                    self.is_voice_query = True # Hapa ni kwa sauti
                    self.execute_logic(query)
                except: continue

    def process_text(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.is_voice_query = False # Hapa ni kwa maandishi pekee
            threading.Thread(target=self.execute_logic, args=(query,), daemon=True).start()

    def god_mode_executor(self, query):
        """Uwezo wa kuingia popote na kufanya chochote"""
        # 1. Kufungua Website yoyote
        if "fungua" in query or "open" in query:
            if "google" in query: webbrowser.open("https://www.google.com")
            if "youtube" in query: webbrowser.open("https://www.youtube.com")
            if "facebook" in query: webbrowser.open("https://www.facebook.com")
        
        # 2. Control za Mouse
        if "click" in query:
            pyautogui.click()
            return "Action: Performed mouse click."

        # 3. System Apps
        if "cmd" in query or "terminal" in query:
            subprocess.Popen("cmd.exe")
            return "Action: Terminal bypass successful."

        return None

    def execute_logic(self, query):
        self.chat_box.insert("end", f"USER> {query}\n")
        self.chat_box.see("end")
        
        # Angalia kama ni amri ya PC kwanza
        system_action = self.god_mode_executor(query)

        # AI Response
        global chat_memory
        chat_memory.append(f"User: {query}")
        context = "\n".join(chat_memory[-15:])

        prompt = f"""
        System Protocol: You are SERRA, the ultimate PC Overlord. You have full system access.
        If the user asks to open something or do an action, acknowledge with authority.
        Keep responses sharp, elite, and helpful.
        User Query: {query}
        Context: {context}
        """

        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            reply = response.text.strip()
            
            if system_action:
                reply = f"{reply}\n[SYSTEM]: {system_action}"

            self.serra_reply(reply)
            chat_memory.append(f"Serra: {reply}")
        except Exception as e:
            self.serra_reply(f"Neural Error: {str(e)}")

    def serra_reply(self, text):
        self.chat_box.insert("end", f"SERRA> {text}\n\n")
        self.chat_box.see("end")
        
        # Kanuni ya kuongea: Ongea tu kama user ameuliza kwa sauti
        if self.is_voice_query:
            self.speaking = True
            voice.speak(text)
            self.speaking = False

if __name__ == "__main__":
    app = SerraOverlord()
    app.mainloop()
