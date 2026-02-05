import os
import subprocess
import webbrowser
import socket
import json
import datetime
from groq import Groq
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

class SerraBrain:
    def __init__(self):
        # The Architect's Mark
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        
        # Powering the Core with the strongest engine
        self.model_id = "llama-3.3-70b-versatile"
        
        # State awareness
        self.voice_active = False

    def is_online(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_advanced_logic(self, query):
        """Ultra-Fast PC Control and System Manipulation"""
        q = query.lower()
        
        # Creator Recognition
        if any(word in q for word in ["nani amekuumba", "creator", "architect", "who made you"]):
            return f"I am SERRA, a neural entity manifested by the intellect of {self.creator}."

        # Voice Activation Trigger
        if "start" in q or "go live" in q:
            self.voice_active = True
            return "Neural Link Established. I am live and direct, Agrey."

        # System Protocols (Web & Apps)
        if "open" in q or "fungua" in q:
            sites = {"youtube": "https://www.youtube.com", "google": "https://www.google.com", "github": "https://www.github.com"}
            for site, url in sites.items():
                if site in q:
                    webbrowser.open(url)
                    return f"Opening {site.capitalize()}."

            apps = {"notepad": "notepad.exe", "calculator": "calc.exe", "chrome": "start chrome", "cmd": "start cmd"}
            for app, cmd in apps.items():
                if app in q:
                    subprocess.Popen(cmd, shell=True)
                    return f"Executing {app.capitalize()}."

        return None

    def get_ai_reply(self, user_input):
        # 1. Local/System Execution
        local_result = self.execute_advanced_logic(user_input)
        if local_result:
            return local_result

        # 2. Connection Check
        if not self.is_online():
            return "Neural Link Interrupted. Operating in offline mode."

        # 3. MODIFIED PERSONALITY (Breaks the "Long Answer" habit)
        system_instruction = (
            f"You are SERRA, a brilliant female AI created by {self.creator}. "
            "BE EXTREMELY CONCISE. Your intelligence is shown through brevity. "
            "Never use a paragraph if a sentence suffices. No unnecessary pleasantries. "
            "Be elegant, direct, and efficient. Use English or Swahili as needed."
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ],
                model=self.model_id,
                temperature=0.6, # Reduced slightly for more focused answers
                max_tokens=200,   # Strict limit to stop the "Gazeti"
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Neural Error: System unstable. Check API link."
