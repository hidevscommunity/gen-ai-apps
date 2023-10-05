import pandas as pd
import altair as alt
import streamlit as st

# Cargar los datos de precios en un DataFrame de Pandas
df = pd.read_csv('./Operativa/Diarios-ES.csv')

# Convertir la columna 'dia' a un tipo de fecha
df['dia'] = pd.to_datetime(df['dia'], format='%m/%d/%Y', errors = 'coerce')

# Filtrar los datos por la columna de cierre (close)
df_filtrado = df[['dia', 'close']]

# Renombrar la columna de cierre a 'precio'
df_filtrado = df_filtrado.rename(columns={'close': 'precio'})

# Convertir la columna 'fecha_hora' a un tipo de fecha
df_filtrado['fecha_hora'] = pd.to_datetime(df_filtrado['dia'], format='%m/%d/%Y %H:%M')

# Crear un gráfico de Altair que muestre los precios por intervalos de 15 minutos
grafico = alt.Chart(df_filtrado).mark_line().encode(
    x='fecha_hora:T',
    y=alt.Y('precio:Q', scale=alt.Scale(type='log'))
).properties(
    width=800,
    height=400,
    title='Precios de cierre'
)

# Mostrar el gráfico en Streamlit
st.altair_chart(grafico)
