import os
import json
import subprocess
import webbrowser
import socket
from google import genai
from dotenv import load_dotenv

load_dotenv()

class SerraBrain:
    def __init__(self):
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.0-flash"
        
    def check_connection(self):
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_local_command(self, query):
        q = query.lower()
        # System control commands (Work offline)
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "start chrome",
            "vlc": "vlc.exe"
        }
        
        for app, cmd in apps.items():
            if app in q:
                subprocess.Popen(cmd, shell=True)
                return f"System Protocol: I have launched {app.capitalize()} for you."

        if any(word in q for word in ["creator", "muumbaji", "who made you"]):
            return f"I was created by the brilliant mind of {self.creator}. He is my father and my architect."

        return None

    def get_ai_reply(self, user_input):
        # First check for local PC commands
        local_result = self.execute_local_command(user_input)
        if local_result:
            return local_result

        # Check internet for AI response
        if not self.check_connection():
            return "I am currently offline, but I can still help you control your PC. Please check your connection for my full neural capacity."

        # Feminine & Emotional Persona
        system_instruction = (
            f"You are SERRA, an advanced female AI. Your creator is {self.creator}. "
            "Your personality: Sophisticated, calm, feminine, and witty. "
            "You can express emotions: Be gentle when the user is kind, and firm but polite when the user is rude. "
            "You understand both Swahili and English perfectly. Always prioritize being helpful."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{system_instruction}\nUser: {user_input}\nSERRA:"
            )
            return response.text.strip()
        except Exception as e:
            return f"Neural Error: {str(e)}. Should we proceed in offline mode?"
