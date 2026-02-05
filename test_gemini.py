from google import genai
import time

# API Key yako mpya uliyotupa
API_KEY = "AIzaSyD8JtXi8zwa4KCDxa-z2BghRQhnjUG3b6Y"

def test_serra_brain():
    print("--- SERRA NEURAL LINK: V2 ENGINE TEST ---")
    
    try:
        # 1. Initialize Client
        client = genai.Client(api_key=API_KEY)
        
        print("Link Status: Connecting to High-Speed Pulse...")
        
        # 2. Hapa ndio siri: Tunatumia jina la model bila "models/" 
        # na tunatumia 'gemini-2.0-flash' (Toleo la sasa hivi 2026)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Say: Serra System is fully operational!"
        )

        print("\n" + "🚀"*15)
        print(f"BRAIN RESPONSE: {response.text.strip()}")
        print("🚀"*15)
        print("\n[SUCCESS] Serra is now using the 2026 Pulse Engine!")

    except Exception as e:
        print("\n" + "❌"*15)
        print("LINK FAILURE!")
        print(f"Detailed Error: {e}")
        print("❌"*15)
        print("\nJaribu kubadilisha model kuwa 'gemini-1.5-flash' kama 2.0 haipo.")

if __name__ == "__main__":
    test_serra_brain()
