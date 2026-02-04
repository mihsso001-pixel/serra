import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import sys

# 1. SETUP: Sauti ya Serra
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# Unaweza kubadili voices[0] kuwa voices[1] kwa sauti ya kike
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"Serra: {text}")
    engine.say(text)
    engine.runAndWait()

# 2. LISTENING: Uwezo wa kusikia
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query.lower()

# 3. BRAIN: Maelekezo ya kazi
def run_serra():
    command = take_command()
    
    if 'play' in command:
        song = command.replace('play', '')
        speak('playing ' + song)
        pywhatkit.playonyt(song)
        
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time)
        
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        speak(info)
        
    elif 'joke' in command:
        speak(pyjokes.get_joke())
        
    elif 'open notepad' in command:
        speak('Opening Notepad for you')
        os.system('notepad')

    elif 'open chrome' in command:
        speak('Opening Google Chrome')
        os.startfile('C:/Program Files/Google/Chrome/Application/chrome.exe') # Hakikisha path ni sahihi

    elif 'stop' in command or 'exit' in command:
        speak('Goodbye Boss, have a productive day!')
        sys.exit()

    else:
        speak('Please say the command again.')

# 4. START: Kuwasha mfumo
if __name__ == "__main__":
    speak("Serra system activated. How can I help you today?")
    while True:
        run_serra()
