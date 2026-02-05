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

# Kumbukumbu ya Maongezi (Memory)
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

class SerraOverlord(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA NEURAL INTERFACE v4")
        self.geometry("800x600")
        self.config(bg='#000000')
        self.attributes("-topmost", True)
        
        self.active = False
        self.speaking = False
        self.angle = 0
        
        # --- UI LAYOUT ---
        self.grid_columnconfigure(0, weight=1)
        self.header = ctk.CTkLabel(self, text="SERRA OVERLORD", font=("Orbitron", 40, "bold"), text_color="#00f2ff")
        self.header.pack(pady=10)

        # Waves Animation Canvas
        self.canvas = ctk.CTkCanvas(self, width=600, height=200, bg='#000000', highlightthickness=0)
        self.canvas.pack()
        self.waves = [self.canvas.create_line(0, 100, 600, 100, fill="#00f2ff", width=2, smooth=True) for _ in range(5)]

        # Chat Area
        self.chat_box = ctk.CTkTextbox(self, width=700, height=250, font=("Consolas", 14), fg_color="#050505")
        self.chat_box.pack(pady=10)

        # Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=50)
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Enter Command Master...", width=500, height=40)
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.process_text())

        self.btn = ctk.CTkButton(self.input_frame, text="INIT CORE", command=self.toggle_voice, fg_color="#004444")
        self.btn.pack(side="left")

        self.animate()

    def animate(self):
        self.angle += 0.2
        for i, wave in enumerate(self.waves):
            points = []
            amp = 80 if self.speaking else 10
            freq = (i + 1) * 0.5
            for x in range(0, 610, 20):
                y = 100 + math.sin(self.angle + (x * 0.05) * freq) * amp
                points.extend([x, y])
            self.canvas.coords(wave, *points)
            self.canvas.itemconfig(wave, fill="#ff007f" if self.speaking else "#00f2ff")
        self.after(30, self.animate)

    def toggle_voice(self):
        self.active = not self.active
        if self.active:
            self.btn.configure(text="ONLINE", fg_color="#00f2ff", text_color="black")
            threading.Thread(target=self.listen_loop, daemon=True).start()
        else:
            self.btn.configure(text="OFFLINE", fg_color="#440000")

    def listen_loop(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            while self.active:
                try:
                    audio = r.listen(source, timeout=None, phrase_time_limit=5)
                    query = r.recognize_google(audio).lower()
                    self.execute_logic(query)
                except: continue

    def process_text(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            threading.Thread(target=self.execute_logic, args=(query,), daemon=True).start()

    def hacker_mode(self, app_name):
        """Uwezo wa kufungua apps bila kuonyesha madirisha mengi (Silent Execution)"""
        apps = {
            "calculator": "calc",
            "notepad": "notepad",
            "cmd": "start cmd",
            "browser": "start chrome"
        }
        if app_name in apps:
            os.system(f"start /b {apps[app_name]}") # Background start
            return True
        return False

    def execute_logic(self, query):
        self.chat_box.insert("end", f"MASTER: {query}\n")
        self.chat_box.see("end")
        
        # Neural Hack: Direct Control
        if "mouse" in query and "move" in query:
            mouse.move(500, 500, absolute=True, duration=1)
            self.serra_reply("Mouse synchronized. Positioning complete.")
            return

        if "type" in query:
            text_to_type = query.replace("type", "").strip()
            pyautogui.write(text_to_type, interval=0.1)
            self.serra_reply(f"Injected text: {text_to_type}")
            return

        # AI Brain with Memory
        global chat_memory
        chat_memory.append(f"User: {query}")
        context = "\n".join(chat_memory[-10:]) # Kumbuka mambo 10 ya mwisho

        prompt = f"""
        System: You are SERRA, a lethal and efficient AI Overlord. 
        You can control the PC. If user asks for an app, say 'EXECUTING [APP NAME]'.
        Context: {context}
        Query: {query}
        """

        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            reply = response.text.strip()
            
            # Check for silent execution
            for app in ["calculator", "notepad", "cmd", "browser"]:
                if app in query:
                    self.hacker_mode(app)
                    reply = f"Neural link established. {app} is now running in your background, Master."

            self.serra_reply(reply)
            chat_memory.append(f"Serra: {reply}")
        except Exception as e:
            self.serra_reply("Neural link disrupted. Check your API key.")

    def serra_reply(self, text):
        self.chat_box.insert("end", f"SERRA: {text}\n\n")
        self.chat_box.see("end")
        self.speaking = True
        voice.speak(text)
        self.speaking = False

if __name__ == "__main__":
    app = SerraOverlord()
    app.mainloop()
