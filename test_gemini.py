import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
from google import genai
import math
import sys

# --- CONFIGURATION ---
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI" 
MODEL_NAME = "gemini-2.5-flash"

try:
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"API Error: {e}")
    client = None

class VoiceSystem:
    def __init__(self):
        self.lock = threading.Lock()
    def speak(self, text):
        with self.lock:
            try:
                temp_engine = pyttsx3.init()
                voices = temp_engine.getProperty('voices')
                temp_engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
                temp_engine.setProperty('rate', 180)
                temp_engine.say(text)
                temp_engine.runAndWait()
                temp_engine.stop()
            except: pass

voice_box = VoiceSystem()

class SerraAI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SERRA AI - MANUAL TEST MODE")
        self.geometry("600x800")
        self.config(bg='#010103')
        
        self.speaking_state = False
        self.angle = 0

        # UI Visuals
        self.header = ctk.CTkLabel(self, text="SERRA", font=("Impact", 60), text_color="#00f2ff")
        self.header.pack(pady=20)
        
        self.canvas = ctk.CTkCanvas(self, width=400, height=200, bg='#010103', highlightthickness=0)
        self.canvas.pack()
        self.orb = self.canvas.create_oval(100, 20, 300, 180, outline="#00f2ff", width=2)
        
        # Chat Display
        self.chat_display = ctk.CTkTextbox(self, width=500, height=300, font=("Consolas", 14), fg_color="#050505")
        self.chat_display.pack(pady=10)
        self.chat_display.insert("0.0", "SERRA: Manual link active. Type your command below.\n\n")

        # Input Area
        self.input_field = ctk.CTkEntry(self, width=400, placeholder_text="Uliza swali hapa...", font=("Segoe UI", 14))
        self.input_field.pack(side="left", padx=(50, 10), pady=20)
        self.input_field.bind("<Return>", lambda e: self.manual_execute())

        self.send_btn = ctk.CTkButton(self, text="SEND", width=80, command=self.manual_execute, fg_color="#008080")
        self.send_btn.pack(side="left", pady=20)

        self.animate()

    def animate(self):
        self.angle += 0.15
        color = "#ff007f" if self.speaking_state else "#00f2ff"
        self.canvas.itemconfig(self.orb, outline=color)
        self.after(50, self.animate)

    def manual_execute(self):
        query = self.input_field.get()
        if not query: return
        
        self.input_field.delete(0, 'end')
        self.chat_display.insert("end", f"MASTER: {query}\n")
        self.chat_display.see("end")
        
        threading.Thread(target=self.get_ai_response, args=(query,), daemon=True).start()

    def get_ai_response(self, query):
        if client:
            try:
                self.speaking_state = True
                response = client.models.generate_content(
                    model=MODEL_NAME, 
                    contents=f"You are Serra AI. Be very brief and sharp: {query}"
                )
                txt = response.text.strip()
                self.chat_display.insert("end", f"SERRA: {txt}\n\n")
                self.chat_display.see("end")
                voice_box.speak(txt)
                self.speaking_state = False
            except Exception as e:
                self.chat_display.insert("end", f"SYSTEM ERROR: {e}\n\n")
                self.speaking_state = False

if __name__ == "__main__":
    app = SerraAI()
    app.mainloop()
