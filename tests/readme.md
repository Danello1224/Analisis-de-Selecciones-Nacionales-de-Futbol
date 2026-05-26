# Testing & Quality Assurance

This directory contains lightweight validation and testing scripts used to verify the correct behavior of the football data pipeline during development and deployment.

### Contents

* **API Extraction Tests**: Simple Python scripts used to validate API-Football connectivity, response structure, and historical match retrieval for selected national teams.

* **S3 Upload Tests**: Validation scripts used to confirm successful uploads of generated CSV datasets into the Amazon S3 Bronze layer.

* **Athena Query Tests**: Initial SQL queries used to verify table availability, schema detection, and successful analytical querying over the Silver datasets.
