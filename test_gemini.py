from google import genai
import time

# --- USALAMA NA IDENTITY ---
API_KEY = "AIzaSyD8JtXi8zwa4KCDxa-z2BghRQhnjUG3b6Y"

def test_serra_brain():
    print("--- SERRA NEURAL LINK: INITIALIZING TEST ---")
    
    try:
        # 1. Initialize Client (V3 Modern Engine)
        client = genai.Client(api_key=API_KEY)
        
        print("Link Status: Connecting to Gemini Servers...")
        
        # 2. Subiri jibu (Tumeseti gemini-1.5-flash ambayo ndio bora kwa sasa)
        start_time = time.time()
        
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents="Confirm identity. Who are you?"
        )
        
        end_time = time.time()
        latency = round(end_time - start_time, 2)

        print("\n" + "✅"*15)
        print(f"BRAIN RESPONSE: {response.text.strip()}")
        print(f"RESPONSE TIME: {latency} seconds")
        print("✅"*15)
        
        print("\n[SUCCESS] Serra Brain is Online and 100% Functional!")

    except Exception as e:
        print("\n" + "❌"*15)
        print("LINK FAILURE: Brain not responding.")
        print(f"Detailed Error: {e}")
        print("❌"*15)
        print("\nUshauri: Kama inasema 'API Key not found', hakikisha hakuna space")
        print("ndani ya API_KEY string. Kama inasema '404', basi Google bado")
        print("wanai-activate hii key kwenye servers zao (Subiri dakika 5).")

if __name__ == "__main__":
    test_serra_brain()
