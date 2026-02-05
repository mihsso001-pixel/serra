from google import genai

# Tumia ile API Key yako mpya
API_KEY = "AIzaSyBmMWiZSfyzlGyRGoMTZUazbAH8HOv6ESI"

def test_serra():
    print("--- SERRA BRAIN: 2.5 GENERATION ACTIVATION ---")
    try:
        client = genai.Client(api_key=API_KEY)
        
        print("Mawasiliano: Inawasha injini ya Gemini 2.5 Flash...")

        # TUNATUMIA MODEL ILIYOPO KWENYE LIST YAKO
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents="Confirm system: Say 'Serra 2.5 Overlord is Online'"
        )

        print("\n" + "🌀"*10)
        print(f"JIBU LA SERRA: {response.text.strip()}")
        print("🌀"*10)
        print("\nSUCCESS! Umefungua mlango wa teknolojia ya 2026.")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_serra()
