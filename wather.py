# Modern Weather App with Location Detection
# This code uses Tkinter for UI and requests to fetch weather data from OpenWeatherMap API.

import tkinter as tk
from tkinter import messagebox
import requestsran

# You need to replace this with your own API key from OpenWeatherMap
API_KEY = "https://www.metaweather.com/api/location/{woeid}"


def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data.get("cod") != 200:
            raise ValueError(data.get("message", "Error fetching weather"))
        city_name = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        result = f"📍 {city_name}, {country}\n🌡️ Temperature: {temp}°C\n☁️ Condition: {condition.capitalize()}\n💧 Humidity: {humidity}%\n🌬️ Wind Speed: {wind} m/s"
        weather_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def search():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return
    get_weather(city)

# GUI Setup
root = tk.Tk()
root.title("🌦️ Weather App")
root.geometry("400x400")
root.configure(bg="#2C3E50")

title = tk.Label(root, text="Weather App", font=("Helvetica", 20, "bold"), fg="#F1C40F", bg="#2C3E50")
title.pack(pady=20)

city_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
city_entry.pack(pady=10)

search_btn = tk.Button(root, text="Get Weather", font=("Helvetica", 12), command=search,
                       bg="#F1C40F", fg="#2C3E50", padx=10, pady=5)
search_btn.pack(pady=10)

weather_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#2C3E50", fg="white", justify="left")
weather_label.pack(pady=20)

note = tk.Label(root, text="Enter your city name (e.g., Dhaka)", font=("Helvetica", 10), bg="#2C3E50", fg="#BDC3C7")
note.pack()

root.mainloop()
