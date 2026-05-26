import requests
import csv
from datetime import datetime, timezone

# API key used for authentication with API-Football
# API key utilizada para autenticación con API-Football
API_KEY = "ad2e7d01a2094b306ece76e60b7e44cb"

# Required headers for every API request
# Headers requeridos para cada petición a la API
headers = {
    "x-apisports-key": API_KEY
}

# Dictionary containing possible knockout stage rivals
# Diccionario con posibles rivales de fase eliminatoria
teams = {
    "canada": 5529,
    "bosnia": 1113,
    "qatar": 1569,
    "switzerland": 15,
    "england": 10,
    "croatia": 3,
    "sweden": 5,
    "norway": 1090
}

# Minimum accepted date for matches
# Fecha mínima aceptada para los partidos
fecha_inicio = datetime(
    2022,
    8,
    1,
    tzinfo=timezone.utc
)

# Iterate through every selected national team
# Itera sobre cada selección nacional
for team_name, team_id in teams.items():

    print(f"\nDescargando partidos de {team_name.upper()}...")

    # Temporary storage for match data
    # Almacenamiento temporal de partidos
    dataset = []

    # Seasons included in the extraction process
    # Temporadas incluidas en el proceso
    seasons = [2022, 2023, 2024, 2025, 2026]

    # Iterate through every season
    # Itera sobre cada temporada
    for season in seasons:

        print(f"  Temporada {season}")

        # API endpoint used to retrieve fixtures
        # Endpoint utilizado para obtener partidos
        url = (
            f"https://v3.football.api-sports.io/fixtures"
            f"?team={team_id}&season={season}"
        )

        # HTTP request to API-Football
        # Petición HTTP hacia API-Football
        response = requests.get(url, headers=headers)

        # Convert response into JSON format
        # Convierte la respuesta a formato JSON
        data = response.json()

        # Validate API response structure
        # Valida la estructura de respuesta
        if "response" not in data:
            print(f"  Error en temporada {season}")
            continue

        # Process every returned match
        # Procesa cada partido obtenido
        for match in data["response"]:

            try:

                # Extract match date
                # Extrae la fecha del partido
                fecha_str = match["fixture"]["date"]

                # Convert date string into datetime object
                # Convierte la fecha a objeto datetime
                fecha = datetime.fromisoformat(
                    fecha_str.replace("Z", "+00:00")
                )

                # Filter matches from August 2022 onward
                # Filtra partidos desde agosto 2022
                if fecha >= fecha_inicio:

                    # Extract relevant match information
                    # Extrae información relevante del partido
                    local = match["teams"]["home"]["name"]
                    visitante = match["teams"]["away"]["name"]

                    goles_local = match["goals"]["home"]
                    goles_visitante = match["goals"]["away"]

                    torneo = match["league"]["name"]

                    # Store match data
                    # Guarda los datos del partido
                    dataset.append([
                        fecha_str,
                        local,
                        visitante,
                        goles_local,
                        goles_visitante,
                        torneo
                    ])

            # Handle unexpected processing errors
            # Maneja errores inesperados
            except Exception as e:
                print("Error procesando partido:", e)

    # Remove duplicated matches
    # Elimina partidos duplicados
    dataset_unico = []

    # Set used to detect duplicates
    # Set utilizado para detectar duplicados
    vistos = set()

    for row in dataset:

        # Unique key using date and teams
        # Clave única usando fecha y equipos
        key = (
            row[0],
            row[1],
            row[2]
        )

        # Store only unique matches
        # Guarda únicamente partidos únicos
        if key not in vistos:

            vistos.add(key)

            dataset_unico.append(row)

    # Dynamic CSV file name generation
    # Generación dinámica del nombre CSV
    nombre_archivo = f"historico_{team_name}.csv"

    # Create CSV file and write processed data
    # Crea el CSV y escribe los datos procesados
    with open(
        nombre_archivo,
        mode="w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        # CSV column headers
        # Encabezados del CSV
        writer.writerow([
            "fecha",
            "local",
            "visitante",
            "goles_local",
            "goles_visitante",
            "torneo"
        ])

        # Write all unique matches into CSV
        # Escribe todos los partidos únicos
        writer.writerows(dataset_unico)

    # Console confirmation messages
    # Mensajes de confirmación
    print(f"CSV generado: {nombre_archivo}")
    print(f"Partidos guardados: {len(dataset_unico)}")

# Final process confirmation
# Confirmación final del proceso
print("\nProceso completado.")