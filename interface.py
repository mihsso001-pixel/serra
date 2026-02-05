import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import speech_recognition as sr
import pyttsx3

class SerraInterface(ctk.CTk):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.title("SERRA")
        self.geometry("1100x850")
        self.configure(fg_color="#131314")

        # Voice Engine
        self.speaker = pyttsx3.init()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1e1f20")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.new_btn = ctk.CTkButton(self.sidebar, text="+ New Chat", corner_radius=25, 
                                     fg_color="#303132", height=45, command=self.clear_chat)
        self.new_btn.pack(pady=30, padx=20)
        
        self.info_lbl = ctk.CTkLabel(self.sidebar, text=f"Creator: Agrey Albert Moses", 
                                     text_color="#4285F4", font=("Arial", 10, "italic"))
        self.info_lbl.pack(side="bottom", pady=20)

        # --- MAIN CHAT ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.chat_display = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        # --- INPUT BAR ---
        self.input_area = ctk.CTkFrame(self.main_container, fg_color="#1e1f20", corner_radius=30)
        self.input_area.grid(row=1, column=0, padx=40, pady=30, sticky="ew")

        self.attach_btn = ctk.CTkButton(self.input_area, text="+", width=40, fg_color="transparent", 
                                        font=("Arial", 24), command=self.upload_file)
        self.attach_btn.pack(side="left", padx=10)

        self.entry = ctk.CTkEntry(self.input_area, placeholder_text="Ongea na Serra...", 
                                  fg_color="transparent", border_width=0, font=("Arial", 16))
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.send_message())

        # Go Live Button
        self.live_btn = ctk.CTkButton(self.input_area, text="Go Live", width=80, corner_radius=20,
                                      fg_color="#4285F4", command=self.go_live)
        self.live_btn.pack(side="right", padx=5)

        self.send_btn = ctk.CTkButton(self.input_area, text="➤", width=40, fg_color="transparent", 
                                      command=self.send_message)
        self.send_btn.pack(side="right", padx=10)

    def add_bubble(self, text, sender="serra"):
        row = ctk.CTkFrame(self.chat_display, fg_color="transparent")
        row.pack(fill="x", pady=10)

        side = "right" if sender == "user" else "left"
        color = "#004a77" if sender == "user" else "#2b2c2e"
        name_tag = "YOU" if sender == "user" else "SERRA"

        bubble = ctk.CTkFrame(row, fg_color=color, corner_radius=18)
        bubble.pack(side=side, padx=20)

        name_lbl = ctk.CTkLabel(bubble, text=name_tag, font=("Arial", 10, "bold"), 
                                text_color="#8ab4f8")
        name_lbl.pack(anchor="w", padx=15, pady=(5, 0))

        content_lbl = ctk.CTkLabel(bubble, text="", text_color="#e3e3e3", 
                                   wraplength=500, justify="left", font=("Arial", 14))
        content_lbl.pack(padx=15, pady=(2, 10))

        if sender == "serra":
            self.animate_text(content_lbl, text)
            # Serra anongea sauti pia
            threading.Thread(target=lambda: (self.speaker.say(text), self.speaker.runAndWait()), daemon=True).start()
        else:
            content_lbl.configure(text=text)

    def animate_text(self, label, text):
        def type_it(i=0):
            if i <= len(text):
                label.configure(text=text[:i])
                self.chat_display._parent_canvas.yview_moveto(1.0)
                self.after(15, lambda: type_it(i + 1))
        type_it()

    def go_live(self):
        self.live_btn.configure(text="Sikiliza...", fg_color="#ea4335")
        threading.Thread(target=self.voice_thread, daemon=True).start()

    def voice_thread(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = r.listen(source, timeout=5)
                query = r.recognize_google(audio)
                self.after(0, lambda: self.process_input(query))
            except: pass
            self.after(0, lambda: self.live_btn.configure(text="Go Live", fg_color="#4285F4"))

    def send_message(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.process_input(query)

    def process_input(self, query):
        self.add_bubble(query, sender="user")
        threading.Thread(target=self.get_ai_response, args=(query,), daemon=True).start()

    def get_ai_response(self, query):
        res = self.brain.generate_response(query)
        self.add_bubble(res, sender="serra")

    def clear_chat(self):
        for child in self.chat_display.winfo_children():
            child.destroy()

    def upload_file(self):
        f = filedialog.askopenfilename()
        if f: self.add_bubble(f"📎 File: {os.path.basename(f)}", sender="user")
