{% snapshot snapshot_stock_sma_summary %}

{{
  config(
    target_schema = 'snapshots',   
    unique_key    = "symbol || ' ' || date", 
    strategy      = 'check',
    check_cols    = ['close', 'sma_7d', 'sma_30d']
  )
}}

SELECT * FROM {{ ref('stock_sma_summary') }}

{% endsnapshot %}
