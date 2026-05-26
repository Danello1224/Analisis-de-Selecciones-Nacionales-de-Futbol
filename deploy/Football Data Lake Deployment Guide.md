# Football Data Lake Project - Deployment and Replication Guide

## Overview

This document describes the complete process required to replicate the Football Data Lake Project environment using AWS cloud services through the AWS Management Console.

The project focuses on the ingestion, transformation, storage, and analytical processing of international football match data to support scouting and statistical analysis of potential opponents for the Mexican National Team ahead of the FIFA World Cup 2026.

The architecture integrates Amazon S3, AWS Glue, Amazon Athena, and Amazon EC2 to support scalable football data engineering workflows and analytical metric generation.

The deployment process documented here follows the same implementation workflow used during the original project development.

---

# Project Objective

The main objective of the project is to centralize and process historical football match datasets to generate analytical metrics related to national team performance and potential World Cup rivals.

The solution supports:

- Historical football match analysis
- National team performance monitoring
- Football statistics processing
- Query optimization using partitioned parquet datasets
- Scouting-oriented analytical workflows
- Opponent comparison analysis

---

# Project Architecture

The solution is composed of the following AWS services:

| Service | Purpose |
|---|---|
| Amazon S3 | Centralized storage for raw and processed football datasets |
| AWS Glue | PySpark-based cleaning and transformation of football datasets |
| Amazon Athena | SQL querying service for analytical processing |
| Amazon EC2 | Execution of Python ingestion scripts and dataset upload automation |

---

# Data Architecture

The project follows a layered Data Lake architecture:

```text
Raw Football Data
        ↓
Bronze Layer (Raw CSV Files)
        ↓
Silver Layer (Cleaned Parquet Data)
        ↓
Athena SQL Queries
        ↓
Gold Metrics Layer
```

---

# Repository Structure

```text
project-root/
├── dashboard/
├── docs/
├── deploy/
├── tests/
├── img/
├── ppt/
├── src/
└── README.md
```

---

# Football Data Source

The project uses API-Football as the primary external data source for retrieving historical international football matches and national team statistics.

The analyzed national teams include:

- Mexico
- South Africa
- South Korea
- Czech Republic
- Canada
- Qatar
- Switzerland
- Bosnia & Herzegovina
- England
- Croatia
- Sweden
- Norway
- Germany

---

# Football Data Processing Workflow

The project processes historical football datasets containing information such as:

- Match fixtures
- National teams
- Goals scored
- Goals conceded
- Match outcomes
- Draw statistics
- Team performance indicators
- Tournament participation records

The processing pipeline transforms raw football data into optimized analytical datasets used for scouting analysis and statistical querying.

---

# Prerequisites

Before starting the replication process, ensure the following requirements are available.

## AWS Requirements

- AWS account
- Access to AWS Management Console
- IAM permissions for:
  - Amazon S3
  - AWS Glue
  - Amazon Athena
  - Amazon EC2

## Recommended Tools

- Web browser
- Visual Studio Code
- Git
- Python 3

---

# Step 1 — Access AWS Management Console

1. Open the AWS Management Console
2. Sign in to the AWS account
3. Select the project region
4. Verify access to:
   - Amazon S3
   - AWS Glue
   - Amazon Athena
   - Amazon EC2

---

# Step 2 — Configure Amazon S3

## Create the Data Lake Bucket

1. Navigate to Amazon S3
2. Select "Create Bucket"
3. Configure:
   - Bucket name
   - Region
   - Security settings
4. Create the bucket

---

## Configure Data Lake Layers

Inside the S3 bucket, create the following structure:

```text
s3://football-data-lake/
├── bronze/
├── silver/
├── gold/
└── athena-results/
```

### Layer Description

| Layer | Purpose |
|---|---|
| Bronze | Raw historical football datasets in CSV format |
| Silver | Cleaned and partitioned parquet datasets |
| Gold | Analytical football metrics generated from Athena queries |

---

# Step 3 — Configure EC2 Instance

## Launch EC2 Instance

1. Navigate to EC2 Dashboard
2. Select "Launch Instance"
3. Configure:
   - Instance name
   - Operating system
   - Instance type
   - Security groups
   - Key pair

---

## Connect to EC2

Access the instance using:

- EC2 Instance Connect
- SSH

---

## Install Required Dependencies

Install the required tools:

- Python
- Requests
- AWS CLI
- Boto3
- Git

---

## Execute Football Ingestion Scripts

The EC2 instance is used to execute Python scripts responsible for:

- Connecting to API-Football
- Retrieving historical football match data
- Generating CSV datasets
- Uploading datasets to Amazon S3 Bronze layer

The ingestion process retrieves matches from August 2022 onward for each analyzed national team.

Example datasets generated:

```text
historico_mexico.csv
historico_south_korea.csv
historico_england.csv
```

