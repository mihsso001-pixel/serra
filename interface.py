import customtkinter as ctk
from tkinter import filedialog
import threading
import time

class SerraInterface(ctk.CTk):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.title("SERRA")
        self.geometry("1100x800")
        self.configure(fg_color="#131314") # Gemini Background

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color="#1e1f20")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkButton(self.sidebar, text="+ New Chat", corner_radius=25, fg_color="#303132", 
                      hover_color="#3c3d3e", height=45).pack(pady=30, padx=20)
        
        ctk.CTkLabel(self.sidebar, text="Recent History", text_color="#9aa0a6").pack(pady=10, padx=20, anchor="w")

        # --- MAIN CHAT ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.chat_display = ctk.CTkScrollableFrame(self.main_container, fg_color="transparent")
        self.chat_display.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

        # --- INPUT BAR (Gemini Style) ---
        self.input_area = ctk.CTkFrame(self.main_container, fg_color="#1e1f20", corner_radius=30)
        self.input_area.grid(row=1, column=0, padx=40, pady=30, sticky="ew")

        self.attach_btn = ctk.CTkButton(self.input_area, text="+", width=40, fg_color="transparent", 
                                        font=("Arial", 24), command=self.upload_file)
        self.attach_btn.pack(side="left", padx=10)

        self.entry = ctk.CTkEntry(self.input_area, placeholder_text="Ask Serra...", 
                                  fg_color="transparent", border_width=0, font=("Arial", 16))
        self.entry.pack(side="left", fill="x", expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.send_message())

        self.send_btn = ctk.CTkButton(self.input_area, text="➤", width=40, fg_color="transparent", 
                                      command=self.send_message)
        self.send_btn.pack(side="right", padx=10)

    def add_bubble(self, text, sender="serra"):
        row = ctk.CTkFrame(self.chat_display, fg_color="transparent")
        row.pack(fill="x", pady=10)

        if sender == "user":
            bubble = ctk.CTkLabel(row, text=text, fg_color="#004a77", text_color="white", 
                                  corner_radius=20, padx=15, pady=10, wraplength=400)
            bubble.pack(side="right", padx=20)
        else:
            bubble = ctk.CTkLabel(row, text="", fg_color="#1e1f20", text_color="#e3e3e3", 
                                  corner_radius=20, padx=15, pady=10, wraplength=500, justify="left")
            bubble.pack(side="left", padx=20)
            self.animate_text(bubble, text)

    def animate_text(self, label, text):
        """Uwezo wa kuandika kama Gemini (Typewriter)"""
        def type_it(i=0):
            if i <= len(text):
                label.configure(text=text[:i])
                self.chat_display._parent_canvas.yview_moveto(1.0)
                self.after(15, lambda: type_it(i + 1))
        type_it()

    def send_message(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.add_bubble(query, sender="user")
            threading.Thread(target=self.get_response, args=(query,), daemon=True).start()

    def get_response(self, query):
        res = self.brain.generate_response(query)
        self.add_bubble(res, sender="serra")

    def upload_file(self):
        file = filedialog.askopenfilename()
        if file: self.add_bubble(f"📎 File Attached: {os.path.basename(file)}", sender="user")
