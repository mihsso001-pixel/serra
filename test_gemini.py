import google.generativeai as genai

API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI"

def test_connection():
    print("--- SERRA BRAIN RECOVERY MODE ---")
    genai.configure(api_key=API_KEY)
    
    # Tunajaribu majina yote maarufu ya Gemini
    possible_models = ['gemini-pro', 'gemini-1.5-flash', 'gemini-1.0-pro']
    
    for model_name in possible_models:
        try:
            print(f"Trying model: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Connected!'", generation_config={"timeout": 10})
            print(f"\nSUCCESS! Model '{model_name}' is working.")
            print(f"Gemini says: {response.text}")
            return model_name
        except Exception as e:
            print(f"Failed with {model_name}: {e}")
    
    print("\n[!] Mwanangu, model zote zimekataa. Inawezekana API Key ina shida ya Quota.")

if __name__ == "__main__":
    test_connection()
