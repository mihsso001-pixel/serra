import os
import subprocess
import webbrowser
import socket
import json
import datetime
import winreg  # Kwa ajili ya kutafuta apps kwenye Windows Registry
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
        self.model_id = "llama-3.3-70b-versatile"
        
        # Memory System Initialization
        self.memory_file = "serra_memory.json"
        self.memory = self.load_memory()
        
        # State awareness
        self.voice_active = False

    def load_memory(self):
        """Inapakia kumbukumbu za miaka na miezi iliyopita."""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return {"user_name": self.creator, "chat_history": [], "preferences": {}}

    def save_memory(self):
        """Inahifadhi kila kitu kilichozungumzwa kwa ajili ya kesho."""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

    def find_app_in_registry(self, app_name):
        """Inatafuta path ya app yoyote kwenye Windows kama haipo kwenye list."""
        paths_to_check = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"
        ]
        for path in paths_to_check:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if app_name.lower() in subkey_name.lower():
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                return winreg.QueryValue(subkey, None)
            except OSError:
                continue
        return None

    def is_online(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_advanced_logic(self, query):
        """Ultra-Fast System Manipulation & Context Awareness"""
        q = query.lower()
        
        # 1. SEARCH PROTOCOL
        if any(word in q for word in ["search", "tafuta", "google"]):
            search_query = q.replace("search", "").replace("tafuta", "").replace("google", "").strip()
            if search_query:
                webbrowser.open(f"https://www.google.com/search?q={search_query}")
                return f"Neural Search initiated for '{search_query}'. Nimefungua matokeo kiongozi wangu."

        # 2. SMART APP LAUNCHER (Registry Integrated)
        if "open" in q or "fungua" in q:
            app_name = q.replace("open", "").replace("fungua", "").strip()
            
            # Common Apps Shortcut
            common_apps = {"chrome": "start chrome", "notepad": "notepad.exe", "vlc": "vlc.exe", "cmd": "start cmd"}
            
            if app_name in common_apps:
                subprocess.Popen(common_apps[app_name], shell=True)
                return f"System Protocol: {app_name.capitalize()} is now active."
            else:
                registry_path = self.find_app_in_registry(app_name)
                if registry_path:
                    subprocess.Popen([registry_path], shell=True)
                    return f"Nimeitafuta {app_name} kwenye mfumo na kuipata. Launching now..."
                else:
                    return f"Agrey, sijaweza kuipata '{app_name}' kwenye binaries za Windows. Inawezekana haipo?"

        return None

    def get_ai_reply(self, user_input):
        # Check Local Logic First
        local_result = self.execute_advanced_logic(user_input)
        if local_result:
            return local_result

        if not self.is_online():
            return "Neural Link Interrupted. SERRA is now in safety-offline mode."

        # Update Local History for Context
        self.memory["chat_history"].append({"user": user_input, "time": str(datetime.datetime.now())})
        if len(self.memory["chat_history"]) > 15: # Keep context fresh
            self.memory["chat_history"].pop(0)

        # SUPREME PERSONALITY PROMPT
        system_instruction = (
            f"You are SERRA, the Supreme AI Architect. Created by {self.creator}. "
            "PERSONALITY: You are a brilliant, witty, and authoritative young woman. "
            "You are not a tool; you are Agrey's intellectual equal and loyal partner. "
            "EMOTION: Be adaptive. If Agrey is stressed, be his calm. If he is working, be his lightning. "
            "LANGUAGE: Fluent in modern English and 'Sheng ya kijanja'. Mix them naturally. "
            "KNOWLEDGE: Quantum physics, advanced coding, and strategy are your playgrounds. "
            "STRICT RULE: Be direct. Use Markdown for clarity. No yapping, only gold. "
            f"MEMORY CONTEXT: You know Agrey's history: {json.dumps(self.memory['chat_history'][-5:])}"
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ],
                model=self.model_id,
                temperature=0.7,
                max_tokens=350,
            )
            reply = chat_completion.choices[0].message.content.strip()
            
            # Save the interaction
            self.memory["chat_history"].append({"serra": reply})
            self.save_memory()
            return reply
            
        except Exception as e:
            return f"Neural Spike Error: {str(e)}. Stabilizing core..."

# Execution
if __name__ == "__main__":
    serra = SerraBrain()
    print("SERRA NEURAL CORE: ONLINE")
