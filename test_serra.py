import os
import webbrowser
import google.generativeai as genai

# Weka API Key yako
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def test_serra():
    print("--- SERRA SILENT TEST MODE ---")
    print("Andika amri (mfano: 'open calculator', 'who are you', 'exit')")
    
    while True:
        query = input("\nMaster (Type here): ").lower()
        
        if 'exit' in query:
            print("Serra: Shutting down test mode.")
            break
            
        # 1. Test Amri za PC
        if 'calculator' in query:
            print("Serra: Opening Calculator...")
            os.system("calc")
            
        elif 'word' in query:
            print("Serra: Opening Word...")
            os.system("start winword")
            
        elif 'google' in query:
            print("Serra: Opening Google...")
            webbrowser.open("https://www.google.com")
            
        # 2. Test Akili ya Gemini (API)
        else:
            print("Serra: Thinking...")
            try:
                response = model.generate_content(f"You are Serra AI. Answer briefly: {query}")
                print(f"Serra says: {response.text}")
            except Exception as e:
                print(f"Gemini Error: {e}")

if __name__ == "__main__":
    test_serra()
