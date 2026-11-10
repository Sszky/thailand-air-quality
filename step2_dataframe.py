import requests
import pandas as pd

URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
province = {
    ("Bangkok", 16.432, 102.836),
    ("Chiang Mai", 18.7883, 98.9853),
    ("Khon Kaen", 16.4419, 102.835)
}

for name, latitude, longitude in province:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "pm2_5,pm10",
        "start_date": "2025-01-01",
        "end_date": "2025-01-03",
        "timezone": "Asia/Bangkok"
    }

    data = requests.get(URL, params=params, timeout=60).json()

    df = pd.DataFrame(data["hourly"])
    df["province"] = name

    print(df.head())
    print(len(df), "rows")
    print(df.dtypes)

    df.to_parquet(f"{name}_test.parquet", index=False)
    print(f"Saved to {name}_test.parquet")