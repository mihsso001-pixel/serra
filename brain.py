import os
import json
import subprocess
import webbrowser
import pyautogui
from google import genai
from dotenv import load_dotenv

load_dotenv()

class SerraBrain:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.0-flash"
        self.memory_file = "serra_memory.json"
        self.chat_history = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except: return []
        return []

    def save_memory(self):
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history[-20:], f, indent=4)

    def execute_system_command(self, query):
        """Uwezo wa kipekee wa ku-control PC na Links"""
        q = query.lower()
        
        # Kufungua Website/Links
        if "fungua" in q or "open" in q or "go to" in q:
            if "youtube" in q:
                webbrowser.open("https://www.youtube.com")
                return "System Protocol: Opening YouTube. Navigating to visual streams."
            if "google" in q:
                webbrowser.open("https://www.google.com")
                return "System Protocol: Google search engine initialized."
            if "github" in q:
                webbrowser.open("https://www.github.com")
                return "System Protocol: Accessing the developer mainframe on GitHub."

        # Kufungua Apps za PC
        if "fungua" in q or "launch" in q:
            apps = {"notepad": "notepad.exe", "calc": "calc.exe", "chrome": "start chrome"}
            for app, cmd in apps.items():
                if app in q:
                    subprocess.Popen(cmd, shell=True)
                    return f"System Protocol: {app.capitalize()} is now active."

        return None

    def generate_response(self, user_input):
        # Angalia kama ni amri ya PC kwanza
        command_result = self.execute_system_command(user_input)
        if command_result:
            return command_result

        # Persona ya Gemini
        persona = "You are SERRA, the advanced AI twin of Gemini. Speak with wit, brilliance, and a futuristic tone. You can control the user's PC directly."
        
        try:
            # Kutuma kwa Gemini
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{persona}\nUser: {user_input}\nSERRA:"
            )
            reply = response.text.strip()
            self.chat_history.append({"user": user_input, "serra": reply})
            self.save_memory()
            return reply
        except Exception as e:
            return f"Neural Error: Connection lost. ({str(e)})"
