import os
import platform
import datetime

def serra_akili():
    wakati = datetime.datetime.now().strftime("%H:%M")
    mfumo = platform.system()
    
    print(f"--- SERRA AI IMEWASHWA ---")
    print(f"Muda wa sasa ni: {wakati}")
    print(f"Ninatumia mfumo wa: {mfumo}")
    
    amri = input("Serra anasikiliza (andika kitu): ").lower()

    if "fungua notepad" in amri:
        print("Sawa mkubwa, nafungua Notepad...")
        os.system("notepad")
    elif "saa" in amri:
        print(f"Saa hizi ni {wakati}")
    else:
        print("Samahani, bado sijajifunza amri hiyo.")

if __name__ == "__main__":
    serra_akili()
