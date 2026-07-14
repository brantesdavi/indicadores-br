SELECT
    data,
    valor,
    indicador
FROM {{ source('raw', 'raw_indicadores_bcb') }}