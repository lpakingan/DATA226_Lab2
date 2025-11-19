
  create or replace   view USER_DB_CAMEL.analytics.market_data
  
   as (
    SELECT
    symbol,
    date,
    open,
    close,
    min as low,
    max as high,
    volume
FROM USER_DB_CAMEL.raw.lab2_market_data
  );

