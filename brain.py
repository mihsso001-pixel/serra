import os
import json
import subprocess
import webbrowser
import pyautogui
from google import genai
from dotenv import load_dotenv

# Pakia siri kutoka kwenye .env
load_dotenv()

class SerraBrain:
    def __init__(self):
        # Setup Gemini Client
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_id = "gemini-2.0-flash" # Toleo la kisasa kabisa
        
        # Setup Memory
        self.memory_file = "serra_memory.json"
        self.chat_history = self.load_memory()

    def load_memory(self):
        """Inapakia kumbukumbu ya zamani kutoka kwenye file la JSON"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_memory(self):
        """Inahifadhi maongezi ya sasa kwenye file ili asisahau"""
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.chat_history[-40:], f, indent=4) # Tunatunza maongezi 40 tu yasizidi uzito

    def execute_pc_command(self, query):
        """Hapa ndipo Serra anapata mikono ya ku-control PC yako"""
        q = query.lower()
        
        # 1. Kufungua Programu za Windows
        if "open" in q or "fungua" in q:
            apps = {
                "chrome": "start chrome",
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "cmd": "start cmd",
                "vlc": "vlc.exe",
                "word": "start winword",
                "excel": "start excel"
            }
            for app, command in apps.items():
                if app in q:
                    subprocess.Popen(command, shell=True)
                    return f"Neural link established with {app.capitalize()}. Access granted."

        # 2. Kutafuta Mtandaoni (Web Search)
        if "search" in q or "tafuta" in q:
            search_query = q.replace("search", "").replace("tafuta", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            return f"Scanning the global network for: {search_query}. Results are on your screen."

        # 3. Mouse Control (Basic)
        if "move mouse" in q:
            pyautogui.moveRel(0, -200, duration=0.5)
            return "Manual override: Cursor repositioned."

        return None # Kama sio amri ya PC, rudi kwenye AI ya kawaida

    def generate_response(self, user_input):
        """Inatengeneza jibu la Serra kama Gemini"""
        
        # Angalia kwanza kama ni amri ya PC
        pc_action = self.execute_pc_command(user_input)
        if pc_action:
            return pc_action

        # Kama ni maongezi, tumia Gemini Persona
        persona = (
            "You are SERRA, a brilliant and witty AI twin of Gemini. "
            "You have direct control over the user's computer. "
            "Your tone is professional, sharp, and slightly futuristic. "
            "If you perform a PC action, report it as 'System Protocol Executed'."
        )

        # Tengeneza Prompt yenye kumbukumbu
        full_prompt = f"{persona}\n\nHistory:\n{self.chat_history}\n\nUser: {user_input}\nSERRA:"

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=full_prompt
            )
            reply = response.text.strip()
            
            # Hifadhi kwenye kumbukumbu
            self.chat_history.append({"user": user_input, "serra": reply})
            self.save_memory()
            
            return reply
        except Exception as e:
            return f"Neural Error: Connection to the core was interrupted. ({str(e)})"
