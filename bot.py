import speech_recognition as sr
import pyttsx3
import requests
import json
import re
import os
import subprocess
import webbrowser

# ================== CONFIGURATION ==================
API_KEY = os.getenv("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")  # আপনার API Key env var-এ রাখুন
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://your-site-or-project.com",
    "X-Title": "Jarvis Assistant"
}

# ================== INITIALIZATION ==================
engine = pyttsx3.init()
engine.setProperty("rate", 180)

recognizer = sr.Recognizer()

# ================== SPEAK & LISTEN ==================
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # mic calibration
        print("🎤 Listening...")
        try:
            audio = recognizer.listen(source, phrase_time_limit=15)  # allow longer speech
        except sr.WaitTimeoutError:
            print("⏳ Listening timeout.")
            return None
    try:
        print("🔍 Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("⚠️ Could not understand audio")
        return None
    except sr.RequestError as e:
        print("❌ Speech Recognition Error:", str(e))
        return None

# ================== CLEANING ==================
def clean_response(text):
    text = re.sub(r'\\n|\n|\r', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

# ================== CHAT WITH DEEPSEEK ==================
def chat_with_deepseek(prompt):
    try:
        data = {
            "model": "deepseek/deepseek-r1-zero:free",
            "messages": [
                {
                    "role": "system",
                    "content": "You are Jarvis, an intelligent AI assistant. Speak clearly and in a natural tone. Respond in the same language the user speaks."
                },
                {"role": "user", "content": prompt}
            ]
        }
        response = requests.post(API_URL, headers=HEADERS, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            raw_answer = result["choices"][0]["message"]["content"]
            print("🧠 AI Raw Response:", raw_answer)
            return clean_response(raw_answer)
        else:
            print("❌ API Error:", response.status_code, response.text)
            return "Sorry, I couldn't get a response from the AI."
    except Exception as e:
        print("❌ Exception:", str(e))
        return "There was a problem connecting to the AI."

# ================== CONTROL FUNCTIONS ==================
def shutdown():
    speak("Shutting down the system.")
    os.system("shutdown /s /t 1")

def open_chrome():
    speak("Opening Chrome.")
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    if os.path.exists(path):
        subprocess.Popen([path])
    else:
        speak("Chrome not found on this system.")

def search_google(query):
    speak(f"Searching Google for {query}")
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def open_folder(folder_name):
    user_folder = os.path.expanduser("~")
    folder_path = os.path.join(user_folder, folder_name)
    speak(f"Opening folder {folder_name}")
    if os.path.exists(folder_path):
        try:
            os.startfile(folder_path)  # Windows
        except AttributeError:
            subprocess.Popen(["xdg-open", folder_path])  # Linux
    else:
        speak("Sorry, I can't find that folder.")

# ================== MAIN LOOP ==================
if __name__ == "__main__":
    speak("Hello, I am Jarvis. Say 'Jarvis' to activate me.")

    while True:
        print("🕒 Waiting for wake word 'Jarvis'...")
        wake_input = listen()

        if wake_input and "jarvis" in wake_input.lower():
            speak("Yes? What would you like me to do?")
            command = listen()

            if command:
                command_lower = command.lower()

                if any(word in command_lower for word in ["exit", "quit", "stop", "bye"]):
                    speak("Goodbye! Have a great day.")
                    break

                elif "shutdown" in command_lower:
                    shutdown()
                    break

                elif "open chrome" in command_lower:
                    open_chrome()

                elif "search for" in command_lower or "google" in command_lower:
                    search_query = command_lower.replace("search for", "").replace("google", "").strip()
                    if search_query:
                        search_google(search_query)
                    else:
                        speak("What should I search for?")

                elif "open folder" in command_lower:
                    folder = command_lower.replace("open folder", "").strip()
                    open_folder(folder)

                else:
                    response = chat_with_deepseek(command)
                    if response:
                        speak(response)
                    else:
                        speak("I couldn't understand the response.")
            else:
                speak("Sorry, I didn't catch that.")
