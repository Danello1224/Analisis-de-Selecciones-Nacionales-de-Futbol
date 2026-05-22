import requests
import polars as pl

API_KEY = "ad2e7d01a2094b306ece76e60b7e44cb"
headers = {
    "x-apisports-key": API_KEY
}

url = "https://v3.football.api-sports.io/fixtures?team=16&season=2023"

response = requests.get(url, headers=headers)
data = response.json()

rows = []

for match in data["response"]:
    rows.append({
        "fecha": match["fixture"]["date"],
        "local": match["teams"]["home"]["name"],
        "visitante": match["teams"]["away"]["name"],
        "goles_local": match["goals"]["home"],
        "goles_visitante": match["goals"]["away"],
        "torneo": match["league"]["name"]
    })

df = pl.DataFrame(rows)

df.write_csv("partidos_mexico.csv")

print(df.head())
