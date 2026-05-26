import boto3

# FILE CONFIGURATION

local_file = "historico_mexico.csv"

# S3 CONFIGURATION

bucket_name = "lunam-2026-ingenieriadedatos-equipo6-759626152179-us-east-1"

s3_file = (
    "bronze/mexico/"
    "historico_mexico.csv"
)

# CREATE S3 CLIENT

s3 = boto3.client("s3")

# UPLOAD FILE TO S3

s3.upload_file(
    local_file,
    bucket_name,
    s3_file
)

print("Archivo subido correctamente a S3")
