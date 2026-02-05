import customtkinter as ctk
from tkinter import filedialog
import threading
import os
import speech_recognition as sr
import pyttsx3

class SerraInterface(ctk.CTk):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        
        # Window Setup
        self.title("SERRA NEURAL INTERFACE")
        self.geometry("1100x850")
        self.configure(fg_color="#131314")

        # Initialize Voice Engine (Female & Slow)
        self.tts_engine = pyttsx3.init()
        self.setup_female_voice()

        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1e1f20")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.new_chat_btn = ctk.CTkButton(self.sidebar, text="+ New Session", corner_radius=25, 
                                          fg_color="#303132", height=45, command=self.reset_chat)
        self.new_chat_btn.pack(pady=30, padx=20)
        
        self.credits = ctk.CTkLabel(self.sidebar, text=f"Architect: Agrey Albert Moses", 
                                     text_color="#4285F4", font=("Arial", 11, "italic"))
        self.credits.pack(side="bottom", pady=20)

        # --- MAIN CHAT ---
        self.chat_container = ctk.CTkFrame(self, fg_color="transparent")
        self.chat_container.grid(row=0, column=1, sticky="nsew")
        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)

        self.scroll_frame = ctk.CTkScrollableFrame(self.chat_container, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        # --- INPUT AREA ---
        self.bottom_bar = ctk.CTkFrame(self.chat_container, fg_color="#1e1f20", corner_radius=30)
        self.bottom_bar.grid(row=1, column=0, padx=40, pady=30, sticky="ew")

        self.add_file_btn = ctk.CTkButton(self.bottom_bar, text="+", width=40, fg_color="transparent", 
                                          font=("Arial", 24), command=self.handle_upload)
        self.add_file_btn.pack(side="left", padx=10)

        self.user_input = ctk.CTkEntry(self.bottom_bar, placeholder_text="Message Serra...", 
                                       fg_color="transparent", border_width=0, font=("Arial", 16))
        self.user_input.pack(side="left", fill="x", expand=True, padx=5)
        self.user_input.bind("<Return>", lambda e: self.send_request())

        self.live_btn = ctk.CTkButton(self.bottom_bar, text="Go Live", width=80, corner_radius=20,
                                      fg_color="#4285F4", command=self.start_voice_mode)
        self.live_btn.pack(side="right", padx=5)

        self.send_btn = ctk.CTkButton(self.bottom_bar, text="➤", width=40, fg_color="transparent", 
                                      command=self.send_request)
        self.send_btn.pack(side="right", padx=10)

    def setup_female_voice(self):
        """Finds a female voice and slows down the speech rate"""
        voices = self.tts_engine.getProperty('voices')
        # Usually, voices[1] is female on Windows, but we check for 'female' in name
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                self.tts_engine.setProperty('voice', voice.id)
                break
        self.tts_engine.setProperty('rate', 165) # Slower pace for elegance

    def create_bubble(self, message, role="serra"):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        row.pack(fill="x", pady=10)

        align = "right" if role == "user" else "left"
        bg_color = "#004a77" if role == "user" else "#2b2c2e"
        display_name = "YOU" if role == "user" else "SERRA"

        bubble = ctk.CTkFrame(row, fg_color=bg_color, corner_radius=18)
        bubble.pack(side=align, padx=20)

        name_tag = ctk.CTkLabel(bubble, text=display_name, font=("Arial", 10, "bold"), text_color="#8ab4f8")
        name_tag.pack(anchor="w", padx=15, pady=(5, 0))

        content = ctk.CTkLabel(bubble, text="", text_color="#e3e3e3", wraplength=500, justify="left", font=("Arial", 14))
        content.pack(padx=15, pady=(2, 10))

        if role == "serra":
            self.typewriter_effect(content, message)
            # Run voice in a separate thread so it doesn't freeze the UI
            threading.Thread(target=self.speak_text, args=(message,), daemon=True).start()
        else:
            content.configure(text=message)

    def typewriter_effect(self, label, text):
        def type_it(i=0):
            if i <= len(text):
                label.configure(text=text[:i])
                self.scroll_frame._parent_canvas.yview_moveto(1.0)
                self.after(15, lambda: type_it(i + 1))
        type_it()

    def speak_text(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def send_request(self):
        msg = self.user_input.get()
        if msg:
            self.user_input.delete(0, 'end')
            self.create_bubble(msg, role="user")
            threading.Thread(target=self.fetch_ai_response, args=(msg,), daemon=True).start()

    def fetch_ai_response(self, query):
        reply = self.brain.get_ai_reply(query)
        self.create_bubble(reply, role="serra")

    def reset_chat(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

    def start_voice_mode(self):
        self.live_btn.configure(text="Listening...", fg_color="#ea4335")
        threading.Thread(target=self.listen_thread, daemon=True).start()

    def listen_thread(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                self.after(0, lambda: self.handle_voice_input(text))
            except: pass
            self.after(0, lambda: self.live_btn.configure(text="Go Live", fg_color="#4285F4"))

    def handle_voice_input(self, text):
        self.create_bubble(text, role="user")
        threading.Thread(target=self.fetch_ai_response, args=(text,), daemon=True).start()

    def handle_upload(self):
        f = filedialog.askopenfilename()
        if f: self.create_bubble(f"📎 File Attached: {os.path.basename(f)}", role="user")
