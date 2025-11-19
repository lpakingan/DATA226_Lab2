SELECT
    symbol,
    date,
    open,
    close,
    min as low,
    max as high,
    volume
FROM USER_DB_CAMEL.raw.lab2_market_data