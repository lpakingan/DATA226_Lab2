from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

from datetime import timedelta
from datetime import datetime
import snowflake.connector

import yfinance as yf

def return_snowflake_conn():
  """
  Create connection with Snowflake
  """
  # Initialize the SnowflakeHook
  hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')

  # Execute the query and fetch results
  conn = hook.get_conn()
  return conn.cursor()

# ------------------- EXTRACT -------------------
@task
def extract(symbol1, symbol2):
  """
  Download 180 days of stock data for 2 symbols.
  """
  stock_data = yf.download([f'{symbol1}', f'{symbol2}'], period = '180d')
  return stock_data

# ------------------- TRANSFORM -------------------
@task
def transform(stock_data):
  """
  Formats the last 180 days of the stock prices of the two stocks into the format of the table
  """
  stock_data = stock_data.stack()
  transformed_stock_data = stock_data.reset_index()

  return transformed_stock_data

# ------------------- LOAD -------------------
@task
def load(stock_data, target_table):
  """
  Full refresh load into Snowflake.
  """
  cur = return_snowflake_conn()
  try:
      cur.execute("BEGIN;")
      cur.execute(f"""CREATE TABLE IF NOT EXISTS {target_table} (
        symbol  VARCHAR,
        date    DATE,
        open    FLOAT,
        close   FLOAT,
        min     FLOAT,
        max     FLOAT,
        volume  INT,
        PRIMARY KEY (symbol, date)
        );
        """)
      cur.execute(f"""DELETE FROM {target_table}""")
      for index, record in stock_data.iterrows():
        symbol = record["Ticker"]
        date = record["Date"]
        open = record["Open"]
        close = record["Close"]
        min = record["Low"]
        max = record["High"]
        volume = record["Volume"]
        insert_sql = f"INSERT INTO {target_table} (symbol, date, open, close, min, max, volume) VALUES ('{symbol}', '{date}', {open}, {close}, {min}, {max}, {volume})"
        print(insert_sql)
        cur.execute(insert_sql)
      cur.execute("COMMIT;")
  except Exception as e:
      cur.execute("ROLLBACK;")
      print(e)
      raise e

# DAG
with DAG(
    dag_id = '180DayStockData',
    start_date = datetime(2025,11,11),
    catchup = False,
    max_active_runs = 1,
    tags = ['ETL'],
    schedule = None
) as dag:
    target_table = "raw.lab2_market_data"
    symbol1 = Variable.get("first_stock_symbol")
    symbol2 = Variable.get("second_stock_symbol")

    data = extract(symbol1, symbol2)
    stocks_data = transform(data)
    load(stocks_data, target_table)