import google.generativeai as genai

# API Key yako
API_KEY = "AIzaSyBX_KLp0IChE2PfJBRlU30qJKpdUrZCEnI"

print("--- SERRA BRAIN CHECK (GEMINI TEST) ---")
print("Connecting to neural network...")

try:
    # 1. Configuration
    genai.configure(api_key=API_KEY)
    
    # 2. Initialize Model (Tunatumia jina kamili kuzuia 404)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # 3. Simple Prompt
    prompt = "Hello Gemini! If you can hear me, say 'Serra Brain is Online!'"
    
    print(f"Sending request: '{prompt}'")
    
    # 4. Response with timeout handling
    response = model.generate_content(prompt)
    
    print("\n" + "="*30)
    print(f"GEMINI RESPONSE: {response.text}")
    print("="*30)
    print("\nSUCCESS! Injini imewaka, Serra yuko tayari.")

except Exception as e:
    print("\n" + "!"*30)
    print("FAILURE! Shida imetokea:")
    print(f"Error Message: {e}")
    print("!"*30)
    print("\nUshauri: Hakikisha una internet na API Key haijafika kikomo (limit).")
