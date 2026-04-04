# Cloud Sales Warehouse Platform

Production-style cloud data platform integrating batch and streaming pipelines into Amazon S3 and Redshift Serverless, orchestrated with Airflow and transformed using dbt for analytics and API serving.

## Architecture Overview

Batch + Streaming → S3 (Raw) → dbt (Transform) → Redshift → FastAPI / Power BI

## Tech Stack

- AWS S3
- Amazon Redshift Serverless
- dbt Core
- Apache Airflow
- FastAPI
- Kafka
- Redis
- Power BI

## Features

- Batch ingestion (historical data)
- Streaming ingestion (near real-time simulation)
- Data lake structure (raw / silver / gold)
- Warehouse modeling (fact + dimension)
- Orchestration with Airflow
- API serving layer
- BI-ready data marts

## Project Goal

Simulate a modern production data platform combining:
- Batch ETL pipelines
- Event-driven streaming
- Cloud storage and warehouse
- Data modeling and transformation
- API and dashboard consumption
