import boto3 
from botocore.exceptions import NoCredentialsError
import os

# S3 bucket name used to store project datasets
# Nombre del bucket S3 utilizado para almacenar datasets
BUCKET_NAME = "unam-2026-ingenieriadedatos-equipo6-759626152179-us-east-1-an"

# Dictionary containing local CSV files
# and their corresponding team folders
# Diccionario con archivos CSV locales
# y sus carpetas correspondientes
archivos = {
    "mexico": "historico_mexico.csv",
    "south_korea": "historico_corea.csv",
    "south_africa": "historico_sudafrica.csv",
    "czech_republic": "historico_chequia.csv",

    "canada": "historico_canada.csv",
    "bosnia": "historico_bosnia.csv",
    "qatar": "historico_qatar.csv",
    "switzerland": "historico_switzerland.csv",
    "england": "historico_england.csv",
    "croatia": "historico_croatia.csv",
    "sweden": "historico_sweden.csv",
    "norway": "historico_norway.csv"
}

# Create S3 client using boto3
# Crea el cliente S3 utilizando boto3
s3 = boto3.client("s3")

try:

    # Iterate through every local CSV file
    # Itera sobre cada archivo CSV local
    for pais, archivo_local in archivos.items():

        # Verify if the local file exists
        # Verifica si el archivo local existe
        if not os.path.exists(archivo_local):

            print(f"[ERROR] No existe: {archivo_local}")
            continue

        # Destination path inside the S3 bucket
        # Ruta destino dentro del bucket S3
        ruta_s3 = f"1bronce/{pais}/{archivo_local}"

        # Console message before upload
        # Mensaje de consola antes de subir
        print(
            f"Subiendo {archivo_local} "
            f"a s3://{BUCKET_NAME}/{ruta_s3}"
        )

        # Upload file to Amazon S3
        # Sube el archivo hacia Amazon S3
        s3.upload_file(
            archivo_local,
            BUCKET_NAME,
            ruta_s3
        )

        # Successful upload confirmation
        # Confirmación de carga exitosa
        print(f"[OK] {archivo_local} subido correctamente\n")

# Handle missing AWS credentials
# Maneja errores de credenciales AWS
except NoCredentialsError:

    print(
        "Error: No se encontraron credenciales AWS."
    )

# Handle unexpected errors
# Maneja errores inesperados
except Exception as e:

    print(
        f"Ocurrió un error inesperado: {e}"
    )

# Final process confirmation
# Confirmación final del proceso
print("Proceso finalizado.")