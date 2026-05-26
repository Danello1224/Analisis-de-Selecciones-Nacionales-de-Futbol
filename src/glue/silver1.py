# Importamos las herramientas del sistema de AWS y Python
import sys

# Importamos el "motor" y el contexto de Spark para poder procesar Big Data en paralelo
from pyspark.context import SparkContext
from pyspark.sql import SparkSession

# Importamos las funciones específicas de Spark para manipular, limpiar y transformar columnas
from pyspark.sql.functions import col, to_timestamp, year, trim, upper

# Inicializamos el entorno de ejecución de Spark en los servidores de AWS Glue
sc = SparkContext()
spark = SparkSession(sc)

# Creamos la lista de todas las selecciones rivales cuyos archivos CSV vamos a procesar
teams = ["bosnia", "canada", "chequia", "coreasur", "croatia", "england", "germany", "mexico", "norway", "qatar", "sudafrica", "sweden", "switzerland"]

# Definimos el nombre exacto de nuestro bucket de S3 del Equipo 6 donde están guardadas las capas
bucket = "unam-2026-ingenieriadedatos-equipo6-759626152179-us-east-1-an"

# Iniciamos un ciclo para ir limpiando los datos de cada país, uno por uno
for team in teams:
    # Imprimimos en la consola de AWS Glue qué país está procesando el script en este momento
    print(f"Procesando {team}...")
    
    # Leemos el archivo de texto plano (CSV) de la capa cruda (1bronce) en S3
    df = spark.read \
        .option("header", True) \          # Le indicamos a Spark que la primera fila tiene los nombres de las columnas
        .option("encoding", "UTF-8") \     # ¡Punto clave! Forzamos la lectura en UTF-8 para no romper acentos (como en México)
        .csv(f"s3://{bucket}/1bronce/{team}/historico_{team}.csv") # Ruta de origen en S3

    # PROCESO DE LIMPIEZA Y TIPADO DE DATOS
    df_clean = (
        df
        .dropna(how="all") # Borramos filas que estén completamente vacías
        .dropna(subset=["fecha","local","visitante","goles_local","goles_visitante"]) # Borramos filas si les falta algún dato clave
        .withColumn("local", trim(col("local")))       # Quitamos espacios en blanco basura al inicio o final del equipo local
        .withColumn("visitante", trim(col("visitante"))) # Quitamos espacios en blanco basura al inicio o final del equipo visitante
        .withColumn("torneo", trim(col("torneo")))       # Quitamos espacios en blanco basura en el nombre de la competencia
        .withColumn("local", upper(col("local")))       # Convertimos el nombre del equipo local a MAYÚSCULAS para estandarizar
        .withColumn("visitante", upper(col("visitante"))) # Convertimos el nombre del equipo visitante a MAYÚSCULAS para estandarizar
        .withColumn("fecha", to_timestamp(col("fecha")))  # Convertimos el texto de la fecha a un tipo Fecha real (Timestamp)
        .withColumn("goles_local", col("goles_local").cast("int"))       # Convertimos los goles del local de texto a Número Entero (int)
        .withColumn("goles_visitante", col("goles_visitante").cast("int")) # Convertimos los goles del visitante de texto a Número Entero (int)
    )

    # APLICACIÓN DE REGLAS DE CALIDAD DE DATOS
    df_clean = (
        df_clean
        .filter(col("fecha").isNotNull()) # Filtramos y eliminamos partidos que se hayan quedado sin fecha válida
        .filter(col("goles_local") >= 0)  # Regla de calidad: Los goles del local no pueden ser negativos
        .filter(col("goles_visitante") >= 0) # Regla de calidad: Los goles del visitante no pueden ser negativos
        .filter(col("goles_local") <= 20)  # Regla de calidad: Filtramos anomalías (máximo 20 goles por partido para el local)
        .filter(col("goles_visitante") <= 20) # Regla de calidad: Filtramos anomalías (máximo 20 goles por partido para el visitante)
        .filter(col("local") != col("visitante")) # Validación lógica: Una selección no puede jugar contra sí misma
        .dropDuplicates(["fecha", "local", "visitante"]) # Eliminamos partidos repetidos (duplicados de la API)
    )

    # Creamos una columna nueva llamada "year" extrayendo únicamente el año de la fecha del partido
    df_clean = df_clean.withColumn("year", year(col("fecha")))

    # Imprimimos aviso en los logs indicando que comenzará la escritura optimizada
    print(f"Escribiendo datos particionados de {team} en formato Parquet...")
    
    # GUARDADO OPTIMIZADO EN FORMATO PARQUET
    df_clean.write \
        .mode("overwrite") \       # Si los datos ya existían en la carpeta, los sobrescribimos para no duplicar en S3
        .partitionBy("year") \     # ¡Mágico! Le ordenamos a Spark que divida físicamente los archivos en carpetas por Año
        .parquet(f"s3://{bucket}/2silver/{team}/") # Destino final en formato columnar Parquet dentro de la Capa Silver

    # Imprimimos en los logs que el país actual terminó exitosamente todo su pipeline
    print(f" {team} completo")

# Mensaje final para indicar que todo el catálogo de países fue transformado y purificado con éxito
print(" TODO LISTO")
