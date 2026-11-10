#fetch api for 77 province in Thailand about pm2.5 hourly data and save to parquet file

import os, time
import requests
import pandas as pd

START = "2023-01-01"
END = "2025-12-31"
URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

PROVINCES = [
    ("Bangkok","Central",13.756,100.502), ("Ang Thong","Central",14.589,100.455),
    ("Chai Nat","Central",15.186,100.125), ("Kamphaeng Phet","Central",16.483,99.522),
    ("Lop Buri","Central",14.799,100.654), ("Nakhon Nayok","Central",14.204,101.213),
    ("Nakhon Pathom","Central",13.820,100.062), ("Nakhon Sawan","Central",15.704,100.137),
    ("Nonthaburi","Central",13.862,100.514), ("Pathum Thani","Central",14.021,100.525),
    ("Phetchabun","Central",16.419,101.160), ("Phichit","Central",16.443,100.349),
    ("Phitsanulok","Central",16.821,100.265), ("Phra Nakhon Si Ayutthaya","Central",14.353,100.569),
    ("Samut Prakan","Central",13.599,100.597), ("Samut Sakhon","Central",13.548,100.274),
    ("Samut Songkhram","Central",13.409,100.002), ("Saraburi","Central",14.528,100.910),
    ("Sing Buri","Central",14.888,100.398), ("Sukhothai","Central",17.007,99.823),
    ("Suphan Buri","Central",14.474,100.117), ("Uthai Thani","Central",15.380,100.025),
    ("Chiang Mai","North",18.788,98.985), ("Chiang Rai","North",19.910,99.840),
    ("Lampang","North",18.289,99.491), ("Lamphun","North",18.574,99.009),
    ("Mae Hong Son","North",19.302,97.965), ("Nan","North",18.783,100.778),
    ("Phayao","North",19.166,99.902), ("Phrae","North",18.145,100.141),
    ("Uttaradit","North",17.620,100.099),
    ("Amnat Charoen","Northeast",15.858,104.628), ("Bueng Kan","Northeast",18.360,103.647),
    ("Buri Ram","Northeast",14.993,103.103), ("Chaiyaphum","Northeast",15.806,102.031),
    ("Kalasin","Northeast",16.432,103.506), ("Khon Kaen","Northeast",16.432,102.836),
    ("Loei","Northeast",17.486,101.722), ("Maha Sarakham","Northeast",16.184,103.301),
    ("Mukdahan","Northeast",16.545,104.723), ("Nakhon Phanom","Northeast",17.407,104.781),
    ("Nakhon Ratchasima","Northeast",14.971,102.102), ("Nong Bua Lam Phu","Northeast",17.204,102.441),
    ("Nong Khai","Northeast",17.879,102.742), ("Roi Et","Northeast",16.054,103.653),
    ("Sakon Nakhon","Northeast",17.155,104.148), ("Si Sa Ket","Northeast",15.118,104.322),
    ("Surin","Northeast",14.882,103.494), ("Ubon Ratchathani","Northeast",15.244,104.848),
    ("Udon Thani","Northeast",17.415,102.786), ("Yasothon","Northeast",15.792,104.145),
    ("Chachoengsao","East",13.690,101.072), ("Chanthaburi","East",12.611,102.104),
    ("Chon Buri","East",13.361,100.985), ("Prachin Buri","East",14.050,101.372),
    ("Rayong","East",12.681,101.282), ("Sa Kaeo","East",13.814,102.072),
    ("Trat","East",12.243,102.515),
    ("Kanchanaburi","West",14.023,99.533), ("Phetchaburi","West",13.112,99.940),
    ("Prachuap Khiri Khan","West",11.812,99.797), ("Ratchaburi","West",13.537,99.817),
    ("Tak","West",16.884,99.126),
    ("Chumphon","South",10.493,99.180), ("Krabi","South",8.086,98.906),
    ("Nakhon Si Thammarat","South",8.432,99.963), ("Narathiwat","South",6.426,101.823),
    ("Pattani","South",6.869,101.250), ("Phang Nga","South",8.451,98.525),
    ("Phatthalung","South",7.617,100.078), ("Phuket","South",7.880,98.392),
    ("Ranong","South",9.966,98.635), ("Satun","South",6.624,100.067),
    ("Songkhla","South",7.199,100.595), ("Surat Thani","South",9.139,99.333),
    ("Trang","South",7.556,99.611), ("Yala","South",6.541,101.281),
]

print("Total provinces:", len(PROVINCES))

os.makedirs("air", exist_ok=True)
os.makedirs("province", exist_ok=True)

dim = pd.DataFrame(PROVINCES, columns=["province", "region", "latitude", "longitude"])
dim.to_parquet("province/province.parquet", index=False)    

failed = []
for name, region, latitude, longitude in PROVINCES:
    params = {
        "latitude" : latitude,
        "longitude" : longitude,
        "hourly" : "pm2_5,pm10",
        "start_date" : START,
        "end_date" : END,
        "timezone" : "Asia/Bangkok"     
    }

    try:
        r = requests.get(URL, params=params, timeout=120)
        r.raise_for_status()  # Raise an error for bad responses
        hourly = r.json()["hourly"]
        df = pd.DataFrame(hourly)
        df["province"] = name
        file_name = name.lower().replace(" ", "_") + ".parquet"
        df.to_parquet("air/" + file_name, index=False)
        print(f"Saved {file_name} with {len(df)} rows")
    except Exception as e:
        print(f"Failed to fetch data for {name}: {e}")
        failed.append(name)
    time.sleep(1)  # Sleep for 1 second to avoid hitting the API too quickly

print("Failed provinces:", failed)