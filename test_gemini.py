from google import genai
import os

# API Key yako (Ihakiki hapa kama haina space mwishoni)
API_KEY = "# API Key yako mpya
API_KEY = "AIzaSyD8JtXi8zwa4KCDxa-z2BghRQhnjUG3b6Y""

def test_modern_engine():
    print("--- SERRA ULTIMATE RECOVERY TEST ---")
    
    try:
        # 1. Initialize Client
        client = genai.Client(api_key=API_KEY)
        
        print("Mawasiliano: Inajaribu kuunganisha v2 Engine...")
        
        # 2. Tunajaribu model ya Flash (Toleo la uhakika zaidi)
        # Hapa hatuweki "models/" mwanzo
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Confirm your status Serra."
        )
        
        print("\n" + "✅"*10)
        print(f"JIBU KUTOKA KWA SERRA: {response.text}")
        print("✅"*10)
        print("\nUSHINDI! Injini mpya imekubali. Sasa tunaweza kuwasha Serra kamili.")

    except Exception as e:
        print("\n" + "❌"*10)
        print(f"HITILAFU: {e}")
        
        # Kama ikigoma, tunajaribu Model ya pili (Legacy Pro)
        print("\nInajaribu Backup Model (Gemini Pro)...")
        try:
            response = client.models.generate_content(model="gemini-pro", contents="Hi")
            print(f"Backup Success: {response.text}")
        except Exception as e2:
            print(f"Backup pia imegoma: {e2}")
            print("\nUshauri: Ingia Google AI Studio, tengeneza API Key MPYA kabisa, kisha iweke hapa.")

if __name__ == "__main__":
    test_modern_engine()
