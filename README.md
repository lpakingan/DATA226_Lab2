# DATA226 Lab 2 — Stock ETL Pipeline

**Authors**: Liana Pakingan, Louisa Stumpf  
**Course**: DATA 226 - Data Warehouse

---

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Usage Instructions](#usage-instructions)
- [Validation](#validation)
- [Assumptions & Limitations](#assumptions--limitations)
- [Future Enhancements](#future-enhancements)


## Overview

This repository implements an end-to-end data pipeline that extracts stock price data from the `yfinance` API, loads the data into Snowflake, and performs ELT transformations with dbt. Apache Airflow orchestrates and schedules the workflow.

The pipeline includes:

- **ETL DAG (`180DayStockData`)**
   - Reads two stock symbols from Airflow Variables  
   - Uses `yfinance` to fetch 180 days of historical data  
   - Cleans the data using Pandas  
   - Loads the data into Snowflake (`raw.lab2_market_data`)

- **ELT DAG (`dbtDAG`)**
   - Transforms and cleans the raw data into analytics-ready tables
   - Runs dbt commands against Snowflake  
   - Builds cleaned/curated tables from the raw data  
   - Optional data tests validate the transformed outputs

The project demonstrates a modern cloud-based pipeline following an Extract → Load → Transform pattern.


## Architecture

1. **Airflow DAG #1**  
   - Reads two stock symbols from Airflow Variables  
   - Uses `yfinance` to fetch 180 days of historical data  
   - Cleans the data using Pandas  
   - Loads the data into Snowflake (`raw.lab2_market_data`)

2. **Airflow DAG #2 (dbtDAG)**  
   - Runs dbt commands against Snowflake  
   - Builds cleaned/curated tables from the raw data  
   - Optional data tests validate the transformed outputs

3. **Optional Notebooks**  
   - In the `visualization/` folder, you may add notebooks to analyze or plot the transformed results.


## Prerequisites

Before running the project, ensure you have:

- Docker & Docker Compose installed
- A Snowflake account with write access to your target schema
- Airflow running through the provided `docker-compose.yaml`
- Python packages such as:
  ```
  yfinance
  snowflake-connector-python
  pandas
  dbt-snowflake
  ```

## Setup Instructions

### 1. Start Airflow

```
docker-compose up -d
```

Wait for the Airflow webserver and scheduler to start.

### 2. Configure Airflow Variables

In the Airflow UI (`http://localhost:8080`):

Create the following variables:

- `first_stock_symbol` (example: LLY)
- `second_stock_symbol` (example: MNRA)

### 3. Configure the Snowflake Connection

In **Airflow → Admin → Connections**, create a connection:

- Conn ID: `snowflake_conn`
- Conn Type: Snowflake
- Fill in: account, user, password, warehouse, database, role
- Fill in Snowflake Schema as: `RAW`


## Usage Instructions

### Step 1 — Run the ETL DAG

Trigger the DAG:

```
180DayStockData
```

This will:

- Fetch two stocks from Airflow Variables  
- Pull ~180 days of price history  
- Load the data into Snowflake  

### Step 2 — Run the ELT DAG

Trigger:

```
dbtDAG
```

This will:

- Run `dbt run`  
- Optionally execute tests (`dbt test`)  
- Build transformed tables in Snowflake  

You can also set up a dependency so `dbtDAG` runs automatically after `180DayStockData`.


## Validation

### Check the raw table in Snowflake:

```SELECT symbol, COUNT(*) AS record_count, MIN(date), MAX(date)
FROM raw.lab2_market_data
GROUP BY symbol
```

Query should return a record count of 180 for each stock symbol.

### Check transformed tables:

```sql
SELECT *
FROM analytics.stock_summary
LIMIT 20
```

The query returns the first 20 transformed stock records with columns such as `SYMBOL`, `DATE`, `CLOSE`, and calculated rolling metrics like `SMA_7D` and `SMA_30D`. Early rows show only closing prices, and SMA values appear once enough days of data are available, confirming that the dbt models successfully produced cleaned, analytics-ready stock data.


## Assumptions & Limitations

- The pipeline currently supports exactly **two** stock symbols.  
- The data window is fixed at approximately **180 days**.  
- yfinance data may occasionally lag or contain missing timestamps.   
- dbt transformations assume the raw table already exists and contains valid data.


## Future Enhancements

- Expand to support a dynamic list of ticker symbols  
- Add incremental loading logic  
- Automate `dbtDAG` to run after ETL completion   
- Add CI/CD for dbt using GitHub Actions  
