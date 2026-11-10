import requests

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

params = {
    "latitude": 16.432,  # Example latitude (Bangkok)
    "longitude": 102.836,  # Example longitude (Bangkok)
    "hourly": "pm2_5,pm10",
    "start_date": "2025-01-01",
    "end_date": "2025-01-03",
    "timezone": "Asia/Bangkok"
}

response = requests.get(URL, params=params, timeout=60)
print(response.url)
print("status:", response.status_code)

data = response.json()
print(data.keys())
print(data["hourly"]["time"][:5])
print(data["hourly"]["pm2_5"][:5])
