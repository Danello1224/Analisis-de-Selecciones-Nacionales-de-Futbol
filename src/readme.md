# Source Code
This directory contains the production-ready source code of the data engineering platform, segmented by operational components.

### Contents

* `ec2/`: Python-based extraction scripts executed on Amazon EC2 instances. These scripts connect to API-Football, retrieve historical international match data for multiple national teams, and generate structured CSV datasets used as the Bronze layer input.

* `glue/`: Distributed PySpark ETL scripts (`silver1.py`) for data cleaning, UTF-8 text normalization, null-value filtering, duplicate removal, and native year partitioning into the Silver layer.

* `athena/`: SQL analytical queries executed in Amazon Athena for calculating football performance metrics such as wins, draws, losses, win percentage, goals scored, goals conceded, and per-match averages for every analyzed national team.
