{{ config(materialized='table') }}

WITH pivot AS (
    SELECT  
        data,
        MAX(CASE WHEN indicador = 'selic' THEN valor END) AS selic,
        MAX(CASE WHEN indicador = 'ipca' THEN valor END) AS ipca_raw
    FROM {{ref('mart_indicadores')}}
    GROUP BY data

),
-- marca
marcado AS (
    SELECT  
        data,
        selic,
        ipca_raw,
        CASE WHEN ipca_raw IS NOT NULL THEN 1 ELSE 0 END AS tem_valor_novo
    FROM pivot
),
--agrupa
agrupado AS (
    SELECT 
        data,
        selic,
        ipca_raw,
        SUM(tem_valor_novo) OVER (ORDER BY data) AS grupo
    FROM marcado
),
--preenche
preenchido AS (

    SELECT
        data,
        selic,
        MAX(ipca_raw) OVER (PARTITION BY grupo) AS ipca
    FROM agrupado
)
--calcula
SELECT
    data,
    selic,
    ipca,
    selic - ipca AS juro_real
FROM preenchido
WHERE selic IS NOT NULL

