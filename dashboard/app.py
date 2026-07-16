from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
#assim ele descobre a apsta raiz automaticamente

from db import get_engine
import pandas as pd
import streamlit as st

engine = get_engine()


df_atual = pd.read_sql("""
    WITH ultimas_datas AS (
        SELECT indicador, MAX(data) AS ultima_data
        FROM mart_indicadores
        GROUP BY indicador
    )

    SELECT m.data, m.valor, m.indicador
    FROM mart_indicadores m
    JOIN ultimas_datas u
        ON m.indicador = u.indicador
        AND m.data = u.ultima_data                 
""", engine)

df_juro_real = pd.read_sql("""
    SELECT * FROM mart_juro_real
    ORDER BY data DESC LIMIT 1
""", engine)

df_historico = pd.read_sql("""
    SELECT * FROM mart_juro_real
    ORDER BY data DESC LIMIT 180
""", engine)

st.title("Painel de Indicadores Econômicos")

col1, col2, col3, col4 = st.columns(4)

with col1:
    selic_row = df_atual[df_atual["indicador"] == "selic"].iloc[0]
    st.metric(label="Selic",value=f"{selic_row["valor"]:.2f}%")

with col2:
    cdi_row = df_atual[df_atual["indicador"] == "cdi"].iloc[0]
    st.metric(label="CDI",value=f"{cdi_row["valor"]:.2f}%")

with col3:
    dollar_row = df_atual[df_atual["indicador"] == "dolar"].iloc[0]
    st.metric(label="Dolar",value=f"R$ {dollar_row["valor"]:.2f}")

with col4:
    ipca_row = df_atual[df_atual["indicador"] == "ipca"].iloc[0]
    st.metric(label="IPCA",value=f"{ipca_row["valor"]:.2f}%")

juro_row = df_juro_real.iloc[0]
st.metric(label="Juro Real (aproximado)", value=f"{juro_row['juro_real']:.2f}%")

st.write("Juro real por periodo")
st.line_chart(df_historico.set_index("data")[["juro_real"]])

col_a, col_b = st.columns(2)

with col_a:
    st.write("Selic")
    st.line_chart(df_historico.set_index('data')[["selic"]])
with col_b:
    st.write("IPCA")
    st.line_chart(df_historico.set_index('data')[["ipca"]])