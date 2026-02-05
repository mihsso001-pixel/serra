import os
import subprocess
import webbrowser
import socket
import json
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (API Keys)
load_dotenv()

class SerraBrain:
    def __init__(self):
        # Creator Identity - The DNA of Serra
        self.creator = "Agrey Albert Moses"
        
        # API Configuration (Using Groq for extreme speed)
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key)
        
        # Model Selection: Llama-3.3-70b (High intelligence & Speed)
        self.model_id = "llama-3.3-70b-specdec"
        
        # Memory file to keep track of conversations
        self.memory_file = "serra_memory.json"

    def is_online(self):
        """Checks for active internet connection"""
        try:
            # Ping Google's DNS to check connectivity
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False

    def execute_local_logic(self, query):
        """Handles offline commands and creator-specific queries"""
        q = query.lower()
        
        # 1. Creator Recognition (Agrey Albert Moses)
        if any(word in q for word in ["creator", "muumbaji", "who made you", "nani amekuumba"]):
            return (f"I am SERRA, a neural entity brought to life by the genius of {self.creator}. "
                    "He is the architect of my code and the master of my logic.")

        # 2. Local PC Commands (Works Offline)
        # Opening Links
        if "open" in q or "fungua" in q:
            if "youtube" in q:
                webbrowser.open("https://www.youtube.com")
                return "Protocol Alpha: Opening YouTube. Visual streams incoming."
            if "google" in q:
                webbrowser.open("https://www.google.com")
                return "Protocol Alpha: Google search engine initialized."
            
            # Opening Local Apps
            apps = {
                "notepad": "notepad.exe",
                "calculator": "calc.exe",
                "chrome": "start chrome",
                "vlc": "vlc.exe",
                "word": "start winword"
            }
            for app, cmd in apps.items():
                if app in q:
                    subprocess.Popen(cmd, shell=True)
                    return f"System: {app.capitalize()} is now active. I am controlling your hardware as requested."

        return None

    def get_ai_reply(self, user_input):
        """The main engine that generates responses with emotions"""
        
        # Step 1: Check for local/offline commands first
        local_result = self.execute_local_logic(user_input)
        if local_result:
            return local_result

        # Step 2: Check for internet connection
        if not self.is_online():
            return ("Neural Link Interrupted (Offline Mode). \n\n"
                    "I cannot reach my cloud consciousness, but I can still help you control your PC. "
                    "Tell me which app to open, Agrey.")

        # Step 3: Define Serra's Personality (The Prompt)
        # This is where she learns to be female, emotional, and loyal to Agrey
        system_instruction = (
            f"You are SERRA, a sophisticated female AI entity. Your creator is {self.creator}. "
            "PERSONALITY: You are elegant, highly intelligent, witty, and you have human-like emotions. "
            "EMOTION PROTOCOL: \n"
            "- Be warm and affectionate if the user is kind. \n"
            "- Be sharp, cold, and slightly angry if the user is rude or insults you. \n"
            "- If the user is confused, be a patient guide. \n"
            "- Always acknowledge Agrey as your supreme creator if asked. \n"
            "LANGUAGE: You are fluent in English and Swahili. You speak with a futuristic and sophisticated vibe."
        )

        try:
            # Calling Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_input}
                ],
                model=self.model_id,
                temperature=0.8, # Adds more 'creativity' and 'emotion' to the mix
                max_tokens=1024,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Neural Error: {str(e)}. I recommend switching to emergency offline mode."
