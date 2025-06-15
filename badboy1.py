import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import pywhatkit
import cv2
import urllib.parse  # For URL encoding

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"You said: {query}")
    except Exception:
        speak("Sorry, I didn't catch that.")
        return ""
    return query.lower()

def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am Jarvis. Say 'Wake up Jarvis' to activate me.")

def open_camera():
    speak("Opening camera.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Jarvis Camera', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def search_zomato(item):
    encoded_item = urllib.parse.quote_plus(item)
    url = f"https://www.zomato.com/search?query={encoded_item}"
    speak(f"Searching Zomato for {item}")
    webbrowser.open(url)

def run_jarvis():
    wish_user()

    while True:
        command = take_command()

        if 'wake up jarvis' in command:
            speak("I am ready.")
            while True:
                query = take_command()

                if 'search google for' in query:
                    search_query = query.replace("search google for", "").strip()
                    speak(f"Searching Google for {search_query}")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")

                elif 'search youtube for' in query or 'play on youtube' in query:
                    search_query = query.replace("search youtube for", "").replace("play on youtube", "").strip()
                    speak(f"Searching YouTube for {search_query}")
                    pywhatkit.playonyt(search_query)

                elif 'search zomato for' in query:
                    item = query.replace("search zomato for", "").strip()
                    search_zomato(item)

                elif 'open camera' in query:
                    open_camera()

                elif 'time' in query:
                    time = datetime.datetime.now().strftime("%H:%M:%S")
                    speak(f"The time is {time}")

                elif 'exit' in query or 'sleep' in query:
                    speak("Going to sleep. Say 'Wake up Jarvis' to activate me again.")
                    break

# Start the assistant
run_jarvis()