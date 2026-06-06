import urllib3
import requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_coordinates(city: str) -> tuple[float, float] | None:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    resp = requests.get(url, params=params, timeout=10, verify=False)
    resp.raise_for_status()
    data = resp.json()
    if "results" not in data or not data["results"]:
        return None
    result = data["results"][0]
    return result["latitude"], result["longitude"]


def get_weather(lat: float, lon: float) -> dict:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code", "wind_speed_10m"],
        "timezone": "auto",
    }
    resp = requests.get(url, params=params, timeout=10, verify=False)
    resp.raise_for_status()
    return resp.json()


weather_codes = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle",
    53: "Moderate drizzle", 55: "Dense drizzle", 56: "Light freezing drizzle",
    57: "Dense freezing drizzle", 61: "Slight rain", 63: "Moderate rain",
    65: "Heavy rain", 66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snowfall", 73: "Moderate snowfall", 75: "Heavy snowfall",
    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
    82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail",
}


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python main.py <city>")
        return

    city = " ".join(sys.argv[1:])

    try:
        coords = get_coordinates(city)
        if coords is None:
            print(f"City '{city}' not found.")
            return

        lat, lon = coords
        weather = get_weather(lat, lon)
        current = weather.get("current", {})

        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        wcode = current.get("weather_code")
        wind = current.get("wind_speed_10m")

        condition = weather_codes.get(wcode, f"Unknown ({wcode})")

        print(f"Weather in {city} ({lat:.2f}, {lon:.2f}):")
        print(f"  Condition:     {condition}")
        print(f"  Temperature:   {temp}°C")
        print(f"  Humidity:      {humidity}%")
        print(f"  Wind speed:    {wind} km/h")

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")


if __name__ == "__main__":
    main()
