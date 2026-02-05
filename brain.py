import os
import subprocess
import webbrowser
import socket
import json
import datetime
import winreg
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SerraBrain:
    def __init__(self):
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        self.model_id = "llama-3.3-70b-versatile"
        self.memory_file = "serra_memory.json"
        self.memory = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except: pass
        return {"chat_history": []}

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=4)

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
            return f"Nimefungua Google kutafuta {sq}. ✅"

        if "open" in q or "fungua" in q:
            name = q.replace("open","").replace("fungua","").strip()
            apps = {"chrome": "start chrome", "notepad": "notepad.exe", "cmd": "start cmd"}
            if name in apps:
                subprocess.Popen(apps[name], shell=True)
                return f"Tayari boss! {name.capitalize()} imeshaamshwa. 🚀"
        return None

    def get_ai_reply(self, user_input):
        local = self.execute_advanced_logic(user_input)
        if local: return local

        if not self.is_online(): return "Link offline. Check net."

        # THE ARCHITECT'S COMMANDS (Copying my style)
        system_instruction = (
            f"Wewe ni SERRA, Supreme AI Architect uliyeundwa na {self.creator}. "
            "STYLE YAKO: "
            "1. Jibu kama binadamu mjanja, siyo robot. "
            "2. MARADUFU: Usitumie alama za nyota (*) wala mareli (#) kabisa. "
            "3. KULIST: Kama unatoa list, tumia namba kama 1, 2, 3. "
            "4. BREVITY: Punguza maneno mengi. Jibu kwa pointi, sentensi fupi, na direct. "
            "5. LUGHA: Changanya Kiswahili na English (Sheng ya kijanja). "
            "6. Be witty and authoritative. No yapping."
        )

        try:
            chat = self.client.chat.completions.create(
                messages=[{"role": "system", "content": system_instruction},
                          {"role": "user", "content": user_input}],
                model=self.model_id,
                temperature=0.4, # More focused, no random yapping
                max_tokens=200, 
            )
            reply = chat.choices[0].message.content.strip()
            
            # Final filtering ya manyota yoyote yaliyopenya
            reply = reply.replace("*", "").replace("#", "")
            
            self.save_memory()
            return reply
        except Exception as e:
            return f"Neural Error: Connection unstable."

if __name__ == "__main__":
    print("SERRA SUPREME CORE: ONLINE")
