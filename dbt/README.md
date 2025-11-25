This dbt project that transforms raw historical stock price data into cleaned, analytics-ready tables with **simple moving average (SMA)** indicators (e.g., 7-day and 30-day SMAs) for each symbol and date.

---

## Overview

This project takes raw daily stock price data from yfinance and builds the following pipeline:

1. **Staging layer** – Standardized and cleaned version of the raw data.
2. **Analytics layer** – Final analytics model that calculates **simple moving averages** over rolling windows (e.g., 7-day, 30-day).

---

## Models

This dbt project contains two core models:

### 1. `market_data` (staging model)

The `market_data` model ingests records from the raw stock price table and prepares them for analytics by ensuring that data fields follow Snowflake naming conventions (i.e. renaming reserved min/max to low/high).


### 2. `stock_sma_summary` (analytics model)

The `stock_sma_summary` model takes relevant columns from the created `market_data` view and calculates **simple moving average (SMA)** indicators for each symbol and date if enough historical data exists for a full 7d/30d calculation. The created summary table can be used to create visualizations.
