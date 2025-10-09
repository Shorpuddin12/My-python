# Let's start with the Emotion Based Music Player project.
# This script uses DeepFace to detect emotion from webcam and plays music accordingly.
# GUI is created using Tkinter.

import cv2
from deepface import DeepFace
import os
import random
import threading
import tkinter as tk
from tkinter import messagebox
import pygame

# Dictionary mapping emotions to folders containing music
EMOTION_MUSIC_DIR = {
    "happy": "music/happy",
    "sad": "music/sad",
    "angry": "music/angry",
    "surprise": "music/surprise",
    "neutral": "music/neutral"
}

# Initialize Pygame Mixer
pygame.mixer.init()

# Function to play random song from emotion folder
def play_music_for_emotion(emotion):
    folder = EMOTION_MUSIC_DIR.get(emotion)
    if not folder or not os.path.exists(folder):
        messagebox.showerror("Error", f"No music found for emotion: {emotion}")
        return
    songs = [f for f in os.listdir(folder) if f.endswith(".mp3")]
    if not songs:
        messagebox.showerror("Error", f"No .mp3 files in folder: {folder}")
        return
    song = random.choice(songs)
    song_path = os.path.join(folder, song)
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

# Function to detect emotion from webcam
def detect_emotion():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        messagebox.showerror("Error", "Failed to access webcam.")
        return
    try:
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        print(f"Detected emotion: {emotion}")
        play_music_for_emotion(emotion)
        messagebox.showinfo("Emotion Detected", f"Detected emotion: {emotion.capitalize()}")
    except Exception as e:
        messagebox.showerror("Error", str(e))
    finally:
        cap.release()
        cv2.destroyAllWindows()

# GUI Setup
def start_detection():
    threading.Thread(target=detect_emotion).start()

window = tk.Tk()
window.title("🎧 Emotion Based Music Player")
window.geometry("400x300")
window.configure(bg="#222831")

title = tk.Label(window, text="Emotion Based Music Player", font=("Helvetica", 16, "bold"), bg="#222831", fg="#FFD369")
title.pack(pady=30)

start_btn = tk.Button(window, text="Start Emotion Detection", command=start_detection,
                      font=("Helvetica", 12), bg="#FFD369", fg="#222831", padx=20, pady=10)
start_btn.pack(pady=20)

note = tk.Label(window, text="Make sure your webcam is on\nAnd music folders exist", bg="#222831", fg="white")
note.pack(pady=10)

window.mainloop()
