import pyttsx3

# কবিতা
poem = """

"""

# ইঞ্জিন তৈরি
engine = pyttsx3.init()

# Male voice select
voices = engine.getProperty('voices')
for voice in voices:
    if "male" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

# Speech rate & volume (optional tuning)
engine.setProperty('rate', 140)   # Slow, emotional
engine.setProperty('volume', 1.0) # Full volume

# Audio save
engine.save_to_file(poem, 'joyti_miss_male_voice.mp3')
engine.runAndWait()

print("✅ Male voice file saved as 'joyti_miss_male_voice.mp3'")
