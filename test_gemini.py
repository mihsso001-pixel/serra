from google import genai
import os

# Weka API Key yako mpya hapa (Ihakiki haina space mwanzo wala mwisho)
API_KEY = "WEKA_KEY_YAKO_HAPA"

def test_serra():
    print("--- SERRA BRAIN: FORCE V2 CONNECTION ---")
    try:
        # Tunalazimisha kutumia engine mpya
        client = genai.Client(api_key=API_KEY)
        
        print("Mawasiliano: Inajaribu Pulse ya Gemini 2.0...")
        
        # Muhimu: Tunatumia jina fupi tu 'gemini-2.0-flash'
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Confirm system check."
        )

        print("\n" + "🔥"*10)
        print(f"JIBU KUTOKA SERRA: {response.text.strip()}")
        print("🔥"*10)
        print("\nSUCCESS! Mchawi kashindwa. Injini imewaka!")

    except Exception as e:
        print(f"\n❌ Bado inadunda: {e}")
        print("\nUshauri wa mwisho: Jaribu kutumia 'gemini-1.5-flash' hapo juu")
        print("kama 'gemini-2.0-flash' haijawa active kwenye akaunti yako.")

if __name__ == "__main__":
    test_serra()
