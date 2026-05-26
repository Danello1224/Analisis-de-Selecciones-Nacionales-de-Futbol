import requests
import csv
from datetime import datetime, timezone

# API CONFIGURATION
# Configuración de la API

API_KEY = "ad2e7d01a2094b306ece76e60b7e44cb"

headers = {
    "x-apisports-key": API_KEY
}

# GROUP STAGE RIVALS CONFIGURATION
# Configuración de rivales de fase de grupos

teams = {
    "mexico": 16,
    "corea": 17,
    "sudafrica": 1531,
    "chequia": 770
}

# SEASONS TO QUERY
# Temporadas a consultar

seasons = [2022, 2023, 2024, 2025, 2026]

# START DATE FILTER
# Filtro de fecha inicial

fecha_inicio = datetime(
    2022,
    8,
    1,
    tzinfo=timezone.utc
)

# MAIN TEAM LOOP
# Bucle principal de equipos

for team_name, team_id in teams.items():

    print(f"\nDescargando partidos de {team_name.upper()}...")

    partidos = []

    # SEASON LOOP
    # Bucle de temporadas

    for season in seasons:

        print(f"Consultando temporada {season}...")

        # API REQUEST URL
        # URL de consulta API

        url = (
            f"https://v3.football.api-sports.io/fixtures"
            f"?team={team_id}&season={season}"
        )

        # HTTP REQUEST
        # Solicitud HTTP

        response = requests.get(
            url,
            headers=headers
        )

        # JSON RESPONSE
        # Respuesta JSON

        data = response.json()

        # MATCH EXTRACTION
        # Extracción de partidos

        for match in data["response"]:

            fecha_str = match["fixture"]["date"]

            fecha = datetime.fromisoformat(
                fecha_str.replace("Z", "+00:00")
            )

            # FILTER MATCHES SINCE AUGUST 2022
            # Filtrar partidos desde agosto 2022

            if fecha >= fecha_inicio:

                partidos.append({

                    "fecha": fecha_str,

                    "local":
                    match["teams"]["home"]["name"],

                    "visitante":
                    match["teams"]["away"]["name"],

                    "goles_local":
                    match["goals"]["home"],

                    "goles_visitante":
                    match["goals"]["away"],

                    "torneo":
                    match["league"]["name"]
                })

    # CSV FILE GENERATION
    # Generación del archivo CSV

    nombre_archivo = f"historico_{team_name}.csv"

    with open(
        nombre_archivo,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # CSV HEADERS
        # Encabezados CSV

        writer.writerow([
            "fecha",
            "local",
            "visitante",
            "goles_local",
            "goles_visitante",
            "torneo"
        ])

        # WRITE MATCH DATA
        # Escritura de datos

        for partido in partidos:

            writer.writerow([
                partido["fecha"],
                partido["local"],
                partido["visitante"],
                partido["goles_local"],
                partido["goles_visitante"],
                partido["torneo"]
            ])

    # FINAL TEAM SUMMARY
    # Resumen final por equipo

    print(
        f"CSV generado: {nombre_archivo}"
    )

    print(
        f"Partidos guardados: {len(partidos)}"
    )

# FINAL PROCESS CONFIRMATION
# Confirmación final del proceso

print("\nProceso completado.")
