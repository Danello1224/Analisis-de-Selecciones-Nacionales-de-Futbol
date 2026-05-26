import sys
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, year, trim, upper

sc = SparkContext()
spark = SparkSession(sc)

#teams = ["mexico", "coreasur", "sudafrica", "chequia"]
teams = ["bosnia", "canada", "chequia", "coreasur", "croatia", "england", "germany", "mexico", "norway", "qatar", "sudafrica", "sweden", "switzerland"]
bucket = "unam-2026-ingenieriadedatos-equipo6-759626152179-us-east-1-an"

for team in teams:
    print(f"Procesando {team}...")
    df = spark.read \
        .option("header", True) \
        .option("encoding", "UTF-8") \
        .csv(f"s3://{bucket}/1bronce/{team}/historico_{team}.csv")

    df_clean = (
        df
        .dropna(how="all")
        .dropna(subset=["fecha","local","visitante","goles_local","goles_visitante"])
        .withColumn("local", trim(col("local")))
        .withColumn("visitante", trim(col("visitante")))
        .withColumn("torneo", trim(col("torneo")))
        .withColumn("local", upper(col("local")))
        .withColumn("visitante", upper(col("visitante")))
        .withColumn("fecha", to_timestamp(col("fecha")))
        .withColumn("goles_local", col("goles_local").cast("int"))
        .withColumn("goles_visitante", col("goles_visitante").cast("int"))
    )

    df_clean = (
        df_clean
        .filter(col("fecha").isNotNull())
        .filter(col("goles_local") >= 0)
        .filter(col("goles_visitante") >= 0)
        .filter(col("goles_local") <= 20)
        .filter(col("goles_visitante") <= 20)
        .filter(col("local") != col("visitante"))
        .dropDuplicates(["fecha", "local", "visitante"])
    )

    df_clean = df_clean.withColumn("year", year(col("fecha")))

    print(f"Escribiendo datos particionados de {team} en formato Parquet...")
    
    df_clean.write \
        .mode("overwrite") \
        .partitionBy("year") \
        .parquet(f"s3://{bucket}/2silver/{team}/")

    print(f" {team} completo")

print(" TODO LISTO")