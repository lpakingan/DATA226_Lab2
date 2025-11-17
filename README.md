# Data226 Lab 2

**Course:** Data226  
**Project:** Lab 2 — Stock ETL + ELT Transformation with Airflow, Snowflake & dbt
**Authors:** Liana Pakingan, Louisa Stumpf   

---

## Overview
This repo contains two Airflow DAGs that demonstrate an end-to-end pipeline using **Snowflake**:

1. **ETL DAG (`180DayStockData`)**  
   - Extracts 180 days of stock prices from Yahoo Finance.  
   - Transforms data into a clean tabular format.  
   - Loads it into Snowflake (`raw.lab2_market_data`).  

2. **ETL DAG (`dbtDAG`)**  

---

## Setup
- Configure a Snowflake connection in Airflow (`snowflake_conn`) with account, user, password, warehouse, database, and role.
- Configure variables `first_stock_symbol` and `second_stock_symbol` in Airflow with two stock symbols of your choice.
- Install required Python packages: `yfinance`, `snowflake-connector-python`, `pandas`, `dbt-snowflake`.

---

## Running
1. Start Airflow (`docker-compose up -d` if using the provided config).  
2. Add your DAGs to the `dags/` folder.  
3. Trigger `180DayStockData` first, then `dbtDAG`.  
   - Or set up a dependency so `dbtDAG` waits for `180DayStockData`.  

---



