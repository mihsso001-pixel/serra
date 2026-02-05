from google import genai
import sys

# API Key yako
API_KEY = "AIzaSyD8JtXi8zwa4KCDxa-z2BghRQhnjUG3b6Y"

def test_modern_engine():
    print("--- SERRA MODERN ENGINE TEST (v3) ---")
    
    try:
        # 1. Initialize Client (Muundo mpya huu)
        client = genai.Client(api_key=API_KEY)
        
        print("Neural Link: Connecting to Google GenAI Servers...")
        
        # 2. Generate Content (Tunatumia gemini-1.5-flash ambayo ni stable zaidi kwa sasa)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Hello! Confirm you are the new Serra Brain by saying: 'New Engine Online!'"
        )
        
        print("\n" + "="*40)
        print(f"RESPONSE FROM AI: {response.text}")
        print("="*40)
        print("\n[SUCCESS] Injini mpya inafanya kazi bila makosa!")

    except Exception as e:
        print("\n" + "!"*40)
        print(f"FAILURE: Kuna hitilafu imetokea.")
        print(f"Error Details: {e}")
        print("!"*40)
        print("\nUshauri: Hakikisha umepiga 'pip install google-genai' na internet ipo poa.")

if __name__ == "__main__":
    test_modern_engine()
