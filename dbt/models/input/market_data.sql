SELECT
    symbol,
    date,
    open,
    close,
    min as low,
    max as high,
    volume
FROM {{ source('raw', 'lab2_market_data') }}
