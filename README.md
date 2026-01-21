# dockerized-etl-data-pipeline
End-to-end ETL data engineering pipeline using Python, Airflow, dbt, PostgreSQL, Superset, and Docker for containerized, reproducible analytics workflows.

## Introduction
This repository contains a fully containerized ETL pipeline built with Docker.
Data is extracted using Python, orchestrated with Airflow, transformed with dbt inside PostgreSQL, and visualized using Superset.

## Architecture
![Project Architecture](ETL.png)

## Technology Used
1. Programming Language - Python
2. Query Language - SQL
3. Database - PostgreSQL
4. Orchestration - Apache Airflow
5. Transformation - dbt
6. Visualization/BI - Apache Superset
7. Containerization & Environment Management - Docker & Docker Compose

## Dataset Used
This project uses publicly available earthquake data from the U.S. Geological Survey (USGS) Earthquake API. The API provides near real-time and historical information about global seismic activity.
The API exposes earthquake event data in GeoJSON format and includes records for earthquakes detected worldwide, updated continuously by USGS monitoring systems.

### More Info About Dataset
* Original Data Source - https://earthquake.usgs.gov/fdsnws/event/1/#callback

## Premissions and Setup
If postgres or docker premissions are denied, type:
**chmod +x postgres/*.sh docker/*.sh**

Setup Instructions:
1. Clone the repo.

2. Run cp .env_example .env (or copy/rename manually).

3. Configure Docker Init Environment: cp docker/.env_example docker/.env

4. Configure .env files

5. Start Docker

5. Run docker-compose up.
