from google import genai

# Hii ndio key yenyewe kutoka kwenye picha yako (Case Sensitive)
API_KEY = "AIzaSyD8JtXi8zwa4KCDxa-z2BghRQhnjUG3b6Y"

def test_serra():
    print("--- SERRA BRAIN CHECK: FINAL ATTEMPT ---")
    try:
        # Tunatumia Client ya kisasa (SDK v3)
        client = genai.Client(api_key=API_KEY)
        
        print("Mawasiliano: Inapeleka ombi kwa Gemini 2.0...")
        
        # Hapa tunatumia gemini-2.0-flash (Injini mpya kabisa ya 2026)
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Confirm your status. Use exactly five words."
        )

        print("\n" + "🚀"*10)
        print(f"JIBU LA SERRA: {response.text.strip()}")
        print("🚀"*10)
        print("\nSUCCESS! Sasa tuko tayari kuwasha Serra kamili.")

    except Exception as e:
        print(f"\n❌ Error imetokea: {e}")
        print("\nUshauri: Hakikisha umepiga 'pip install google-genai' kwenye CMD yako.")

if __name__ == "__main__":
    test_serra()
