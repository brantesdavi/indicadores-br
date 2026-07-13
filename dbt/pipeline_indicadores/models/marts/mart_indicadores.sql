{{ config(materialized='table') }}

WITH base AS (
    SELECT
        data,
        valor,
        indicador,
        LAG(valor) OVER (
            PARTITION BY indicador
            ORDER BY data
        ) AS valor_anterior
    FROM {{ ref('stg_indicadores_bcb') }}
)

SELECT 
    *,
    (valor - valor_anterior) / NULLIF(valor_anterior, 0) as variacao
FROM base

