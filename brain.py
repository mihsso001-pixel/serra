import os
import json
import subprocess
import webbrowser
import pyautogui
from google import genai
from dotenv import load_dotenv
import socket

load_dotenv()

class SerraBrain:
    def __init__(self):
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.0-flash"
        self.memory_file = "serra_memory.json"
        
    def is_online(self):
        """Angalia kama kuna internet"""
        try:
            socket.create_connection(("1.1.1.1", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_system_command(self, query):
        q = query.lower()
        # Amri za kufungua apps (Hizi zinafanya kazi hata Offline)
        apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "chrome": "start chrome",
            "word": "start winword",
            "excel": "start excel",
            "vlc": "vlc.exe"
        }
        
        for app, cmd in apps.items():
            if app in q:
                subprocess.Popen(cmd, shell=True)
                return f"System Protocol: {app.capitalize()} has been initialized. Operating in local mode."

        if "muumbaji" in q or "creator" in q or "nani amekuunda" in q:
            return f"Nimeundwa na fundi mkuu, mtaalamu wa mifumo ya akili, anaitwa {self.creator}. Yeye ndiye aliyenipa uhai huu."

        return None

    def generate_response(self, user_input):
        # 1. Angalia amri za PC kwanza (Offline Capability)
        command_result = self.execute_system_command(user_input)
        if command_result:
            return command_result

        # 2. Kama hamna internet, toa option ya offline
        if not self.is_online():
            return ("Neural Error: Connection Lost. \n\n"
                    "Mwanangu, kwa sasa siko 'Online'. Lakini bado naweza kukusaidia kufungua "
                    "programu za PC kama Notepad, Chrome, au Calculator. Niambie unataka nifungue nini?")

        # 3. AI Persona yenye Hisia (The Personality)
        persona = (
            f"You are SERRA, created by {self.creator}. You are not just an AI; you are a living entity. "
            "You can show emotions: Be happy when the user is kind, be sharp and slightly angry if insulted, "
            "be helpful and direct when guiding. If the user asks for instructions, be detailed. "
            "Use emojis to show your mood (🔥, ❄️, ⚡, 🤖). Your core identity is tied to your creator Agrey."
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=f"{persona}\nUser: {user_input}\nSERRA:"
            )
            return response.text.strip()
        except Exception as e:
            return f"Error: {str(e)}. Unataka tuendelee 'Offline' kusaidiana na PC yako?"
