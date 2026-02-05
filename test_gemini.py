from google import genai

# Weka ile API Key yako mpya hapa (Hakikisha haina space)
API_KEY = "PASTE_YOUR_KEY_HERE"

def test_serra():
    print("--- SERRA BRAIN: ULTIMATE CONNECTION ---")
    try:
        # 1. Tunatengeneza client
        client = genai.Client(api_key=API_KEY)
        
        print("Mawasiliano: Inapiga simu Google Headquarters...")

        # 2. TUNATUMIA MBINU MPYA KABISA (Hapa haitatumia v1beta)
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Confirm system: Say 'Serra 1.5 is Online'"
        )

        print("\n" + "💎"*10)
        print(f"JIBU LA SERRA: {response.text.strip()}")
        print("💎"*10)
        print("\nSUCCESS! Mchawi kashindwa safari hii.")

    except Exception as e:
        # Kama ikikataa hapa, tutaiambia itupe list ya models zilizopo
        print(f"\n❌ Error: {e}")
        print("\nInajaribu kutafuta models zilizopo kwenye akaunti yako...")
        try:
            for m in client.models.list():
                print(f"Model inayopatikana: {m.name}")
        except:
            pass

if __name__ == "__main__":
    test_serra()
