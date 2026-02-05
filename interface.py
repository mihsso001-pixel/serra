import customtkinter as ctk
import threading
import math

# Sanifu rangi (Gemini Palette)
BG_COLOR = "#0F0F0F"  # Giza nene
TEXT_BG = "#1E1E1E"   # Box la maneno
ACCENT_COLOR = "#4285F4" # Blue ya Google
SERRA_TEXT = "#00fbff" # Cyan ya Serra

class SerraInterface(ctk.CTk):
    def __init__(self, brain):
        super().__init__()
        self.brain = brain
        self.title("SERRA AI")
        self.geometry("950x750")
        self.configure(fg_color=BG_COLOR)

        # 1. Header Safi
        self.header = ctk.CTkLabel(self, text="S E R R A", font=("Impact", 35), text_color=ACCENT_COLOR)
        self.header.pack(pady=(20, 10))

        # 2. Chat Display (Imetulia bila border mbaya)
        self.chat_display = ctk.CTkTextbox(
            self, width=850, height=450, 
            font=("Segoe UI", 16), 
            fg_color=TEXT_BG, 
            border_width=0, 
            corner_radius=15,
            scrollbar_button_color=ACCENT_COLOR
        )
        self.chat_display.pack(pady=10, padx=20)
        self.chat_display.configure(state="disabled")

        # 3. Input Area (Kama ya Gemini)
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(pady=20, fill="x", padx=50)

        self.entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Kama unavyoniuliza mimi hapa...", 
            width=650, height=50, 
            corner_radius=25,
            border_color=ACCENT_COLOR,
            fg_color="#252525"
        )
        self.entry.pack(side="left", padx=10)
        self.entry.bind("<Return>", lambda e: self.send_text())

        # 4. Kitufe cha Listen
        self.mic_btn = ctk.CTkButton(
            self.input_frame, text="●", 
            width=50, height=50, 
            corner_radius=25, 
            fg_color=ACCENT_COLOR,
            hover_color="#3367D6",
            text_color="white",
            font=("Arial", 20),
            command=self.start_listening
        )
        self.mic_btn.pack(side="left")

    def typewriter_effect(self, text):
        """Hapa ndipo 'usenge' unaisha na u-Gemini unaanza"""
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", "\n✨ SERRA: ", "serra_tag")
        
        def type_letter(i=0):
            if i < len(text):
                self.chat_display.insert("end", text[i])
                self.chat_display.see("end")
                self.after(20, lambda: type_letter(i + 1)) # Spidi ya herufi
            else:
                self.chat_display.insert("end", "\n")
                self.chat_display.configure(state="disabled")

        type_letter()

    def send_text(self):
        query = self.entry.get()
        if query:
            self.entry.delete(0, 'end')
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"\n👤 YOU: {query}\n", "user_tag")
            self.chat_display.configure(state="disabled")
            threading.Thread(target=self.process_query, args=(query,), daemon=True).start()

    def process_query(self, query):
        response = self.brain.generate_response(query)
        self.typewriter_effect(response)
