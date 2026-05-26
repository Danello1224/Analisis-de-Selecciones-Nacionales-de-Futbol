# Importamos las herramientas del sistema de AWS y Python
# Import AWS system and Python system tools
import sys

# Importamos el "motor" y el contexto de Spark para poder procesar Big Data en paralelo
# Import the Spark engine and context to process Big Data in parallel
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# Importamos las funciones específicas de Spark para manipular, limpiar y transformar columnas
# Import specific Spark functions to manipulate, clean, and transform columns
from pyspark.sql.functions import col, to_timestamp, year, trim, upper

# Inicializamos el entorno de ejecución de Spark en los servidores de AWS Glue
# Initialize the Spark execution environment on AWS Glue servers
sc = SparkContext()
spark = SparkSession(sc)

# Creamos la lista de todas las selecciones rivales cuyos archivos CSV vamos a procesar
# Create the list of all rival national teams whose CSV files we will process
teams = ["bosnia", "canada", "chequia", "coreasur", "croatia", "england", "germany", "mexico", "norway", "qatar", "sudafrica", "sweden", "switzerland"]

# Definimos el nombre exacto de nuestro bucket de S3 del Equipo 6 donde están guardadas las capas
# Define the exact name of our Team 6 S3 bucket where the layers are stored
bucket = "unam-2026-ingenieriadedatos-equipo6-759626152179-us-east-1-an"

# Iniciamos un ciclo para ir limpiando los datos de cada país, uno por uno
# Start a loop to clean the data for each country, one by one
for team in teams:
    # Imprimimos en la consola de AWS Glue qué país está procesando el script en este momento
    # Print in the AWS Glue console which country the script is currently processing
    print(f"Procesando {team}...")
    
    # Leemos el archivo de texto plano (CSV) de la capa cruda (1bronce) en S3
    # Read the flat text file (CSV) from the raw layer (1bronce) in S3
    df = spark.read \
        .option("header", True) \          # Le indicamos a Spark que la primera fila tiene los nombres de las columnas / Tell Spark the first row contains column names
        .option("encoding", "UTF-8") \     # ¡Punto clave! Forzamos la lectura en UTF-8 para no romper acentos / Key point! Force UTF-8 reading to prevent broken accents
        .csv(f"s3://{bucket}/1bronce/{team}/historico_{team}.csv") # Ruta de origen en S3 / Source path in S3

    # PROCESO DE LIMPIEZA Y TIPADO DE DATOS
    # DATA CLEANING AND TYPING PROCESS
    df_clean = (
        df
        .dropna(how="all") # Borramos filas que estén completamente vacías / Drop rows that are completely empty
        .dropna(subset=["fecha","local","visitante","goles_local","goles_visitante"]) # Borramos filas si les falta algún dato clave / Drop rows if they miss key data
        .withColumn("local", trim(col("local")))       # Quitamos espacios en blanco basura al inicio o final del equipo local / Remove white spaces from local team name
        .withColumn("visitante", trim(col("visitante"))) # Quitamos espacios en blanco basura al inicio o final del equipo visitante / Remove white spaces from away team name
        .withColumn("torneo", trim(col("torneo")))       # Quitamos espacios en blanco basura en el nombre de la competencia / Remove white spaces from tournament name
        .withColumn("local", upper(col("local")))       # Convertimos el nombre del equipo local a MAYÚSCULAS para estandarizar / Convert local team name to UPPERCASE for standardization
        .withColumn("visitante", upper(col("visitante"))) # Convertimos el nombre del equipo visitante a MAYÚSCULAS para estandarizar / Convert away team name to UPPERCASE for standardization
        .withColumn("fecha", to_timestamp(col("fecha")))  # Convertimos el texto de la fecha a un tipo Fecha real (Timestamp) / Convert date text to a real Timestamp type
        .withColumn("goles_local", col("goles_local").cast("int"))       # Convertimos los goles del local de texto a Número Entero (int) / Cast local goals from text to Integer (int)
        .withColumn("goles_visitante", col("goles_visitante").cast("int")) # Convertimos los goles del visitante de texto a Número Entero (int) / Cast away goals from text to Integer (int)
    )

    # APLICACIÓN DE REGLAS DE CALIDAD DE DATOS
    # DATA QUALITY RULES APPLICATION
    df_clean = (
        df_clean
        .filter(col("fecha").isNotNull()) # Filtramos y eliminamos partidos que se hayan quedado sin fecha válida / Filter and remove matches without a valid date
        .filter(col("goles_local") >= 0)  # Regla de calidad: Los goles del local no pueden ser negativos / Quality rule: Local goals cannot be negative
        .filter(col("goles_visitante") >= 0) # Regla de calidad: Los goles del visitante no pueden ser negativos / Quality rule: Away goals cannot be negative
        .filter(col("goles_local") <= 20)  # Regla de calidad: Filtramos anomalías (máximo 20 goles por partido para el local) / Quality rule: Filter anomalies (max 20 goals for local)
        .filter(col("goles_visitante") <= 20) # Regla de calidad: Filtramos anomalías (máximo 20 goles por partido para el visitante) / Quality rule: Filter anomalies (max 20 goals for away)
        .filter(col("local") != col("visitante")) # Validación lógica: Una selección no puede jugar contra sí misma / Logical validation: A team cannot play against itself
        .dropDuplicates(["fecha", "local", "visitante"]) # Eliminamos partidos repetidos (duplicados de la API) / Drop duplicate matches from the API
    )

    # Creamos una columna nueva llamada "year" extrayendo únicamente el año de la fecha del partido
    # Create a new column called "year" extracting only the year from the match date
    df_clean = df_clean.withColumn("year", year(col("fecha")))

    # Imprimimos aviso en los logs indicando que comenzará la escritura optimizada
    # Print a notice in the logs indicating that optimized writing will begin
    print(f"Escribiendo datos particionados de {team} en formato Parquet...")
    
    # GUARDADO OPTIMIZADO EN FORMATO PARQUET
    # OPTIMIZED STORAGE IN PARQUET FORMAT
    df_clean.write \
        .mode("overwrite") \       # Si los datos ya existían en la carpeta, los sobrescribimos para no duplicar en S3 / Overwrite if data already exists in S3 to avoid duplicates
        .partitionBy("year") \     # ¡Mágico! Le ordenamos a Spark que divida físicamente los archivos en carpetas por Año / Magic! Instruct Spark to physically split files into folders by Year
        .parquet(f"s3://{bucket}/2silver/{team}/") # Destino final en formato columnar Parquet dentro de la Capa Silver / Final destination in Parquet format inside Silver layer

    # Imprimimos en los logs que el país actual terminó exitosamente todo su pipeline
    # Print in the logs that the current country successfully finished its pipeline
    print(f" {team} completo")

# Mensaje final para indicar que todo el catálogo de países fue transformado y purificado con éxito
# Final message to indicate that the entire country catalog was successfully transformed and purified
print(" TODO LISTO")
