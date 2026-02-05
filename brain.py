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
        q = query.lower()
        
        # 1. SEARCH PROTOCOL (Search chochote)
        if any(word in q for word in ["search", "tafuta", "nenda", "google"]):
            # Tunachukua maneno baada ya neno 'search' au 'tafuta'
            search_query = q.replace("search", "").replace("tafuta", "").replace("google", "").strip()
            if search_query:
                url = f"https://www.google.com/search?q={search_query}"
                webbrowser.open(url)
                return f"Neural Search initiated for: {search_query}. I've opened the results for you."

        # 2. OPEN APP PROTOCOL (Fungua App yoyote)
        if "open" in q or "fungua" in q:
            app_name = q.replace("open", "").replace("fungua", "").strip()
            
            # Apps za kawaida (Dictionary ya haraka)
            common_apps = {
                "chrome": "start chrome",
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "vlc": "vlc.exe",
                "word": "start winword",
                "excel": "start excel",
                "powerpoint": "start powerpnt",
                "discord": "start discord",
                "spotify": "start spotify"
            }
            
            if app_name in common_apps:
                subprocess.Popen(common_apps[app_name], shell=True)
                return f"System Protocol: {app_name.capitalize()} is now active."
            else:
                # Kama app haipo kwenye list, anajaribu kuifungua moja kwa moja kwa jina lake
                try:
                    subprocess.Popen(f"start {app_name}", shell=True)
                    return f"Attempting to launch {app_name} from system binaries."
                except:
                    return f"App '{app_name}' not found. Please specify the path or ensure it is installed."

        # 3. CORRECTION & ANALYSIS (Anatakiwa atimize alichoambiwa)
        if any(word in q for word in ["sahihisha", "fix", "correct", "fanya"]):
            return None # Hii itapelekwa kwa AI (Llama 3.3) ifanye kazi hiyo

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
