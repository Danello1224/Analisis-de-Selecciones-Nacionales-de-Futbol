# football-soccer-data-engineering-project

Football National Teams Data Lake & Analytics Pipeline:

This project is a data engineering solution focused on analyzing national football teams through a modern AWS-based Data Lake architecture.
The project simulates a real-world scenario where the coaching staff of a national team (in this case, Mexico) needs to analyze opponents ahead of a World Cup using historical international match data.

---

# Project Objective

Build a scalable data pipeline capable of:

- Collecting historical match data from national teams
- Processing and cleaning raw datasets
- Structuring information into analytical layers
- Generating performance metrics
- Enabling SQL-based analytical queries

---

# Project Context

Modern sports analysis increasingly depends on data-driven decision making.
This project addresses those issues by implementing a scalable cloud-based architecture using AWS services.

---

# Architecture Overview

API-Football
↓
Amazon EC2 (Python Scripts)
↓
Amazon S3 - Bronze Layer
↓
AWS Glue (Spark ETL)
↓
Amazon S3 - Silver Layer
↓
Amazon Athena (SQL Analytics)
↓
Amazon S3 - Gold Layer
↓
Performance Metrics & Analysis

---

# Layered Architecture

## Bronze Layer

Stores raw data obtained directly from the API.

### Characteristics
- CSV format
- Unprocessed/raw data
- Organized by national team
- Historical storage

---

## Silver Layer

Contains processed and cleaned datasets.

Data quality rules and transformations are applied using Spark jobs in AWS Glue.

### Transformations Applied
- Null value removal
- Goal validation
- Name standardization
- Data type conversion
- Duplicate removal
- Year-based partitioning

### Format
- Parquet
- Optimized for analytical workloads

---

## Gold Layer

Analytical layer focused on business and football performance metrics.

Data is queried using SQL through Amazon Athena.

### Metrics Generated
- Win rate
- Average goals scored
- Average goals conceded
- Opponent performance analysis
- Tournament performance analysis
- Yearly trends

---

# Data Source

The project uses:

## API-Football

Sports data provider used to retrieve:

- International matches
- Match results
- National teams
- Competitions
- Match dates
- Historical statistics

---

# Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data ingestion scripts |
| Requests | API consumption |
| CSV | Dataset generation |
| Amazon EC2 | Script execution |
| Amazon S3 | Data Lake storage |
| AWS Glue | ETL processing |
| Apache Spark | Data transformation |
| Amazon Athena | SQL analytics |
| Parquet |

---

# Data Ingestion

Python scripts are responsible for:

1. Connecting to API-Football
2. Retrieving historical match data
3. Transforming JSON into CSV datasets
4. Generating datasets per national team

### Teams currently analyzed
- Mexico
- South Korea
- South Africa
- Czech Republic

---

# Data Quality

During the Bronze → Silver transition, several quality rules are applied:

- Removal of incomplete records
- Goal validation (0–20 range)
- Column consistency validation
- Team name standardization
- Duplicate removal

These rules ensure reliable and analysis-ready datasets.

---

# Analytical Queries

Metrics are generated using SQL queries in Amazon Athena.

# Current Project Status

## Completed
- API-Football integration
- Historical CSV dataset generation
- S3 storage integration
- Bronze/Silver architecture
- Glue + Spark ETL jobs
- SQL analytics with Athena
- Initial metric generation

## In Progress
- Expanding analyzed national teams
- Dataset optimization
- Pipeline automation improvements

## Future Improvements
- Analytical dashboards
- Fully serverless architecture
- Predictive sports models
- Advanced opponent comparison analysis

---

# Academic and Professional Purpose

This project aims to apply real-world concepts related to:

- Data Engineering
- Modern Data Lake architectures
- Distributed ETL systems
- Cloud Computing
- Sports analytics

while simulating workflows commonly used in enterprise-level data projects.
