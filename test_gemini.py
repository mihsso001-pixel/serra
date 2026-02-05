from google import genai

# WEKA KEY MPYA HAPA NDANI YA " "
API_KEY = "AIzaSyBmMWiZSfyzlGyRGoMTZUazbAH8HOv6ESI"

def test_serra():
    print("--- SERRA BRAIN CHECK: FINAL ATTEMPT ---")
    try:
        client = genai.Client(api_key=API_KEY)
        print("Mawasiliano: Inapeleka ombi...")
        
        # Jaribu model ya 1.5 kama 2.0 bado haijawa active kwako
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Confirm status"
        )

        print(f"\n🚀 JIBU: {response.text.strip()}")
        print("\nSUCCESS! Sasa weka hii key kwenye main.py")

    except Exception as e:
        print(f"\n❌ Bado kuna Error: {e}")

if __name__ == "__main__":
    test_serra()
