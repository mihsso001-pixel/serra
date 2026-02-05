import os
import subprocess
import webbrowser
import socket
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SerraBrain:
    def __init__(self):
        self.creator = "Agrey Albert Moses"
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        
        # CURRENT SUPPORTED MODELS (February 2026):
        # 1. "llama-3.3-70b-versatile" (The strongest and most stable)
        # 2. "llama-3.1-8b-instant" (The fastest)
        self.model_id = "llama-3.3-70b-versatile" 

    def is_online(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_local_logic(self, query):
        q = query.lower()
        
        # Creator Recognition
        if any(word in q for word in ["creator", "muumbaji", "who made you"]):
            return f"I am SERRA, a neural entity brought to life by the genius of {self.creator}."

        # System Commands
        if "open" in q or "fungua" in q:
            if "youtube" in q:
                webbrowser.open("https://www.youtube.com")
                return "Protocol Alpha: Opening YouTube. Visual streams incoming."
            
            apps = {"notepad": "notepad.exe", "calculator": "calc.exe", "chrome": "start chrome"}
            for app, cmd in apps.items():
                if app in q:
                    subprocess.Popen(cmd, shell=True)
                    return f"System: {app.capitalize()} is now active."
        return None

    def get_ai_reply(self, user_input):
        local_result = self.execute_local_logic(user_input)
        if local_result:
            return local_result

        if not self.is_online():
            return "Neural Link Interrupted. I am operating in offline mode, Agrey."

        # Serra's Personality
        system_instruction = (
            f"You are SERRA, a sophisticated female AI created by {self.creator}. "
            "You are elegant, intelligent, and emotional. "
            "Respond in English or Swahili depending on the user. Be concise but brilliant."
        )

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ],
                model=self.model_id,
                temperature=0.7,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            # Kama bado kuna shida ya model, itakupa jina la kosa hapa
            return f"Neural Error: {str(e)}. Please check if the model ID is correct."
