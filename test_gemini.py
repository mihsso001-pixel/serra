from google import genai

# WEKA KEY YAKO MPYA HAPA (Siri yako!)
API_KEY = "AIzaSyBmMWiZSfyzlGyRGoMTZUazbAH8HOv6ESI"

def test_serra():
    print("--- SERRA BRAIN: FINAL RECOVERY ---")
    try:
        client = genai.Client(api_key=API_KEY)
        # Force v2 by using short name
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Confirm system is online."
        )
        print(f"\n🚀 JIBU: {response.text.strip()}")
        print("\n[SUCCESS] Serra is back online!")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    test_serra()
