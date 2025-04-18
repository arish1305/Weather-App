import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io

API_KEY = "65ed462dcee8c254ed1ca20995469d8b"  # Replace with your actual API key

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description'].title()
            temperature = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            pressure = data['main']['pressure']

            icon_code = data['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            icon_data = requests.get(icon_url).content
            icon_image = Image.open(io.BytesIO(icon_data))
            icon_photo = ImageTk.PhotoImage(icon_image)
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo

            result = (
                f"🌆 City: {city.title()}\n"
                f"🌤 Condition: {weather}\n"
                f"🌡 Temperature: {temperature}°C\n"
                f"😌 Feels like: {feels_like}°C\n"
                f"💧 Humidity: {humidity}%\n"
                f"💨 Wind Speed: {wind_speed} m/s\n"
                f"🔵 Pressure: {pressure} hPa"
            )
            result_label.config(text=result, foreground="#1f4f66")
        else:
            messagebox.showerror("City Not Found", "Invalid city name. Try again!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Network Error", f"Failed to connect.\n\n{str(e)}")
        print("Status code:", response.status_code)
        print("Response:", response.text)

# GUI setup
app = tk.Tk()
app.title("🌦 Beautiful Weather App")
app.geometry("460x540")
app.resizable(False, False)
app.configure(bg="#d0e7f9")  # Soft blue background

# Fonts & Style
style = ttk.Style()
style.configure("TLabel", font=("Segoe UI", 12), background="#d0e7f9")
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TEntry", font=("Segoe UI", 11))

# Title banner
title_label = tk.Label(app, text="🌦 Weather Forecast", font=("Segoe UI", 18, "bold"), bg="#d0e7f9", fg="#154360")
title_label.pack(pady=15)

# Input
ttk.Label(app, text="Enter City Name:").pack(pady=8)
city_entry = ttk.Entry(app, width=30)
city_entry.pack(pady=5)

ttk.Button(app, text="Get Weather", command=get_weather).pack(pady=12)

# Icon display
icon_label = ttk.Label(app)
icon_label.pack()

# Output result
result_label = tk.Label(app, text="", font=("Segoe UI", 11), bg="#d0e7f9", fg="#1f4f66", justify="left", anchor="center")
result_label.pack(pady=10)

# Footer
tk.Label(app, text="✨ Powered by OpenWeatherMap", font=("Segoe UI", 9), bg="#d0e7f9", fg="#555").pack(pady=15)

app.mainloop()
