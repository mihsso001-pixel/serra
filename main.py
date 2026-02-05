import sys
from brain import SerraBrain
from interface import SerraInterface

def launch_serra():
    try:
        # 1. Anzisha akili ya Serra (Gemini + PC Control)
        print("Initializing Neural Core...")
        brain = SerraBrain()

        # 2. Anzisha mwili wa Serra (UI + Sauti)
        # Tunapitisha 'brain' ndani ya interface ili iweze kuwasiliana
        print("Establishing Neural Interface...")
        app = SerraInterface(brain)

        # 3. Washa programu
        print("SERRA is now online.")
        app.mainloop()

    except Exception as e:
        print(f"Failed to launch SERRA: {e}")
        sys.exit(1)

if __name__ == "__main__":
    launch_serra()
