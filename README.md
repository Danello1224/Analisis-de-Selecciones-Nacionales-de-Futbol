# Football soccer data engineering project

Football National Teams Data Lake & Analytics Pipeline:

This project is a data engineering solution focused on analyzing national football teams through a modern AWS-based Data Lake architecture.
The project simulates a real-world scenario where the coaching staff of a national team, in this case Mexico, needs to analyze opponents before a World Cup using historical international match data.

---

# Project Objective

Build a scalable data pipeline capable of:

- Collecting historical match data from national teams
- Processing and cleaning raw datasets
- Structuring information into analytical layers
- Generating performance metrics
- Enabling SQL-based analytical queries

---

# Architecture Overview
<img width="1024" height="698" alt="image" src="https://github.com/user-attachments/assets/c2fb8234-2e95-481a-9771-ba5769612c83" />

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
| Parquet | Analytical optimization |

---

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
- Advanced opponent comparison analysis

---


# Professional Purpose

This project aims to apply real-world concepts related to:

- Data Engineering
- Modern Data Lake architectures
- Distributed ETL systems
- Cloud Computing
- Sports analytics

It also simulates workflows commonly used in enterprise-level data projects.
