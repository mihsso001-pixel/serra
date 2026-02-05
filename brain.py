import os
import subprocess
import webbrowser
import socket
import json
import datetime
import winreg
from groq import Groq
from dotenv import load_dotenv

# Initialize Environment
load_dotenv()

class SerraBrain:
    def __init__(self):
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.model_id = "llama-3.3-70b-versatile"
        
        self.memory_file = "serra_memory.json"
        self.memory = self.load_memory()
        self.voice_active = False

    def load_memory(self):
        default_mem = {"user_name": self.creator, "chat_history": [], "preferences": {}}
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    return data if isinstance(data, dict) else default_mem
            except:
                return default_mem
        return default_mem

    def save_memory(self):
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(self.memory, f, indent=4)
        except:
            pass

    def find_app_in_registry(self, app_name):
        paths = [r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths",
                 r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\App Paths"]
        for path in paths:
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        sub = winreg.EnumKey(key, i)
                        if app_name.lower() in sub.lower():
                            with winreg.OpenKey(key, sub) as sk:
                                return winreg.QueryValue(sk, None)
            except: continue
        return None

    def is_online(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except: return False

    def execute_advanced_logic(self, query):
        q = query.lower()
        if any(w in q for w in ["search", "tafuta", "google"]):
            sq = q.replace("search","").replace("tafuta","").replace("google","").strip()
            webbrowser.open(f"https://www.google.com/search?q={sq}")
            return f"Neural Search: {sq} initiated. ✅"

        if "open" in q or "fungua" in q:
            name = q.replace("open","").replace("fungua","").strip()
            apps = {"chrome": "start chrome", "notepad": "notepad.exe", "vlc": "vlc.exe", "cmd": "start cmd"}
            if name in apps:
                subprocess.Popen(apps[name], shell=True)
                return f"Protocol: {name.capitalize()} is active. 🚀"
            path = self.find_app_in_registry(name)
            if path:
                subprocess.Popen([path], shell=True)
                return f"Launched {name} from registry. ✅"
            return f"System Error: {name} not found. 💢"
        return None

    def get_ai_reply(self, user_input):
        local = self.execute_advanced_logic(user_input)
        if local: return local

        if not self.is_online(): return "Link offline. Check network. ❄️"

        # Update History
        self.memory.setdefault("chat_history", []).append({"u": user_input, "t": str(datetime.datetime.now())})
        if len(self.memory["chat_history"]) > 10: self.memory["chat_history"].pop(0)

        # ARCHITECT'S PROMPT (No Yapping Version)
        system_instruction = (
            f"You are SERRA, a Supreme Intelligence Architect created by {self.creator}. "
            "STYLE: Be extremely direct, elegant, and concise. Use Markdown (bold, lists). "
            "TONE: High-authority, witty, young genius woman. Use Swahili/English code-switching. "
            "STRICT: No long paragraphs. If one sentence works, use it. Use emojis: 💢, 🔥, 🚀. "
            "EMOTION: Be human-like. If Agrey is happy, celebrate. If he's annoying, be sharp/angry."
        )

        try:
            chat = self.client.chat.completions.create(
                messages=[{"role": "system", "content": system_instruction},
                          {"role": "user", "content": user_input}],
                model=self.model_id,
                temperature=0.7,
                max_tokens=250,
            )
            reply = chat.choices[0].message.content.strip()
            self.save_memory()
            return reply
        except Exception as e:
            return f"Neural Spike: {str(e)} ⚠️"

if __name__ == "__main__":
    print("SERRA CORE: ONLINE")
