import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000/countries"

def export_countries():
    response = requests.get(API_URL, timeout = 20)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data)

    

    columns = ["country_name", "capital", "population", "area"]
    df = df.reindex(columns=columns)

    print(df.to_string(index=False))
    df.to_csv("exported_countries.csv", index=False)

    print(f"\nExported {len(df)} countries to CSV.")

if __name__ == "__main__":
    export_countries()