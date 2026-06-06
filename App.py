from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "74b4f002c640470642bf377e975d3ec5"

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form["city"]

        if city.strip() == "":
            error = "Please enter a city name."
        else:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            try:
                response = requests.get(url)
                data = response.json()

                if data.get("cod") == 200:
                    weather_data = { "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "weather": data["weather"][0]["description"].title(),
                        "wind_speed": data["wind"]["speed"],
                        "icon": data["weather"][0]["icon"],
                        "main_weather": data["weather"][0]["main"]
}
                    icon = weather_data["icon"]
                    emoji_map  = {
    "01d": "☀",   # clear day
    "01n": "🌙",   # clear night
    "02d": "⛅",
    "02n": "☁🌙",
    "03d": "☁",
    "03n": "☁",
    "04d": "☁",
    "04n": "☁",
    "09d": "🌧",
    "09n": "🌧",
    "10d": "🌦",
    "10n": "🌧🌙",
    "11d": "⛈",
    "11n": "⛈",
    "13d": "❄",
    "13n": "❄",
    "50d": "🌫",
    "50n": "🌫"
}

                    weather_data["emoji"] = emoji_map.get(icon, "🌍")
                else:
                    error = "City not found."

            except:
                error = "Something went wrong."

    return render_template(
        "index.html",
        weather_data=weather_data,
        error=error
    )

if __name__ == "__main__":
    app.run(debug=True)