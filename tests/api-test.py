import requests

API_KEY = "----"

headers = {
    "x-apisports-key": API_KEY
}

# Mexico = 16

url = (
    "https://v3.football.api-sports.io/fixtures"
    "?team=16&season=2025"
)

response = requests.get(
    url,
    headers=headers
)

data = response.json()

# SHOW FIRST 5 MATCHES

for match in data["response"][:5]:

    print(
        match["teams"]["home"]["name"],
        "-",
        match["teams"]["away"]["name"]
    )
