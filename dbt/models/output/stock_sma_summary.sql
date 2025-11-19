WITH base AS (

    SELECT
        symbol,
        date,
        close
    FROM {{ ref('market_data') }}

),

stock_day AS (

    SELECT
        symbol,
        date,
        close,
        ROW_NUMBER() OVER (
            PARTITION BY symbol
            ORDER BY date
        ) AS row_number
    FROM base

),

stock_sma AS (

    SELECT
        symbol,
        date,
        close,

        CASE
            WHEN row_number >= 7 THEN
                AVG(close) OVER (
                    PARTITION BY symbol
                    ORDER BY date
                    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
                )
        END AS sma_7d,

        CASE
            WHEN row_number >= 30 THEN
                AVG(close) OVER (
                    PARTITION BY symbol
                    ORDER BY date
                    ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
                )
        END AS sma_30d

    FROM stock_day
)

SELECT
    symbol,
    date,
    close,
    sma_7d,
    sma_30d
FROM stock_sma
