import customtkinter as ctk
import threading
import time
import math
import pyttsx3
import speech_recognition as sr

class SerraInterface(ctk.CTk):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain # Unganisha na Brain.py
        
        # Window Configuration
        self.title("SERRA NEURAL INTERFACE")
        self.geometry("900x700")
        self.configure(fg_color="#050505") # Black Dark Theme
        
        # Sauti Engine
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id if len(self.voices) > 1 else self.voices[0].id)
        self.engine.setProperty('rate', 180)
        
        # UI State
        self.is_speaking = False
        self.angle = 0
        
        # --- UI ELEMENTS ---
        self.setup_ui()
        self.animate_waves()

    def setup_ui(self):
        # Header
        self.logo = ctk.CTkLabel(self, text="S E R R A", font=("Orbitron", 30, "bold"), text_color="#00fbff")
        self.logo.pack(pady=20)

        # Canvas ya Mawimbi (Waves)
        self.canvas = ctk.CTkCanvas(self, width=800, height=100, bg="#050505", highlightthickness=0)
        self.canvas.pack()
        self.wave_lines = [self.canvas.create_line(0, 50, 800, 50, fill="#00fbff", width=2, smooth=True) for _ in range(5)]

        # Chat Area (The Display)
        self.chat_display = ctk.CTkTextbox(self, width=800, height=400, font=("Consolas", 15), 
                                           fg_color="#0a0a0a", border_color="#00fbff", border_width=1)
        self.chat_display.pack(pady=10, padx=20)
        self.chat_display.configure(state="disabled") # Zuia user kuedit manually

        # Input Area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20, fill="x", padx=50)

        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ask Serra or command your PC...", 
                                  width=600, height=45, corner_radius=20)
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.send_text())

        self.mic_btn = ctk.CTkButton(self.input_frame, text="LISTEN", width=100, height=45, 
                                     corner_radius=20, fg_color="#00fbff", text_color="black",
                                     command=self.start_listening)
        self.mic_btn.pack(side="left")

    def animate_waves(self):
        """Inafanya mawimbi yacheze kama ya Gemini"""
        self.angle += 0.2
        for i, line in enumerate(self.wave_lines):
            points = []
            amplitude = 40 if self.is_speaking else 5
            for x in range(0, 810, 20):
                y = 50 + math.sin(self.angle + (x * 0.05) + i) * amplitude
                points.extend([x, y])
            self.canvas.coords(line, *points)
        self.after(30, self.animate_waves)

    def typewriter_effect(self, text):
        """Inaandika herufi kwa herufi kama mimi (Gemini)"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\nSERRA> ")
        
        def type_letter(i=0):
            if i < len(text):
                self.chat_display.insert("end", text[i])
                self.chat_display.see("end")
                self.after(25, lambda: type_letter(i + 1)) # Kasi ya kuandika (25ms)
            else:
                self.chat_display.insert("end", "\n")
                self.chat_display.configure(state="disabled")
                self.is_speaking = False

        type_letter()

    def send_text(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"\nYOU> {query}\n")
            self.chat_display.configure(state="disabled")
            
            # Fikiria na Jibu
            threading.Thread(target=self.process_query, args=(query,), daemon=True).start()

    def start_listening(self):
        """Anasikiliza kupitia Mic"""
        threading.Thread(target=self.voice_input_thread, daemon=True).start()

    def voice_input_thread(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.mic_btn.configure(text="LISTENING...", fg_color="#ff004c")
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=5)
                query = r.recognize_google(audio)
                self.chat_display.configure(state="normal")
                self.chat_display.insert("end", f"\nYOU (Voice)> {query}\n")
                self.chat_display.configure(state="disabled")
                self.process_query(query)
            except:
                pass
            self.mic_btn.configure(text="LISTEN", fg_color="#00fbff")

    def process_query(self, query):
        self.is_speaking = True
        response = self.brain.generate_response(query)
        
        # Speak and Type at the same time
        threading.Thread(target=self.speak, args=(response,), daemon=True).start()
        self.typewriter_effect(response)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

if __name__ == "__main__":
    # Hii ni kwa ajili ya testing tu
    pass 