---

# Step 4 — Upload Raw Datasets to S3 Bronze Layer

After generating the CSV datasets from EC2:

1. Navigate to Amazon S3
2. Open the Data Lake bucket
3. Upload the generated CSV files into the Bronze layer

Example structure:

```text
bronze/mexico/historico_mexico.csv
bronze/england/historico_england.csv
bronze/croatia/historico_croatia.csv
```

Verify:

- CSV files uploaded successfully
- Folder organization by country
- Correct file naming convention

---

# Step 5 — Configure AWS Glue

## Create Glue Database

1. Open AWS Glue
2. Navigate to "Databases"
3. Create a new database

Example:

```text
football_data_lake_db
```

---

# Step 6 — Configure Glue Crawlers

## Create Crawlers

1. Navigate to "Crawlers"
2. Create a crawler for the Silver layer
3. Configure:
   - S3 parquet source
   - IAM role
   - Database destination

---

## Execute Crawlers

Run crawlers to detect parquet schemas stored in the Silver layer.

The crawlers automatically detect:

- Dataset schemas
- Column structures
- File formats
- Partitions by year

Verify:

- Tables created successfully
- Schemas generated correctly
- Metadata available in Athena

---

# Step 7 — Configure ETL Jobs in AWS Glue

## ETL Workflow Overview

The ETL process transforms raw football datasets into structured analytical datasets.

The scripts are responsible for:

- Data cleaning
- UTF-8 normalization
- Null value handling
- Duplicate removal
- Year partitioning
- Parquet conversion

---

## Silver Layer Structure

The Silver layer stores partitioned parquet datasets organized by year to optimize Athena query performance.

Example:

```text
silver/mexico/2025/
```

---

## Create Glue ETL Jobs

1. Navigate to "ETL Jobs"
2. Create a new Glue Job
3. Configure:
   - IAM role
   - Script location
   - Temporary directory
   - Input and output locations

---

## Execute ETL Jobs

Run the ETL jobs to process the datasets from:

```text
Bronze → Silver
```

Processed parquet datasets should be stored in:

```text
s3://football-data-lake/silver/
```

---

# Step 8 — Configure Amazon Athena

## Configure Query Results

1. Open Amazon Athena
2. Configure the query result location:

```text
s3://football-data-lake/athena-results/
```

---

## Validate Glue Integration

Verify Athena detects:

- Glue databases
- Tables
- Metadata
- Year partitions

---

## Execute Football Analytics Queries

Run analytical SQL queries against the Silver datasets.

The Athena queries generate metrics such as:

- Wins
- Draws
- Losses
- Win percentage
- Goals scored
- Goals conceded
- Goals per match averages

Example:

```sql
SELECT
    COUNT(*) AS matches
FROM "2silver"
WHERE local = 'MEXICO'
   OR visitante = 'MEXICO';
```

---

# Step 9 — Generate Gold Metrics Layer

The Gold layer contains analytical metrics generated from Athena SQL queries.

These datasets are focused on:

- National team performance analysis
- Rival comparison
- Historical football statistics
- Scouting-oriented metrics

The resulting datasets can be exported or reused for additional analysis.

---

# Step 10 — Optional Dashboard Prototype

An optional dashboard prototype was developed for visualization purposes using HTML, CSS, JavaScript, and AI-assisted design tools.

The dashboard was intended as a complementary visualization layer for displaying football statistics and analytical metrics.

---

# Step 11 — Validation and Testing

## Infrastructure Validation

Verify:

- S3 buckets operational
- Glue jobs executed successfully
- Athena queries functional
- EC2 instance accessible

---

## Data Validation

Verify:

- Raw datasets uploaded correctly
- ETL transformations completed successfully
- Silver layer generated properly
- Metrics calculated accurately

---

# Troubleshooting

## Common Issues

### Athena Tables Not Appearing

Solution:

- Re-run Glue Crawlers
- Verify S3 paths
- Validate Glue permissions

---

### ETL Job Failures

Solution:

- Review Glue Job logs
- Validate parquet structure
- Verify IAM permissions

---

### Incorrect Football Metrics

Solution:

- Validate SQL queries
- Review aggregation logic
- Verify dataset normalization

---

### Access Denied Errors

Solution:

- Review IAM policies
- Validate S3 bucket permissions
- Confirm service access configuration

---

# Security Recommendations

The project environment should follow cloud security best practices:

- Restrict IAM permissions using least-privilege principles
- Protect S3 buckets from public access
- Monitor resource access
- Secure EC2 connectivity
- Maintain credential confidentiality

---

# Final Notes

This project demonstrates the implementation of a cloud-based sports analytics pipeline using AWS services for football data engineering and scouting analysis.

The architecture prioritizes simplicity, scalability, low operational cost, and efficient analytical querying for historical football datasets.

