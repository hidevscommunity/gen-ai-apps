# Importar las librerías necesarias
from src.datos import *
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from bokeh.plotting import figure
import datetime as dt
import ta
from textos import *
from sklearn.preprocessing import StandardScaler
from datetime import timedelta
import datetime
import plotly.express as px
from scipy.stats import norm
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots
from sklearn.cluster import KMeans
from scipy.interpolate import make_interp_spline
from datetime import datetime, timedelta




    

st.set_page_config(page_title="Mi tablero de Streamlit",
                page_icon=":guardsman:",
                layout="wide",
                initial_sidebar_state="expanded"                
                )
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)



    
# Cargar la imagen de logo
with open("fintra-logo-blanco.png", 'rb') as img:
    st.image(img.read(), width=200)
    
    
    

# Utilizar una estructura de control de flujo más clara
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab11, tab12= st.tabs(["Reporte de Mercado", "Estadísticas ES_F", "Gráficos ES_F", "Opciones 0DTE", "Charts Índices", "Charts Acciones", "Meme Stocks", "Gamma", "CotReport", "Estadísticas CBOE", "Estadísticas Macroeconómicas"])

with tab1:

    def mostrar_sidebar():
        data_source = st.sidebar.selectbox("Selecciona un fichero de datos", list(renombre.values()))

        for archivo, nombre_amigable in renombre.items():
            if data_source == nombre_amigable:
                if archivo == "./Operativa/processed/Diarios-ES.csv":
                    df = df_diarios_ES
                else:
                    df = df_diarios_NQ
                break
        return df

    st.sidebar.title("Fuente de datos")
    df = mostrar_sidebar()

   

    # Título de la sección
    st.header('Día 05/09/2023')
    


    # Introducción
    st.write(txt_comentario)
    st.image("./img/Julio/25Julio/callvolume.png")
    st.image("./img/Julio/25Julio/putvolume.png")
    st.image("./img/Julio/25Julio/calloi.png")
    st.image("./img/Julio/25Julio/putoi.png")
    #ppner imagen
    #st.image("./img/5Mayo/cme-liquidez.jpeg")
    st.image("./img/Julio/25Julio/gamma.png")  
    # Gráfico de precios de la semana
    st.subheader('Niveles importantes')
    st.write(txt_niveles)
    st.write(txt_sentiment)
    st.image("./img/Julio/25Julio/callnet.png")
    st.image("./img/Julio/25Julio/putnet.png")
    
    # Análisis de los principales movimientos del mercado
    st.subheader('Planteamiento y escenarios operativos')
    st.write(txt_esperamos)
    st.image("./img/Julio/25Julio/estructura.png")
    
    # Volatilidad
    st.subheader('Volatilidad')
    st.write(txt_volatilidad)
    st.image("./img/Julio/25Julio/volatilidad.png") 




    st.info(title_esta_semana, icon="ℹ️")
    st.caption(esta_semana1)
    st.caption(esta_semana2)
    st.caption(esta_semana3)
    st.caption(esta_semana4)
    st.caption(esta_semana5)


    
    
with tab2: 
    
    st.subheader("Últimos 2 días")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1).tail(2))
    
    st.subheader("Estadísticas generales")
    # Mostrar la tabla completa al iniciar el programa
    st.dataframe(df.drop("Unnamed: 0", axis=1))
    
    st.subheader("Estadísticas por rango de fechas")
    # Crear campos de entrada de fecha
    fecha_inicio = st.date_input("Selecciona una fecha de inicio")
    fecha_fin = st.date_input("Selecciona una fecha de fin")
    df["Date"] = pd.to_datetime(df["Date"])
    


    try:
        # Crear un botón para aplicar el filtro
        if st.button("Aplicar filtro"):
            # Filtrar la base de datos
            df_filtrado = df.drop("Unnamed: 0", axis=1)[(df["Date"].dt.date >= fecha_inicio) & (df["Date"].dt.date <= fecha_fin)]
            # Mostrar la tabla con los datos filtrados
            st.dataframe(df_filtrado)

        st.subheader("Estadísticas descriptivas")
        # Excluir columnas no numéricas
        numeric_columns = df.select_dtypes(include=[float, int]).columns
        df_numeric2 = df[numeric_columns]
        df_numeric2 = df_numeric2.drop("Unnamed: 0", axis=1)
        st.write(df_numeric2.describe().round(2))

        st.subheader("HeatMap")
        # Excluir columnas no numéricas
        numeric_columns = df.select_dtypes(include=[float, int]).columns
        df_numeric = df[numeric_columns]
        # Eliminar la columna "Unnamed:"
        df_numeric = df_numeric.drop("Unnamed: 0", axis=1)
        # Calcular la matriz de correlaciones
        correlation_matrix = df_numeric.corr().reset_index().melt('index')

        # Crear el heatmap con Altair
        heatmap = alt.Chart(correlation_matrix).mark_rect().encode(
            x='index:O',
            y='variable:O',
            color='value:Q'
        ).properties(
            width=1000,
            height=800,
            title='Mapa de correlaciones'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(heatmap)


    except Exception as e:
        st.error(f"Error: {e}")







with tab3:
    

    

    # Filtro de periodo
    periodo = st.selectbox("Selecciona un periodo", ["1 día", "1 semana", "1 mes", "Todo"], index=3)

    if periodo == "1 día":
        df_filtered = df[-1:]
    elif periodo == "1 semana":
        df_filtered = df[-7:]
    elif periodo == "1 mes":
        df_filtered = df[-30:]
    else:
        df_filtered = df

    # Dividir la pantalla en dos columnas
    col1, col2 = st.columns(2)

    # Gráfico de Líneas - Evolución del Precio de Cierre
    line_chart = px.line(df_filtered, x='Date', y=['Closing Price',"Day's High","Day's Low"], title='Evolución del Precio de Cierre')
    col1.plotly_chart(line_chart, use_container_width=True)

    # Crear el gráfico de área
    area_chart = px.line(df_filtered, x='Date', y=['Range in ticks'], title='Rango en ticks')

    # Agregar el precio de cierre al eje y derecho
    area_chart.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Closing Price'],
                                mode='lines', name='Closing Price', yaxis='y2'))

    # Configurar el eje y derecho
    area_chart.update_layout(yaxis2=dict(title='Closing Price', side='right', overlaying='y'))

    # Configurar el tipo de gráfico a "stacked"
    area_chart.update_layout(barmode='stack')

    # Mostrar el gráfico
    col2.plotly_chart(area_chart, use_container_width=True)


    # Calcular el volumen acumulado semanalmente
    df_filtered['Volumen Acumulado'] = df_filtered['Volume'].cumsum()
    # Actualizar el gráfico de dispersión con el volumen acumulado
    scatter_chart = px.scatter(df_filtered, x='Closing Price', y=['Volumen Acumulado'], title='Relación entre Precio de Cierre y Volumen Acumulado')
    col1.plotly_chart(scatter_chart, use_container_width=True)

    # Gráfico de Área - Volumen Value Area
    area_chart = px.line(df_filtered, x='Date', y=['Volume Value Area Low', 'Volume Value Area High', 'Volume in Vpoc Zone'], title='Volumen Value Area')
    col2.plotly_chart(area_chart, use_container_width=True)


    # Gráfico de Dispersión - Relación entre Precio de Cierre y Volumen
    scatter_chart = px.scatter(df_filtered, x='Closing Price', y='Volume', title='Relación entre Precio de Cierre y Volumen')
    col1.plotly_chart(scatter_chart, use_container_width=True)
    
    


    # Obtener el recuento de volumen por día de la semana
    volume_counts = df_filtered['Weekday'].value_counts().sort_index()

    # Calcular los porcentajes de volumen por día de la semana
    volume_percentages = volume_counts / volume_counts.sum() * 100

    # Crear un nuevo DataFrame con los días de la semana y sus porcentajes de volumen
    volume_data = pd.DataFrame({'Día de la Semana': volume_percentages.index, 'Porcentaje de Volumen': volume_percentages.values})

    #Gráfico de Violín - Distribución de Rendimientos
    violin_chart = px.violin(df_filtered, y='Volume', title='Distribución de Volumen')
    col2.plotly_chart(violin_chart, use_container_width=True)

    #Gráfico de Líneas - VIX y VIX1D
    vix_line_chart = px.line(df_filtered, x='Date', y=['VIX Closing Price', 'vix_0dte'], title='VIX y VIX1D')
    col1.plotly_chart(vix_line_chart, use_container_width=True)


    

    # Calcular la media móvil de 50 días
    df['SMA_50'] = df['Closing Price'].rolling(window=50).mean()

    # Calcular la diferencia entre el precio de cierre y la apertura
    df['Price_Diff'] = df['Closing Price'] - df['Opening']

    # Calcular la tendencia (1 si el precio es mayor que la media móvil, -1 si es menor, 0 si es neutral)
    df['Trend'] = np.where(df['Price_Diff'] > 15, 1, np.where(df['Price_Diff'] < -15, -1, 0))

    # Mapear los valores de tendencia a etiquetas descriptivas
    trend_labels = {1: 'Tendencia Alcista', -1: 'Tendencia Bajista', 0: 'Tendencia Lateral'}
    df['Trend'] = df['Trend'].map(trend_labels)

    # Filtrar el DataFrame según el periodo seleccionado
    if periodo == "1 día":
        df_filtered = df[-1:]
    elif periodo == "1 semana":
        df_filtered = df[-7:]
    elif periodo == "1 mes":
        df_filtered = df[-30:]
    else:
        df_filtered = df

    # Obtener el recuento de cada categoría de tendencia
    trend_counts = df_filtered['Trend'].value_counts().sort_index()

    # Calcular los porcentajes de cada categoría
    trend_percentages = trend_counts / trend_counts.sum() * 100

    # Crear un nuevo DataFrame con las categorías y sus porcentajes
    trend_data = pd.DataFrame({'Tendencia': trend_percentages.index, 'Porcentaje': trend_percentages.values})

    # Definir los colores para cada categoría de tendencia
    colors = {'Tendencia Alcista': 'lightgreen', 'Tendencia Bajista': 'lightcoral', 'Tendencia Lateral': 'lightgray'}

    # Crear el gráfico de tarta con los colores personalizados
    trend_chart = go.Figure(data=[go.Pie(labels=trend_data['Tendencia'], values=trend_data['Porcentaje'], marker=dict(colors=[colors[t] for t in trend_data['Tendencia']]))])

    # Configurar el título del gráfico
    trend_chart.update_layout(title='Tendencia de Precios')

    col1.plotly_chart(trend_chart, use_container_width=True)











    #Gráfico de Área - Volumen en Zonas de Punto de Control
    vpoc_chart = px.area(df_filtered, x='Date', y='Volume in Vpoc Zone', title='Volumen en Zonas de Punto de Control')
    col2.plotly_chart(vpoc_chart, use_container_width=True)
    
    # Filtrar los datos por encima y por debajo de 4000
    above_4000_data = df_filtered[df_filtered['Closing Price'] > 4000]
    below_4000_data = df_filtered[df_filtered['Closing Price'] <= 4000]

    # Combinar los datos en un único DataFrame
    combined_data = pd.concat([above_4000_data, below_4000_data])

    # Asignar colores a las barras según la condición
    combined_data['Color'] = np.where(combined_data['Closing Price'] > 4000, '> 4000', '< 4000')

    # Gráfico de Barras - Precios por Encima y por Debajo de 4000
    combined_chart = px.scatter(combined_data, x='Date', y='Closing Price', title='Precios por Encima y por Debajo de 4000', color='Color')
    col2.plotly_chart(combined_chart, use_container_width=True)
    
    
    # Gráfico de Barra - Volumen por Día de la Semana
    volume_bar_chart = px.bar(df_filtered, x='Weekday', y='Volume', title='Volumen por Día de la Semana')

    # Configurar el ancho del contenedor al 100%
    volume_bar_chart.update_layout(width=800, height=400)

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(volume_bar_chart, use_container_width=True)

    # Obtener el recuento de volumen por día de la semana
    volume_counts = df_filtered['Weekday'].value_counts().sort_index()

    # Calcular los porcentajes de volumen por día de la semana
    volume_percentages = volume_counts / volume_counts.sum() * 100

    # Crear un nuevo DataFrame con los días de la semana y sus porcentajes de volumen
    volume_data = pd.DataFrame({'Día de la Semana': volume_percentages.index, 'Porcentaje de Volumen': volume_percentages.values})

    



    # Convertir la columna "dia" a tipo datetime
    data_OI['dia'] = pd.to_datetime(data_OI['dia'])

    # Crear gráfico utilizando Altair y filtrar los días de fin de semana
    chart = alt.Chart(data_OI[data_OI['dia'].dt.weekday < 5]).encode(
        x='dia:T',
        tooltip=['dia']
    )

    # Gráfico de barras para el volumen de operaciones
    bar_chart = chart.mark_bar(opacity=0.7, color='cyan').encode(
        y='volume:Q',
        tooltip=['volume']
    ).properties(
        title='Volumen y Open Interest minisp500'
    )

    # Gráfico de línea para la variable OI
    line_chart = chart.mark_line(color='orange').encode(
        y='oi:Q',
        tooltip=['oi']
    ).properties(
        title='Open Interest'
    )

    # Combinar los gráficos de barras y línea
    chart_combined = alt.layer(bar_chart, line_chart).resolve_scale(y='independent')

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart_combined, use_container_width=True)






    # Calcular el drawdown diario
    df_filtered['Daily Drawdown'] = (df_filtered['Closing Price'].shift(1).cummax() - df_filtered['Closing Price']) / df_filtered['Closing Price'].shift(1)

    # Calcular el drawdown acumulado
    df_filtered['Cumulative Drawdown'] = (df_filtered['Closing Price'].cummax() - df_filtered['Closing Price']) / df_filtered['Closing Price'].cummax()

    # Calcular el máximo drawdown
    max_drawdown = df_filtered['Cumulative Drawdown'].max()

    # Calcular la ganancia acumulada
    df_filtered['Cumulative Gain'] = (df_filtered['Closing Price'] - df_filtered['Closing Price'].cummin()) / df_filtered['Closing Price'].cummin()

    # Calcular la máxima ganancia
    max_gain = df_filtered['Cumulative Gain'].max()

    # Multiplicar el drawdown y la ganancia por -1 y convertirlos en porcentajes
    df_filtered['Cumulative Drawdown'] = df_filtered['Cumulative Drawdown'] * -100
    df_filtered['Cumulative Gain'] = df_filtered['Cumulative Gain'] * 100
    
    # Crear dataframe para el máximo drawdown
    drawdown_df = pd.DataFrame({'Fecha': df_filtered['Date'], 'Drawdown': df_filtered['Cumulative Drawdown']})

    # Crear dataframe para la máxima ganancia
    gain_df = pd.DataFrame({'Fecha': df_filtered['Date'], 'Ganancia': df_filtered['Cumulative Gain']})
    
    # Eliminar el valor 0 del dataframe de ganancias
    gain_df = gain_df[gain_df['Ganancia'] != 0]
    
    # Eliminar el valor 0 del dataframe de ganancias
    drawdown_df = drawdown_df[drawdown_df['Drawdown'] != 0]
    
    # Gráfico de Líneas - Máximo Drawdown y Máxima Ganancia
    drawdown_chart = go.Figure()

    # Agregar el área de drawdown en rojo
    drawdown_chart.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Cumulative Drawdown'], fill='tozeroy', fillcolor='red', line_color='red', name='Pérdida'))

    # Agregar el área de ganancia en verde
    drawdown_chart.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Cumulative Gain'], fill='tozeroy', fillcolor='green', line_color='green', name='Ganancia'))

    # Configurar la leyenda
    drawdown_chart.update_layout(legend_title='Filtro', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1))

    # Configurar el título del gráfico
    drawdown_chart.update_layout(title='Máxima Pérdida y Ganancia')

    # Mostrar el gráfico de drawdown y ganancia
    st.plotly_chart(drawdown_chart, use_container_width=True)








    @st.cache_data
    def model(x_name, y_name, predict_value, num_days):
        x = df[x_name].dropna().values.reshape(-1, 1)
        y = df[y_name].dropna().values.reshape(-1, 1)

        sc_x = StandardScaler()
        sc_y = StandardScaler()

        x_std = sc_x.fit_transform(x)
        y_std = sc_y.fit_transform(y)

        slr = LinearRegression()
        slr.fit(x_std, y_std)

        predict_values_std = sc_x.transform(np.array([predict_value + i for i in range(num_days)]).reshape(-1, 1))
        predictions = slr.predict(predict_values_std)
        predictions = sc_y.inverse_transform(predictions)
            
        return x_std, y_std, slr, predictions

  










    #DELTAS
    
    # Transformar la columna 'Date' a formato fecha
    df['Date'] = pd.to_datetime(df['Date'])



    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(df, x='Date', y='Delta',
                color='Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Delta': 'Deltas'},
                title=f'Delta ')

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=df['Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(df['Date']), y0=0, x1=max(df['Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')

    # Mostrar el gráfico de barras en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    
    
    
    ########### VARIACION PORCENTUAL DEL PRECIO DE CIERRE ###########
    # Calcular la variación porcentual del precio de cierre
    df['Daily_Return'] = df['Closing Price'].pct_change() * 100

    # Crear el gráfico de barras con Plotly Express
    fig = px.bar(df, x='Date', y='Daily_Return',
                color='Daily_Return',
                color_continuous_scale='RdYlGn',  # Escala de colores para positivo (verde) y negativo (rojo)
                labels={'Daily_Return': 'Variación Porcentual'},
                title='Variación Porcentual Diaria del Precio de Cierre')

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(df['Date']), y0=0, x1=max(df['Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y la variación porcentual
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.2f}%')

    # Mostrar el gráfico de barras en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    
    
    
    
    
    
    
    
    
      # Mostrar tabla de datos con 2 inputs
    # Mostrar gráfico de dispersión de dos columnas
    col_x = st.selectbox('Selecciona una columna para el eje x', df.drop("Unnamed: 0", axis=1).columns)
    col_y = st.selectbox('Selecciona una columna para el eje y', df.drop("Unnamed: 0", axis=1).columns)
    tipo_grafico = st.selectbox("Seleccione el tipo de gráfico", ["Linea", "Puntos", "Barras"], index=0)


    if tipo_grafico == "Linea":
        line_plot = alt.Chart(df).mark_line().encode(
            x=col_x,
            y=col_y,
            tooltip=[col_x, col_y]
        ).interactive()
        st.write("### Gráfico de Línea " + col_x + " vs " + col_y)
        st.altair_chart(line_plot, use_container_width=True)
    elif tipo_grafico == "Puntos":
        scatter_plot = alt.Chart(df).mark_circle().encode(
            x=col_x,
            y=col_y,
            tooltip=[col_x, col_y]
        ).interactive()
        st.write("### Gráfico de Puntos " + col_x + " vs " + col_y)
        st.altair_chart(scatter_plot, use_container_width=True)
    else:
        bar_plot = alt.Chart(df).mark_bar().encode(
            x=col_x,
            y=col_y,
            tooltip=[col_x, col_y]
        ).interactive()
        st.write("### Gráfico de Barras " + col_x + " vs " + col_y)
        st.altair_chart(bar_plot, use_container_width=True)

    
    
    
    
    
    
    ######################   FORECAST #######################
    
    
    

    st.subheader("Regresión Linea para hacer predicciones a un día")

    x_name = st.selectbox("Selecciona la variable independiente", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])

    y_name = st.selectbox("Selecciona la variable a predecir", ["Closing Price", "VIX Closing Price", "Volume", "Opening", "Day's High", "Day's Low", "Vpoc", "Vwap", "Range in ticks"])
    latest_date = df['Date'].max() - timedelta(days=1)
    latest_row = df[df['Date'] == latest_date][x_name]
    if not latest_row.empty:
        predict_value = st.number_input("Último valor de la variable independiente en ayer o ingresa los datos que deseas hacer una relación y con ello tendrás una predicción(" + x_name + "):", value=latest_row.values[0])
    else:
        predict_value = st.number_input("Último valor de la variable independiente en ayer o ingresa los datos que deseas hacer una relación y con ello tendrás una predicción(" + x_name + "):")


    x_std, y_std, slr, prediction = model(x_name, y_name, predict_value, 1)

    scatter = alt.Chart(pd.DataFrame({
        "x": x_std.flatten(),
        "y": y_std.flatten()
    })).mark_circle().encode(
        x='x',
        y='y'
    )

    line = alt.Chart(pd.DataFrame({
        "x": x_std.flatten(),
        "y": slr.predict(x_std).flatten()
    })).mark_line(color='orange').encode(
        x='x',
        y='y'
    )

    st.altair_chart(scatter + line, use_container_width=True)


    variable_dependiente = y_name

    st.write("La predicción para la variable: ", variable_dependiente, "es", prediction[0][0])

    
    
    
    
    
       
    
    
#ZONA DE PRUEBAS
    
    

        
        
        
    
    
    
    
    
    
    
    
with tab4:
    
    

    

    # Mostrar la tabla completa al iniciar el programa
    st.subheader('Opciones con expiración diarias 0DTE')
    st.caption('Las opciones sobre acciones son importantes porque ofrecen oportunidades comerciales rápidas y pueden influir en el mercado de futuros. Los operadores de futuros deben estar atentos a estas opciones para aprovechar las oportunidades y minimizar los riesgos.')
    
    ticker_input = st.text_input("Ingrese el nombre, ticker del Índice o Acción:","SPX")

    archivo_seleccionado = None

    # Buscar el archivo correspondiente basado en el ticker_input
    for archivo, datos in data_files.items():
        if ticker_input.lower() in archivo.lower():
            archivo_seleccionado = archivo
            df = pd.DataFrame(datos)
            break

    if archivo_seleccionado is None:
        st.write("Ticker o acción no encontrado")
        st.stop()

    # Crear lista de fechas únicas en la columna "Expiration Date"
    fechas_unicas = df['Expiration Date'].unique()

    # Selectbox para seleccionar la fecha de vencimiento
    fecha_seleccionada = st.selectbox(
        "Seleccione la fecha de vencimiento: ",
        fechas_unicas
    )

    # Filtrar el DataFrame para seleccionar solo las filas que corresponden a la fecha de vencimiento seleccionada
    df_filtrado = df[df['Expiration Date'] == fecha_seleccionada]

    # Obtener todos los valores de Strike en el DataFrame filtrado
    strikes = df_filtrado['Strike'].unique()

    # Crear un nuevo DataFrame con todos los valores de Strike y reindexar el DataFrame filtrado
    df_strikes = pd.DataFrame({'Strike': strikes})
    df_filtrado = pd.merge(df_filtrado, df_strikes, on='Strike', how='right').fillna(0)



    # Selección de la variable a graficar
    selected_vars = st.multiselect(
        "Selecciones la variable a graficar",
        [
            'Calls', 'Calls Last Sale', 'Calls Net','Calls Bid', 'Calls Ask','Calls Volume', 'Calls IV','Calls Delta',
            'Calls Gamma', 'Calls Open Interest', 'Strike', 'Puts', 'Puts Last Sale', 'Puts Net', 'Puts Bid', 'Puts Ask', 'Puts Volume',
            'Puts IV','Puts Delta', 'Puts Gamma', 'Puts Open Interest'
        ],
        default=["Calls Volume","Puts Volume", "Calls Open Interest", "Puts Open Interest"]
    )

    # Selección del tipo de gráfico
    tipo_grafico2 = st.selectbox(
        "Seleccione el tipo de gráfico",
        ["Bars", "Scatter"],
        key='tipo_grafico2',
        index=0
    )

    if len(selected_vars) > 0:
        fig = go.Figure()

        for variable in selected_vars:
            # Si el tipo de gráfico es línea
            if tipo_grafico2 == 'Bars':
                fig.add_trace(go.Bar(x=df_filtrado['Strike'], y=df_filtrado[variable],  name=variable))
            else:
                fig.add_trace(go.Scatter(x=df_filtrado['Strike'], y=df_filtrado[variable],  mode='markers', name=variable))

        # Personaliza los títulos y ejes del gráfico
        fig.update_layout(
            title=f'Chart of {", ".join(selected_vars)} to date {fecha_seleccionada}',
            xaxis_title= 'Strike',
            yaxis_title= variable,
            #barmode='relative',
            barmode= 'stack',
            xaxis=dict(
                tickmode='linear',
                tick0=df_filtrado['Strike'].min(),
                dtick=5
            )
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Por favor seleccione al menos una variable")




# Crear un DataFrame con los datos de interés
    df_top = df_filtrado[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest', 'Puts Net', 'Calls Net', 'Puts Gamma', 'Calls Gamma']]

    if archivo_seleccionado not in ["spx_quotedata.csv", "spy_quotedata.csv"]:
        st.markdown(f"**{archivo_seleccionado.replace('_quotedata.csv', '').upper()}**")
        st.dataframe(df_top)
    else:
        if archivo_seleccionado == "spx_quotedata.csv":
            df_top['Price'] = df_top['Strike'] + 35
        else:  # archivo_seleccionado == "spy_quotedata.csv"
            df_top['Price'] = df_top['Strike'] * 10

        df_top = df_top.sort_values(by=['Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest'], ascending=False)
        df_top = df_top.head(15)

        # Mostrar las dos tablas en dos columnas
        col1, col2 = st.columns(2)

        # En la primera columna, mostrar la tabla original con la columna "Strike"
        with col1:
            if ticker_input.upper() not in ["SPX", "SPY"]:
                st.dataframe(df_top[['Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']], width=0)
            else:
                st.markdown(f"**{ticker_input.upper()}**")
                st.dataframe(df_top[['Strike', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])

        # En la segunda columna, mostrar la tabla actualizada con la nueva columna "Nuevo Strike"
        with col2:
            st.write("**Futuros E-Mini S&P 500**")
            st.dataframe(df_top[['Price', 'Calls Volume', 'Calls Open Interest', 'Puts Volume', 'Puts Open Interest']])




    #CURVA VANNA CON DELTA NOTIONAL 0dte
    # Calcula las gammas individuales para Calls y Puts
    data['Gamma Calls'] = 0.5 * abs(data['Calls Net']) * data['Calls IV'] * (data['Calls Delta'])**2
    data['Gamma Puts'] = 0.5 * abs(data['Puts Net']) * data['Puts IV'] * (data['Puts Delta'])**2

    # Ajusta regresiones polinómicas de grado superior para Vanna Calls y Vanna Puts
    degree = 4  # Grado del polinomio (puedes ajustarlo según sea necesario)
    coefficients_calls = np.polyfit(data['Strike'], data['Gamma Calls'], degree)
    polynomial_calls = np.poly1d(coefficients_calls)

    coefficients_puts = np.polyfit(data['Strike'], data['Gamma Puts'], degree)
    polynomial_puts = np.poly1d(coefficients_puts)

    # Crea DataFrames para las curvas de Vanna Calls y Vanna Puts suavizadas
    smoothed_strikes = np.linspace(data['Strike'].min(), data['Strike'].max(), 1000)  # Interpola más puntos para suavizar la curva
    predicted_data_calls = pd.DataFrame({
        'Strike': smoothed_strikes,
        'Vanna Calls': polynomial_calls(smoothed_strikes)
    })

    predicted_data_puts = pd.DataFrame({
        'Strike': smoothed_strikes,
        'Vanna Puts': polynomial_puts(smoothed_strikes)
    })

    # Crea un gráfico con dos líneas curvadas para Vanna Calls y Vanna Puts
    chart = alt.Chart(predicted_data_calls).mark_line(color='green').encode(
        x=alt.X('Strike:O', axis=alt.Axis(format='d')),  # Formato de número entero en el eje x
        y='Vanna Calls:Q',
        tooltip=['Strike', 'Vanna Calls']
    ) + alt.Chart(predicted_data_puts).mark_line(color='red').encode(
        x=alt.X('Strike:O', axis=alt.Axis(format='d')),  # Formato de número entero en el eje x
        y='Vanna Puts:Q',
        tooltip=['Strike', 'Vanna Puts']
    )

    # Muestra el gráfico usando Streamlit
    st.title('Curvas de Vanna Suavizadas para Calls y Puts')
    st.altair_chart(chart, use_container_width=True)







    # Transformar Expiration Date a formato fecha
    data['Expiration Date'] = pd.to_datetime(data['Expiration Date'], format='%a %b %d %Y')

    # Agregar una columna para el total de deltas en cada Expiration Date
    data['Total Delta'] = data['Calls Delta'] + data['Puts Delta']

    # Crear el gráfico con Plotly Express
    fig = px.bar(data, x='Expiration Date', y='Total Delta',
                color='Total Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Total Delta': 'Deltas'},
                title=f"Delta {archivo_seleccionado.replace('_quotedata.csv', '').upper()}".upper())

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=data['Total Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(data['Expiration Date']), y0=0, x1=max(data['Expiration Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')



    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)






    # Código para el gráfico de sesgo de volatilidad con el eje X mejorado
    # Supongamos que tienes un DataFrame llamado "data" con las columnas necesarias

    # Calcular el sesgo de volatilidad (diferencia entre IV de calls y puts) en porcentaje
    data['Sesgo_IV'] = (data['Calls IV'] - data['Puts IV']) * 100  # Multiplicamos por 100 para convertirlo en porcentaje

    # Crear el gráfico de barras
    chart_sesgo_iv = alt.Chart(data).mark_bar().encode(
        x=alt.X('Strike:O', axis=alt.Axis(labelAngle=0), title='Precio de Ejercicio'),  # Rotar las etiquetas del eje X a 0 grados
        y=alt.Y('Sesgo_IV:Q', axis=alt.Axis(format='%'), title='Sesgo de Volatilidad (%)'),  # Formatear el eje Y como porcentaje
        color=alt.condition(alt.datum.Sesgo_IV >= 0, alt.value('orange'), alt.value('cyan')),
        tooltip=['Strike', 'Sesgo_IV']
    ).properties(
        title='Sesgo de Volatilidad (IV) de Calls y Puts por Precio de Ejercicio',
        width=800
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart_sesgo_iv, use_container_width=True)





    
    

                
    

    
    #PROBANDO CALCULAR VANNA JPMORGAN
    # Calcular el Vanna
    data['Vanna Calls'] = data['Calls Last Sale'] * data['Calls Delta'] * data['Calls IV']
    data['Vanna Puts'] = data['Puts Last Sale'] * data['Puts Delta'] * data['Puts IV']

    # Crear un gráfico de barras para mostrar el Vanna por Strike
    chart = alt.Chart(data).mark_bar().encode(
        x='Strike:O',  # Precio de Ejercicio en el eje x
        y=alt.Y('Vanna Calls:Q', title='Vanna Calls'),
        color=alt.value('blue'),
        tooltip=['Strike:O', 'Vanna Calls:Q']
    ).properties(
        width=600,
        height=400,
        title='Vanna Calls por Strike'
    ) + \
    alt.Chart(data).mark_bar().encode(
        x='Strike:O',  # Precio de Ejercicio en el eje x
        y=alt.Y('Vanna Puts:Q', title='Vanna Puts'),
        color=alt.value('red'),
        tooltip=['Strike:O', 'Vanna Puts:Q']
    ).properties(
        width=600,
        height=400,
        title='Vanna Puts por Strike'
    )

    # Título de la aplicación
    st.title('Vanna Calculator')

    # Visualizar el gráfico de barras de Vanna
    st.altair_chart(chart, use_container_width=True)
            
     

        
     
     
     
     

            
            
            
    #Calcular CHARM 0dte
    # Suponiendo que ya tienes el DataFrame 'data' con las columnas mencionadas

    # Asegúrate de que la columna 'Expiration Date' sea de tipo datetime
    data['Expiration Date'] = pd.to_datetime(data['Expiration Date'])

    # Calcular el Charm para cada Strike
    data['Charm'] = data['Calls Delta'] - data['Puts Delta']

    # Crear el gráfico de barras con Altair y ajustar el esquema de color
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Strike:N', title='Strike'),
        y=alt.Y('Charm:Q', title='Charm'),
        color=alt.Color('Charm:Q', scale=alt.Scale(scheme='blues', reverse=True), legend=None),
        tooltip=['Strike:N', 'Charm:Q']
    ).properties(
        width=800,
        height=600,
        title='Charm de Opciones 0DTE sobre SPX para diferentes Strikes'
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart, use_container_width=True)
        
    
    st.header("Todas las expiraciones SPX")

    col1, col2 = st.columns(2)

    with col1:
        # Suponiendo que tienes un DataFrame llamado 'data_all' con las columnas 'Strike', 'Calls Volume' y 'Puts Volume'
        # Crear una nueva columna 'Puts Volume' con valores negativos para representar las Puts Volume por debajo del 0
        data_all['Puts Volume'] = -data_all['Puts Volume']

        # Crear un gráfico de barras para mostrar las columnas de "Calls Volume" y "Puts Volume" para cada "Strike"
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts Volume'], name='Puts Volume'))
        fig2.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls Volume'], name='Calls Volume'))

        # Personaliza los títulos y ejes del gráfico
        fig2.update_layout(
            title='Volumen de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Volume',
            barmode='relative',  # Utiliza 'relative' para que las barras se apilen correctamente
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig2)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Open Interest" y "Puts Open Interest" para cada "Strike"
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=data_all['Calls Open Interest'], name='Calls Open Interest'))
        fig3.add_trace(go.Bar(x=df_top['Strike'], y=data_all['Puts Open Interest'], name='Puts Open Interest'))

        # Personaliza los títulos y ejes del gráfico
        fig3.update_layout(
            title='Interés abierto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Open Interest',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig3)

    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Net" y "Calls Net" para cada "Strike"
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts Net'], name='Puts Net'))
        fig4.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls Net'], name='Calls Net'))

        # Personaliza los títulos y ejes del gráfico
        fig4.update_layout(
            title='Neto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Puts Net',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig4)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Gamma" y "Calls Gamma" para cada "Strike"
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Puts IV'], name='Puts IV'))
        fig5.add_trace(go.Bar(x=data_all['Strike'], y=data_all['Calls IV'], name='Calls IV'))
                    
        # Personaliza los títulos y ejes del gráfico
        fig5.update_layout(
            title='Volatilidad implícita de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='IV Gamma',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig5)
                    
    
    
    


    
    
    
    
    
    

    #SESGO VOLATILIDA ALL EXPIRATIONS SPX
    # Código para el gráfico de sesgo de volatilidad con el eje X mejorado
    # Supongamos que tienes un DataFrame llamado "data" con las columnas necesarias

    # Calcular el sesgo de volatilidad (diferencia entre IV de calls y puts) en porcentaje
    data_all['Sesgo_IV'] = (data_all['Calls IV'] - data_all['Puts IV']) * 100  # Multiplicamos por 100 para convertirlo en porcentaje

    # Crear el gráfico de barras
    chart_sesgo_iv = alt.Chart(data_all).mark_bar().encode(
        x=alt.X('Strike:O', axis=alt.Axis(labelAngle=0), title='Precio de Ejercicio'),  # Rotar las etiquetas del eje X a 0 grados
        y=alt.Y('Sesgo_IV:Q', axis=alt.Axis(format='%'), title='Sesgo de Volatilidad (%)'),  # Formatear el eje Y como porcentaje
        color=alt.condition(alt.datum.Sesgo_IV >= 0, alt.value('orange'), alt.value('cyan')),
        tooltip=['Strike', 'Sesgo_IV']
    ).properties(
        title='Sesgo de Volatilidad (IV) de Calls y Puts por Precio de Ejercicio',
        width=800
    )

    # Mostrar el gráfico en Streamlit
    st.altair_chart(chart_sesgo_iv, use_container_width=True)
    
    


    #DELTA TODAS LAS EXPIRACIONES SPX
    # Transformar Expiration Date a formato fecha
    data_all['Expiration Date'] = pd.to_datetime(data_all['Expiration Date'], format='%a %b %d %Y')

    # Agregar una columna para el total de deltas en cada Expiration Date
    data_all['Total Delta'] = data_all['Calls Delta'] + data_all['Puts Delta']

    # Crear el gráfico con Plotly Express
    fig = px.bar(data_all, x='Expiration Date', y='Total Delta',
                color='Total Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Total Delta': 'Deltas'},
                title=f"Delta SPX")

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=data_all['Total Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(data_all['Expiration Date']), y0=0, x1=max(data_all['Expiration Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')



    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)









    # Crear el gráfico usando Altair con formato de fecha personalizado
    chart2 = alt.Chart(data_all).mark_line().encode(
        x=alt.X('Expiration Date:T', 
                axis=alt.Axis(title='Fecha de Vencimiento', labelAngle=45, format='%b %d, %Y')),  # Formato personalizado de fecha
        y='sum(Calls Open Interest):Q',
        color=alt.value('#9EF8EE')
    ) + alt.Chart(data_all).mark_line().encode(
        x=alt.X('Expiration Date:T', 
                axis=alt.Axis(title='Fecha de Vencimiento', labelAngle=45, format='%b %d, %Y')),  # Formato personalizado de fecha
        y='sum(Puts Open Interest):Q',
        color=alt.value('#F24405')
    )

    # Agregar etiquetas de texto personalizadas
    text = alt.Chart(data_all).mark_text(dx=-20, dy=-10, color='#9EF8EE').encode(
        x=alt.X('Expiration Date:T', 
                axis=alt.Axis(title='Fecha de Vencimiento', labelAngle=45, format='%b %d, %Y')),  # Formato personalizado de fecha
        y='sum(Calls Open Interest):Q',
        text='sum(Calls Open Interest):Q'
    ) + alt.Chart(data_all).mark_text(dx=20, dy=-10, color='#F24405').encode(
        x=alt.X('Expiration Date:T', 
                axis=alt.Axis(title='Fecha de Vencimiento', labelAngle=45, format='%b %d, %Y')),  # Formato personalizado de fecha
        y='sum(Puts Open Interest):Q',
        text='sum(Puts Open Interest):Q'
    )

    # Mostrar el gráfico y las etiquetas usando Altair
    st.altair_chart(chart2 + text, use_container_width=True)







    #probador GAMMA 0dte
    # Supongamos que tienes un DataFrame llamado 'data' con las columnas 'Calls Gamma' y 'Puts Gamma'
    # Calcula el Net Gamma restando 'Puts Gamma' de 'Calls Gamma'
    data['Net Gamma'] = data['Calls Gamma'] - data['Puts Gamma']

    # Crea un gráfico de barras para visualizar el Net Gamma por Strike
    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Strike:O', title='Strike', axis=alt.Axis(labelAngle=45)),  # Rotar las etiquetas del eje X
        y=alt.Y('Net Gamma:Q', title='Net Gamma ($)',
                axis=alt.Axis(format='~s')),  # Formatear los números en notación de ingeniería para números grandes
        color=alt.condition(
            alt.datum['Net Gamma'] >= 0,
            alt.value('#08A64D'),  # Color para Net Gamma positivo
            alt.value('#F22929')   # Color para Net Gamma negativo
        ),
        tooltip=['Strike:O', 'Net Gamma:Q']
    ).properties(
        width=800,
        height=400,
        title='Net Gamma del S&P 500 (SPX) por Strike'
    )

    # Mostrar el gráfico usando Streamlit
    st.write("Net Gamma del S&P 500 (SPX) por Strike")
    st.altair_chart(chart, use_container_width=True)

    # Supongamos que tienes un DataFrame llamado 'data_all' con las columnas 'Calls Gamma' y 'Puts Gamma'
    # Calcula el Net Gamma restando 'Puts Gamma' de 'Calls Gamma'
    data_all['Net Gamma'] = data_all['Calls Gamma'] - data_all['Puts Gamma']

    # Crea un gráfico de barras para visualizar el Net Gamma por Strike
    chart_all = alt.Chart(data_all).mark_bar().encode(
        x=alt.X('Strike:O', title='Strike', axis=alt.Axis(labelAngle=45)),  # Rotar las etiquetas del eje X
        y=alt.Y('Net Gamma:Q', title='Net Gamma ($)',
                axis=alt.Axis(format='~s')),  # Formatear los números en notación de ingeniería para números grandes
        color=alt.condition(
            alt.datum['Net Gamma'] >= 0,
            alt.value('#08A64D'),  # Color para Net Gamma positivo
            alt.value('#F22929')   # Color para Net Gamma negativo
        ),
        tooltip=['Strike:O', 'Net Gamma:Q']
    ).properties(
        width=800,
        height=400,
        title='Net Gamma del S&P 500 (SPX) por Strike'
    )

    # Mostrar el gráfico usando Streamlit
    st.write("Net Gamma del S&P 500 (SPX) por Strike")
    st.altair_chart(chart_all, use_container_width=True)


    
    
            
    #CURVA DE VANNA 0DTE
    # Elimina los valores duplicados en la columna de Strike
    data = data.drop_duplicates(subset='Strike')

    # Calcula el delta notional para cada opción
    data['Delta Notional Calls'] = data['Calls Delta'] * data['Calls Last Sale']
    data['Delta Notional Puts'] = data['Puts Delta'] * data['Puts Last Sale']

    # Suma los deltas notionales para obtener el delta notional agregado
    data['Delta Notional'] = data['Delta Notional Calls'] + data['Delta Notional Puts']

    # Ordena los datos por el valor del Strike
    data = data.sort_values(by='Strike')

    # Utiliza un spline cúbico para suavizar las curvas con un valor de k más alto (por ejemplo, 5)
    spline = make_interp_spline(data['Strike'], data['Delta Notional'], k=7)
    x_smooth = data['Strike'].values
    y_smooth_notional = spline(x_smooth)

    # Crea un DataFrame con los datos suavizados
    smoothed_data = pd.DataFrame({'Strike': x_smooth, 'Delta Notional': y_smooth_notional})

    # Crea un gráfico de línea para la curva suavizada
    chart = alt.Chart(smoothed_data).mark_line().encode(
        x='Strike:Q',
        y='Delta Notional:Q',
        color=alt.value('#D2E8E3'),
        tooltip=['Strike:Q', 'Delta Notional:Q']
    ).properties(
        width=800,
        height=400
    )

    # Muestra el gráfico en Streamlit
    st.write("Curva de Delta Notional suavizada del S&P 500 (SPX) por Strike")
    st.altair_chart(chart, use_container_width=True)

  
  
  
  
  
    # Supongamos que tienes un DataFrame llamado 'data' con las columnas proporcionadas

    # Calcula la suma de Calls Net y Puts Net
    total_calls_net = data['Calls Net'].sum()
    total_puts_net = data['Puts Net'].sum()

    # Crea un DataFrame para el gráfico
    total_data = pd.DataFrame({'Tipo': ['Total Calls Net', 'Total Puts Net'],
                            'Valor': [total_calls_net, total_puts_net]})

    # Crea un gráfico de barras con Altair
    chart = alt.Chart(total_data).mark_bar().encode(
        x='Tipo',
        y='Valor:Q',
        color=alt.Color('Tipo:N', legend=None),
        tooltip=['Tipo', 'Valor']
    ).properties(
        width=400,
        height=300,
        title='Total Calls Net y Total Puts Net'
    )

    # Muestra el gráfico en Streamlit
    st.write("Total Calls Net y Total Puts Net")
    st.altair_chart(chart, use_container_width=True)
  
  
  
  
  
  
  
  
  
  
    #TODAS LAS EXPIRACIONES VIX
    st.header("Todas las expiraciones VIX")

    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Volume" y "Puts Volume" para cada "Strike"
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Calls Volume'], name='Calls Volume'))
        fig2.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Puts Volume'], name='Puts Volume'))

        # Personaliza los títulos y ejes del gráfico
        fig2.update_layout(
            title='Volumen de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Volume',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig2)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Calls Open Interest" y "Puts Open Interest" para cada "Strike"
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Calls Open Interest'], name='Calls Open Interest'))
        fig3.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Puts Open Interest'], name='Puts Open Interest'))

        # Personaliza los títulos y ejes del gráfico
        fig3.update_layout(
            title='Interés abierto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Open Interest',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig3)

    col1, col2 = st.columns(2)

    with col1:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Net" y "Calls Net" para cada "Strike"
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Puts Net'], name='Puts Net'))
        fig4.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Calls Net'], name='Calls Net'))

        # Personaliza los títulos y ejes del gráfico
        fig4.update_layout(
            title='Neto de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='Puts Net',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig4)

    with col2:
        # Crear un gráfico de barras para mostrar las columnas de "Puts Gamma" y "Calls Gamma" para cada "Strike"
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Puts IV'], name='Puts IV'))
        fig5.add_trace(go.Bar(x=data_vix_all['Strike'], y=data_vix_all['Calls IV'], name='Calls IV'))
                    
        # Personaliza los títulos y ejes del gráfico
        fig5.update_layout(
            title='Volatilidad implícita de opciones call y put para todas las expiraciones',
            xaxis_title='Strike',
            yaxis_title='IV Gamma',
            barmode='stack'
        )

        # Muestra el gráfico en la página
        st.plotly_chart(fig5)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # Transformar Expiration Date a formato fecha
    data_vix_all['Expiration Date'] = pd.to_datetime(data_vix_all['Expiration Date'], format='%a %b %d %Y')

    # Agregar una columna para el total de deltas en cada Expiration Date
    data_vix_all['Total Delta'] = data_vix_all['Calls Delta'] + data_vix_all['Puts Delta']

    # Crear el gráfico con Plotly Express
    fig = px.bar(data_vix_all, x='Expiration Date', y='Total Delta',
                color='Total Delta',
                color_discrete_sequence=['red', 'green'],
                labels={'Total Delta': 'Deltas'},
                title=f"Delta VIX")

    # Definir los colores para valores positivos y negativos
    fig.update_traces(marker=dict(color=data_vix_all['Total Delta'].apply(lambda x: 'green' if x >= 0 else 'red')))

    # Añadir línea horizontal en y=0
    fig.add_shape(type='line', x0=min(data_vix_all['Expiration Date']), y0=0, x1=max(data_vix_all['Expiration Date']), y1=0,
                line=dict(color='black', width=1))

    # Configurar el tooltip para mostrar la fecha y el valor de delta
    fig.update_traces(hovertemplate='<b>%{x|%Y-%m-%d}</b><br>%{y:.0f} Deltas')



    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)





    ##########

    with tab5:
        
        st.subheader("Options Data. Índices más representativos: SPX, SPY, NDX")

        col1, col2 = st.columns(2)
        
        
        with col1:

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Net': df_index['Calls Net'],
                'Puts Net': df_index['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Título del gráfico
            titulo = "Neto de los principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig18 = go.Figure()
            fig18.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net', marker=dict(color='#FF6B6B')))
            fig18.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net', marker=dict(color='#6B66FF')))

            # Personalizar el diseño del gráfico
            fig18.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Neto',
                barmode='group',
                plot_bgcolor='black',  # Fondo negro
                paper_bgcolor='black',  # Fondo del gráfico negro
                font=dict(color='white')  # Color del texto blanco
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig18, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Volume': df_index['Calls Volume'],
                'Puts Volume': df_index['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de los principales Índices: SPX, SPY, NDX"
            # Crear un gráfico de barras
            fig19 = go.Figure()
            fig19.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
            fig19.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

            # Personalizar el diseño del gráfico
            fig19.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Volume',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig19, container_width=1000, container_height=500)






        col1, col2 = st.columns(2)
        
        
        with col1:

            #INDICES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Delta': df_index['Calls Delta'],
                'Puts Delta': df_index['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de los principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig10 = go.Figure()
            fig10.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig10.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig10.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig10, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Gamma': df_index['Calls Gamma'],
                'Puts Gamma': df_index['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de los principales índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig11 = go.Figure()
            fig11.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig11.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig11.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig11, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Last Sale': df_index['Calls Last Sale'],
                'Puts Last Sale': df_index['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)
            #df_chart.sort_values('Expiration Date', inplace=True)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las Principales Índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig12 = go.Figure()
            fig12.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig12.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig12.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig12, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_index['Expiration Date'],
                'Calls Open Interest': df_index['Calls Open Interest'],
                'Puts Open Interest': df_index['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de los principales índices: SPX, SPY, NDX"

            # Crear un gráfico de barras
            fig13 = go.Figure()
            fig13.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig13.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig13.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig13, container_width=1000, container_height=500)



    with tab6:
        

        
        col1, col2 = st.columns(2)
        with col1:

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Net': df_acciones['Calls Net'],
                'Puts Net': df_acciones['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Neto de Principales Acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Neto',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Volume': df_acciones['Calls Volume'],
                'Puts Volume': df_acciones['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Volume',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)






        col1, col2 = st.columns(2)
        with col1:

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Delta': df_acciones['Calls Delta'],
                'Puts Delta': df_acciones['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Gamma': df_acciones['Calls Gamma'],
                'Puts Gamma': df_acciones['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Last Sale': df_acciones['Calls Last Sale'],
                'Puts Last Sale': df_acciones['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones['Expiration Date'],
                'Calls Open Interest': df_acciones['Calls Open Interest'],
                'Puts Open Interest': df_acciones['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de las principales acciones: AMZN, AAPL, GOOG, MSFT, META, TSLA, NVDA, AMD"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)



        #Chart de tecnlogicas
        st.subheader("Acciones tecnológicas")
        col1, col2 = st.columns(2)
        
        
        with col1:

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Net': df_acciones_tech['Calls Net'],
                'Puts Net': df_acciones_tech['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Options Data. Neto de Principales Acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Neto',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Volume': df_acciones_tech['Calls Volume'],
                'Puts Volume': df_acciones_tech['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de las principales acciones:AAPL, GOOG, MSFT,NVDA"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Volume',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)


      
        
    

        col1, col2 = st.columns(2)
        with col1:

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Delta': df_acciones_tech['Calls Delta'],
                'Puts Delta': df_acciones_tech['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Gamma': df_acciones_tech['Calls Gamma'],
                'Puts Gamma': df_acciones_tech['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Last Sale': df_acciones_tech['Calls Last Sale'],
                'Puts Last Sale': df_acciones_tech['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de las principales acciones: AAPL, GOOG, MSFT,NVDA"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_acciones_tech['Expiration Date'],
                'Calls Open Interest': df_acciones_tech['Calls Open Interest'],
                'Puts Open Interest': df_acciones_tech['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de las principales acciones: AAPL, GOOG, MSFT, NVDA"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)
    



    with tab7:
        
        #Chart de Memes Stocks
        st.subheader("Options Data. Meme Stocks")
        col1, col2 = st.columns(2)
        
        
        with col1:

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Net', 'Puts Net']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Net': df_memestock['Calls Net'],
                'Puts Net': df_memestock['Puts Net']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            #df_chart = df_chart.sort_values('Calls Net', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Neto de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Net'], name='Calls Net'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Net'], name='Puts Net'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Neto',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Supongamos que el dataframe contiene las columnas ['Expiration Date', 'Calls Volume', 'Puts Volume']

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Volume': df_memestock['Calls Volume'],
                'Puts Volume': df_memestock['Puts Volume']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Volume', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Volumen de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Volume'], name='Calls Volume'))
            fig6.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Volume'], name='Puts Volume'))

            # Personalizar el diseño del gráfico
            fig6.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Volume',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig6, container_width=1000, container_height=500)






        col1, col2 = st.columns(2)
        with col1:

            #ACCIONES
            #DELTA

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Delta': df_memestock['Calls Delta'],
                'Puts Delta': df_memestock['Puts Delta']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Delta', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Delta de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig14 = go.Figure()
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Delta'], name='Calls Delta', marker=dict(color='green')))
            fig14.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Delta'], name='Puts Delta', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig14.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Delta',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig14, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Gamma

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Gamma': df_memestock['Calls Gamma'],
                'Puts Gamma': df_memestock['Puts Gamma']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Gamma', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Gamma de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig15 = go.Figure()
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Gamma'], name='Calls Gamma'))
            fig15.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Gamma'], name='Puts Gamma'))

            # Personalizar el diseño del gráfico
            fig15.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Gamma',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig15, container_width=1000, container_height=500)







        col1, col2 = st.columns(2)
            
            
        with col1:

            #INDICES
            #Last Sale Mayor actividad en las opciones de compra (calls): La barra más alta y el color verde indican que ha habido una mayor actividad en las opciones de compra en comparación con las opciones de venta. Esto podría sugerir que los inversores tienen un mayor interés en la compra de opciones de compra en este vencimiento en particular.
            #Posible expectativa alcista: La diferencia de altura entre las barras de Calls Last Sale y Puts Last Sale puede indicar una mayor preferencia de los inversores por las posiciones alcistas. La actividad en las opciones de compra podría reflejar una expectativa de que el precio del activo subyacente aumente antes del vencimiento.

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Last Sale': df_memestock['Calls Last Sale'],
                'Puts Last Sale': df_memestock['Puts Last Sale']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Last Sale', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Calls/Puts Last Sale de los Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig16 = go.Figure()
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Last Sale'], name='Calls Last Sale', marker=dict(color='green')))
            fig16.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Last Sale'], name='Puts Last Sale', marker=dict(color='red')))

            # Personalizar el diseño del gráfico
            fig16.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Last Sale',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig16, container_width=1000, container_height=500)

        with col2:
            

            # Obtener los datos del dataframe df_acciones
            # Open Interest

            # Crear un nuevo dataframe para los datos del gráfico
            df_chart = pd.DataFrame({
                'Expiration Date': df_memestock['Expiration Date'],
                'Calls Open Interest': df_memestock['Calls Open Interest'],
                'Puts Open Interest': df_memestock['Puts Open Interest']
            })

            # Establecer la columna 'Expiration Date' como índice
            df_chart.set_index('Expiration Date', inplace=True)

            # Ordenar el dataframe por Calls Net descendente
            df_chart = df_chart.sort_values('Calls Open Interest', ascending=False)

            # Limitar el número de acciones a mostrar en el gráfico
            #num_acciones_mostrar = 10
            #df_chart = df_chart.head(num_acciones_mostrar)

            # Título del gráfico
            titulo = "Open Interest de Principales Memes: LCID, AMC, PLTR, RIVN"

            # Crear un gráfico de barras
            fig17 = go.Figure()
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Calls Open Interest'], name='Calls Open Interest'))
            fig17.add_trace(go.Bar(x=df_chart.index, y=df_chart['Puts Open Interest'], name='Puts Open Interest'))

            # Personalizar el diseño del gráfico
            fig17.update_layout(
                title=titulo,
                xaxis_title='Expiration Date',
                yaxis_title='Open Interest',
                barmode='group'
            )

            # Mostrar el gráfico en la página web
            st.plotly_chart(fig17, container_width=1000, container_height=500)


    with tab8:

        st.subheader("Dark Index (DIX), Gamma Exposure (GEX)")

        # Convertir la columna 'date' en un objeto datetime
        df_squeeze['date'] = pd.to_datetime(df_squeeze['date'])

        # Seleccionar rango de fechas según el select 3 meses , 6 meses, 1 año, 1 año y medio, 2 años , 3 años, o todos los datos
        time_range = st.selectbox("Seleccionar rango de fechas", ["1 Semana" , "1 mes", "3 meses", "6 meses", "1 año", "1 año y medio", "2 años", "3 años",  "Todos los datos"])
        if time_range == "1 Semana":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(weeks=1)]
        elif time_range == "1 mes":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=1)]
        elif time_range == "3 meses":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=3)]
        elif time_range == "6 meses":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(months=6)]
        elif time_range == "1 año":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=1)]
        elif time_range == "1 año y medio":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=1)]
        elif time_range == "2 años":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=2)]
        elif time_range == "3 años":
            df_squeeze = df_squeeze[df_squeeze['date'] >= df_squeeze['date'].max() - pd.DateOffset(years=3)]
        elif time_range == "Todos los datos":
            df_squeeze = df_squeeze
            



        # Seleccionar todas las columnas numéricas excepto date
        numeric_cols = ['price', 'dix', 'gex']
        df_numeric = df_squeeze[numeric_cols]

        # Crear figura con 3 subplots
        fig = make_subplots(rows=3, cols=1, shared_xaxes=True)

        col1, col2 = st.columns(2)

        with col1:
            st.info('**Dark Index (DIX)**, es una medida ponderada en dólares del Dark Pool Indicator (DPI) de los componentes del S&P 500. Cuando el DIX es más alto, el sentimiento del mercado en los fondos oscuros es generalmente más alcista. Cuando el DIX es más bajo, es más bajista o incierto.', icon="ℹ️")

        with col2:
            st.info('**Gamma Exposure (GEX)**, es una medida denominada en dólares de las obligaciones de cobertura de los creadores de mercado de opciones. Cuando GEX es alto, el mercado de opciones implica que la volatilidad será baja. Cuando GEX es bajo, la volatilidad es alta y, aunque esperamos un mercado agitado, es poco probable que se produzcan más pérdidas.', icon="ℹ️")

        # Agregar cada gráfico de línea a la figura
        fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['price'], name='SP500'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['dix'], name='Dark Index'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df_squeeze['date'], y=df_squeeze['gex'], name='Gamma Exposure'), row=3, col=1)

        # Personalizar la figura
        fig.update_layout(
            height=800,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )


        # Mostrar la figura utilizando st.plotly_chart()
        st.plotly_chart(fig, use_container_width=True)
                    

    




    with tab9:

      


        # Crear una figura con dos ejes y
        fig = go.Figure()

        # Agregar las barras del posicionamiento comercial y no comercial
        fig.add_trace(go.Bar(
            x=df_cotSP['dia'],
            y=df_cotSP['cot_commercial'],
            name='Commercial',
            marker_color='#C2BB00'
        ))

        fig.add_trace(go.Bar(
            x=df_cotSP['dia'],
            y=df_cotSP['cot_noncommercial'],
            name='Non-Commercial',
            marker_color='#E1523D'
        ))

        # Configurar el primer eje y para el posicionamiento comercial y no comercial
        fig.update_layout(
            title='Posicionamiento Neto Commercial vs. Non-Commercial',
            xaxis_title='Periodo',
            yaxis_title='Posicionamiento',
            barmode='group',
            xaxis=dict(
                tickformat='%d-%m-%Y',  # Formato de las fechas
                tickmode='auto',
                nticks=10  # Número de ticks en el eje x
            ),
            yaxis=dict(
                side='left'  # Configurar el primer eje y en el lado izquierdo
            )
        )

        # Agregar la línea del precio de cierre en el segundo eje y
        fig.add_trace(go.Scatter(
            x=df_cotSP['dia'],
            y=df_diarios_ES['Closing Price'],
            name='Precio de Cierre',
            yaxis='y2'  # Asociar la línea al segundo eje y
        ))

        # Configurar el segundo eje y para el precio de cierre
        fig.update_layout(
            yaxis2=dict(
                side='right',  # Configurar el segundo eje y en el lado derecho
                overlaying='y',  # Superponer el segundo eje y al primero
                title='Precio de Cierre',
                rangemode='normal'  # Utilizar una escala lineal para el eje y2
            )
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

        
        
        
        
        st.info("En este gráfico se muestra la evolución de los cambios en la posición neta de diferentes participantes del mercado a lo largo del tiempo. Cada línea representa a un grupo de participantes y su respectivo cambio en la posición neta en relación con la fecha. El eje x muestra las fechas en las que se registraron los datos, mientras que el eje y representa el cambio en la posición neta para cada grupo de participantes.",  icon="ℹ️" )

        # Ordenar los datos por fecha
        df_cotSP["dia"] = pd.to_datetime(df_cotSP["dia"])  # Convertir columna "dia" a formato de fecha
        df_cotSP = df_cotSP.sort_values("dia")

        # Obtener la lista de participantes del mercado
        participantes = ['cot_commercial', 'cot_noncommercial', 'cot_dealer', 'cot_institutional', 'cot_leveragedfunds', 'cot_other']

        # Definir una paleta de colores personalizada
        colores = ['blue', 'green', 'orange', 'purple', 'red']

        # Crear el gráfico de líneas
        fig = go.Figure()

        for participante, color in zip(participantes, colores):
            fig.add_trace(go.Line(
                x=df_cotSP['dia'],
                y=df_cotSP[participante],
                name=participante,
                line=dict(color=color),
                hovertemplate='Fecha: %{x}<br>' +
                            'Participante: ' + participante + '<br>' +
                            'Cambio en Posición Neta: %{y}<br>'
            ))

        # Configurar el diseño del gráfico
        fig.update_layout(
            xaxis=dict(title='Fecha'),
            yaxis=dict(title='Cambio en Posición Neta'),
            title='Cambios en la Posición Neta de los Participantes del Mercado'
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)

        
        
        st.info("El gráfico de proporción de posiciones muestra la distribución de las posiciones largas y cortas de los diferentes participantes del mercado en forma de un gráfico de pastel o un gráfico de barras apiladas. Este tipo de gráfico nos ayuda a comprender la estructura general de las posiciones en el mercado y la relación entre las posiciones largas y cortas.",  icon="ℹ️")
        df_cotSP['Total_Position'] = df_cotSP['cot_commercial'] + df_cotSP['cot_noncommercial'] + df_cotSP['cot_dealer'] + df_cotSP['cot_institutional'] + df_cotSP['cot_leveragedfunds'] + df_cotSP['cot_other']
        df_cotSP['Commercial'] = df_cotSP['cot_commercial'] / df_cotSP['Total_Position']
        df_cotSP['NonCommercial'] = df_cotSP['cot_noncommercial'] / df_cotSP['Total_Position']
        df_cotSP['Dealer'] = df_cotSP['cot_dealer'] / df_cotSP['Total_Position']
        df_cotSP['Institutional'] = df_cotSP['cot_institutional'] / df_cotSP['Total_Position']
        df_cotSP['LeverageFunds'] = df_cotSP['cot_leveragedfunds'] / df_cotSP['Total_Position']
        df_cotSP['Other'] = df_cotSP['cot_other'] / df_cotSP['Total_Position']

        # Crear el gráfico de proporción de posiciones con Altair
        chart = alt.Chart(df_cotSP).mark_area(opacity=0.8).encode(
            x='dia:T',
            y=alt.Y('value:Q', stack='normalize'),
            color='variable:N'
        ).transform_fold(
            ['Commercial', 'NonCommercial', 'Dealer', 'Institutional', 'LeverageFunds', 'Other'],
            as_=['variable', 'value']
        ).properties(
            width=600,
            height=400,
            title='Proporción de Posiciones'
        )

        # Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

        # Crear el gráfico de proporción de posiciones con Plotly Express
        fig = px.area(df_cotSP, x='dia', y=['Commercial', 'NonCommercial', 'Dealer', 'Other'],
                    title='Proporción de Posiciones', labels={'value': 'Proporción', 'variable': 'Categoría'})

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)     
        
        
        
        
        
        
        # Información sobre el mapa de correlaciones
        st.info("El mapa de correlaciones en el CotReport representa las correlaciones entre las diferentes categorías de participantes en el mercado financiero. Cada celda del mapa muestra la correlación entre dos categorías específicas en una fecha determinada. Los valores de correlación varían entre -1 y 1, donde -1 indica una correlación negativa perfecta, 1 indica una correlación positiva perfecta y 0 indica ausencia de correlación. Este mapa proporciona una visualización visualmente intuitiva de las relaciones entre las categorías y cómo han cambiado a lo largo del tiempo. Al explorar el mapa de proporciones, se pueden identificar patrones y tendencias en la participación de los diferentes actores del mercado, lo que puede ser útil para tomar decisiones informadas en el ámbito financiero.",  icon="ℹ️")         # Calcular la proporción de posiciones
      
        # Calcular la matriz de correlaciones
        corr_matrix = df_cotSP[['cot_commercial', 'cot_noncommercial', 'cot_dealer', 'cot_institutional', 'cot_leveragedfunds', 'cot_other']].corr()

        # Crear el heatmap de correlaciones con Plotly
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='Viridis'
        ))

        fig.update_layout(
            title='Heatmap de Correlaciones',
            xaxis=dict(title='Variables'),
            yaxis=dict(title='Variables')
        )

        # Mostrar el heatmap en Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Crear el heatmap de correlaciones con Seaborn y Matplotlib
        plt.figure(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')

 
 


 
 
 
 
        st.info("Gráfico de Flujos o Cambios por Categoría es una herramienta visual que nos ayuda a entender los cambios en las posiciones de diferentes categorías de participantes del mercado, proporcionando información valiosa sobre la dirección y magnitud de los flujos de capital en cada categoría.",  icon="ℹ️")
        # Variables de interés
        variables = ['cot_commercial', 'cot_noncommercial', 'cot_dealer', 'cot_institutional', 'cot_leveragedfunds', 'cot_other']

        # Calcular los cambios por categoría
        df_changes = df_cotSP[variables].diff()

        # Crear la figura
        fig = go.Figure()

        # Agregar las líneas de cambio por categoría
        for variable in variables:
            fig.add_trace(go.Scatter(x=df_cotSP['dia'], y=df_changes[variable], mode='lines', name=variable))

        # Personalizar el diseño del gráfico
        fig.update_layout(
            title='Gráfico de flujo de posiciones por Categoría',
            xaxis=dict(title='Día'),
            yaxis=dict(title='Cambio'),
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)
 
 
 





        st.info("El gráfico de barras de comparación de influencias es una herramienta visual efectiva para determinar las variables más influyentes en un conjunto de datos y tomar decisiones informadas basadas en su magnitud relativa de influencia.", icon="ℹ️")

        # Crear un subconjunto del dataframe con las variables necesarias
        df_subset = df_cotSP[['cot_commercial', 'cot_noncommercial', 'cot_dealer', 'cot_institutional', 'cot_leveragedfunds', 'cot_other']]

        # Calcular la matriz de correlación entre las variables
        correlation_matrix = df_subset.corr().abs()

        # Calcular las magnitudes de influencia relativa
        total_absolute_influence = correlation_matrix.sum().sum()
        relative_influence = correlation_matrix.sum() / total_absolute_influence

        # Crear un dataframe con las variables y sus influencias relativas
        df_influences = pd.DataFrame({'Variable': relative_influence.index, 'Influencia Relativa': relative_influence.values})

        # Ordenar el dataframe por la columna de influencia relativa en orden descendente
        df_influences = df_influences.sort_values(by='Influencia Relativa', ascending=False)

        # Crear el gráfico de barras de comparación de influencias con Altair
        chart = alt.Chart(df_influences).mark_bar().encode(
            x=alt.X('Variable:N', sort=None),
            y=alt.Y('Influencia Relativa:Q', axis=alt.Axis(format='.0%')),  # Mostrar como porcentaje en el eje Y
            color=alt.Color('Variable:N', legend=None),
            tooltip=['Variable', alt.Tooltip('Influencia Relativa:Q', format='.2%')]
        ).properties(
            title='Comparación de Influencias Relativas'
        )

        # Mostrar el gráfico de barras de comparación de influencias con Altair y Streamlit
        st.altair_chart(chart, use_container_width=True)


 
 
                
    
    










    with tab11:
        
        #Gráfico de Líneas de Actividad Diaria:
        st.subheader("Actividad Diaria de Trading de Opciones")
        chart = alt.Chart(df_cboe).mark_line().encode(
            x='Day:T',
            y='Equity Option Contracts:Q',
            color='Market Participant:N',
            tooltip=['Day:T', 'Equity Option Contracts:Q']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(chart, use_container_width=True )


        #Gráfico de Barras para Mostrar la Cantidad de Contratos por Tipo:
        st.subheader("Cantidad Total de Contratos por Tipo de Opción")
        bar_chart = alt.Chart(df_cboe).mark_bar().encode(
            x='sum(Equity Option Contracts):Q',
            y='Market Participant:N',
            color='Market Participant:N',
            tooltip=['Market Participant:N', 'sum(Equity Option Contracts):Q']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(bar_chart, use_container_width=True)

        #Gráfico de Dispersion para Relacionar el Número de Contratos con el Número de Transacciones:
        st.subheader("Relación entre Número de Contratos y Número de Transacciones")
        scatter_chart = alt.Chart(df_cboe).mark_circle().encode(
            x='Equity Option Contracts:Q',
            y='Equity Option Trade Count:Q',
            color='Market Participant:N',
            tooltip=['Market Participant', 'Equity Option Contracts', 'Equity Option Trade Count']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(scatter_chart, use_container_width=True)


        #Gráfico de Barras Apiladas para Mostrar la Participación en el Mercado:
        st.subheader("Participación en el Mercado de Opciones")
        stacked_bar_chart = alt.Chart(df_cboe).mark_bar().encode(
            x='Day:T',
            y='Equity Option Contracts:Q',
            color='Market Participant:N',
            tooltip=['Day:T', 'Market Participant', 'Equity Option Contracts:Q']
        ).properties(
            width=600,
            height=400
        )
        st.altair_chart(stacked_bar_chart, use_container_width=True )






        # Ordenar los datos por volumen descendente
        df_cboe = df_cboe.sort_values('Total Option Notional', ascending=False)

        # Gráfico de barras para el volumen de mercado
        def volume_chart():
            chart = alt.Chart(df_cboe).mark_bar().encode(
                x='Market Participant',
                y='Total Option Notional',
                color=alt.Color('Total Option Notional', scale=alt.Scale(scheme='blues')),
                tooltip=['Market Participant', 'Total Option Notional']
            ).properties(
                width=600,
                height=400
            )
            return chart


        st.subheader('Volumen de Mercado')
        st.altair_chart(volume_chart(), use_container_width=True)




        # Ordenar los datos por el día
        df_cboe = df_cboe.sort_values('Day')

        # Gráfico de líneas para la evolución del volumen de contratos de opciones
        def volume_line_chart():
            chart = alt.Chart(df_cboe).mark_line().encode(
                x='Day',
                y='Total Option Contracts',
                color='Market Participant',
                tooltip=['Market Participant', 'Total Option Contracts']
            ).properties(
                width=600,
                height=400
            )
            return chart


        st.subheader('Evolución del Volumen de Contratos de Opciones')
        st.altair_chart(volume_line_chart(), use_container_width=True)




        # Gráfico de barras agrupadas para comparar el volumen de contratos por participante del mercado
        def volume_grouped_bar_chart():
            chart = alt.Chart(df_cboe).mark_bar().encode(
                x=alt.X('Market Participant', sort='-y'),
                y='Total Option Contracts',
                color=alt.Color('Total Option Contracts', scale=alt.Scale(scheme='blues')),
                tooltip=['Market Participant', 'Total Option Contracts']
            ).properties(
                width=600,
                height=400
            )
            return chart


        st.subheader('Volumen de Contratos de Opciones por Participante del Mercado')
        st.altair_chart(volume_grouped_bar_chart(), use_container_width=True)





        # Gráfico de dispersión para explorar la relación entre volumen de contratos y valor nominal
        def scatter_plot():
            chart = alt.Chart(df_cboe).mark_circle().encode(
                x='Total Option Notional',
                y='Total Option Contracts',
                color='Market Participant',
                size='Total Option Contracts',
                tooltip=['Market Participant', 'Total Option Notional', 'Total Option Contracts']
            ).properties(
                width=600,
                height=400
            )
            return chart



        st.subheader('Relación entre Volumen de Contratos y Valor Nominal de Opciones')
        st.altair_chart(scatter_plot(), use_container_width=True)



        # Ordenar los datos por el día
        df_cboe = df_cboe.sort_values('Day')


        st.subheader('Evolución del Volumen Total de Contratos de Opciones')
        st.area_chart(df_cboe['Total Option Contracts'], use_container_width=True)





        # Ordenar los datos por el día
        df_cboe = df_cboe.sort_values('Day')

        # Gráfico de líneas para mostrar la evolución del volumen total de contratos de opciones
        def line_chart():
            chart = alt.Chart(df_cboe).mark_bar().encode(
                x='Day:T',
                y='Total Option Contracts:Q'
            ).properties(
                width=800,
                height=400
            )
            return chart

        # Utilizar Streamlit para mostrar el gráfico de líneas
        st.subheader('Evolución del Volumen Total de Contratos de Opciones')
        st.altair_chart(line_chart(), use_container_width=True)







        # Gráfico de dispersión para mostrar la relación entre el número de transacciones y el volumen notional de contratos de opciones
        def scatter_chart():
            chart = alt.Chart(df_cboe).mark_circle().encode(
                x='Equity Option Trade Count:Q',
                y='Total Option Notional:Q',
                tooltip=['Day', 'Market Participant', 'Equity Option Trade Count', 'Total Option Notional']
            ).properties(
                width=800,
                height=400
            )
            return chart

        # Utilizar Streamlit para mostrar el gráfico de dispersión
        st.title('Análisis de Datos del Mercado CBOE Options Exchange')
        st.subheader('Relación entre el Número de Transacciones y el Volumen Notional de Contratos de Opciones')
        st.altair_chart(scatter_chart(), use_container_width=True)







############## ESTADISTICAS SOBRE TICKER DE OPCIONES DIARIAS ##############



        # Agrupar el volumen por símbolo
        df_grouped = df_options.groupby('Symbol').sum().reset_index()

        # Ordenar los símbolos por volumen de mayor a menor
        df_top_symbols = df_grouped.sort_values('Volume', ascending=False).head(25)

        # Crear el gráfico de barras agrupadas con los símbolos seleccionados
        chart = alt.Chart(df_top_symbols).mark_bar(size=30).encode(
            x=alt.X('Symbol:N', title='Símbolo'),
            y=alt.Y('Volume:Q', title='Volumen de Negociación'),
            color=alt.Color('Symbol:N', legend=None)
        ).properties(
            title='Volumen de Negociación - Top 25 Símbolos',
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16,
            anchor='middle'
        ).interactive()

        # Mostrar el gráfico de barras agrupadas con los símbolos seleccionados
        st.title('Gráfico de barras agrupadas de volumen - Top 25 Símbolos')
        st.altair_chart(chart, use_container_width=True)



        # Agrupar el volumen por tipo de opción y símbolo
        df_grouped = df_options.groupby(['Symbol', 'Call/Put']).sum().reset_index()

        # Seleccionar las 10 mayores acciones por volumen
        top_symbols = df_grouped.groupby('Symbol')['Volume'].sum().nlargest(30).index
        df_top_symbols = df_grouped[df_grouped['Symbol'].isin(top_symbols)]

        # Transformar los valores de volumen de las opciones Put a negativos
        df_top_symbols['Volume'] = df_top_symbols['Volume'].where(df_top_symbols['Call/Put'].str.contains('C', case=False), -df_top_symbols['Volume'])

        # Crear el gráfico de barras apiladas
        chart = alt.Chart(df_top_symbols).mark_bar().encode(
            x='Symbol',
            y=alt.Y('Volume:Q', axis=alt.Axis(title='Volumen'), scale=alt.Scale(domain=[-1000000, 1000000])),
            color=alt.condition(
                alt.datum['Call/Put'] == 'C',
                alt.value('#7EF2E7'),  # Color verde para opciones Call
                alt.value('#D95A11')  # Color rojo para opciones Put
            ),
            tooltip=['Symbol', 'Call/Put', 'Volume']
        ).properties(
            title='Volumen de Negociación por Tipo de Opción Call/Put',
            width=600,
            height=400
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        ).configure_title(
            fontSize=16,
            anchor='middle'
        ).interactive()



        # Mostrar el gráfico de barras apiladas
        st.title('Gráfico de Volumen Call/Put')
        st.altair_chart(chart, use_container_width=True)
                        





        
    
    with tab12:
        
        
        
        st.subheader("Options Data. Acciones más representativas del SP500")
        col1, col2 = st.columns(2)



        # Select para elegir el tipo de gráfico
        tipo_grafico = st.selectbox('Tipo de Gráfico', ['Barras', 'Líneas'], index=1)

        

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de inflación
            fig_inflacion = go.Figure()
            if tipo_grafico == "Barras":
                fig_inflacion.add_trace(go.Bar(
                    x=inflacion_df['Date'],
                    y=inflacion_df['Inflation'],
                    marker_color='blue'
                ))
            else:
                fig_inflacion.add_trace(go.Line(
                    x=inflacion_df['Date'],
                    y=inflacion_df['Inflation'],
                    marker_color='blue'
                ))
            fig_inflacion.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Inflación',
                title='Inflación'
            )
            st.plotly_chart(fig_inflacion, use_container_width=True)

        with col2:  
            # Gráfico de tipos de interés
            fig_tipos_interes = go.Figure()
            if tipo_grafico == "Barras":
                fig_tipos_interes.add_trace(go.Bar(
                    x=tipos_interes_df['Date'],
                    y=tipos_interes_df['Valor'],
                    marker_color='red'
                ))
            else:
                fig_tipos_interes.add_trace(go.Line(
                    x=tipos_interes_df['Date'],
                    y=tipos_interes_df['Valor'],
                    marker_color='red'
                ))
            fig_tipos_interes.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Tasa de Interés',
                title='Tasa de Interés'
            )
            st.plotly_chart(fig_tipos_interes, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de tasa de desempleo
            fig_empleo = go.Figure()
            if tipo_grafico == "Barras":
                fig_empleo.add_trace(go.Bar(
                    x=empleo_df['Date'],
                    y=empleo_df['Cant'],
                    marker_color='green'
                ))
            else:
                fig_empleo.add_trace(go.Line(
                    x=empleo_df['Date'],
                    y=empleo_df['Cant'],
                    marker_color='green'
                ))
            fig_empleo.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Tasa de Desempleo',
                title='Tasa de Desempleo'
            )
            st.plotly_chart(fig_empleo, use_container_width=True)

        with col2:
            # Gráfico de M2
            fig_m2 = go.Figure()
            if tipo_grafico == "Barras":
                fig_m2.add_trace(go.Bar(
                    x=m2_df['Date'],
                    y=m2_df['Dato'],
                    marker_color='purple'
                ))
            else:
                fig_m2.add_trace(go.Line(
                    x=m2_df['Date'],
                    y=m2_df['Dato'],
                    marker_color='purple'
                ))
            fig_m2.update_layout(
                xaxis_title='Fecha',
                yaxis_title='M2',
                title='M2'
            )
            st.plotly_chart(fig_m2, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Mercados Emergentes
            fig_dolares_emergentes = go.Figure()
            if tipo_grafico == "Barras":
                fig_dolares_emergentes.add_trace(go.Bar(
                    x=dolaresEmergentes_df['Date'],
                    y=dolaresEmergentes_df['Cant'],
                    marker_color='orange'
                ))
            else:
                fig_dolares_emergentes.add_trace(go.Line(
                    x=dolaresEmergentes_df['Date'],
                    y=dolaresEmergentes_df['Cant'],
                    marker_color='orange'
                ))
            fig_dolares_emergentes.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Mercados Emergentes',
                title='Mercados Emergentes vs Dollar EEUU'
            )
            st.plotly_chart(fig_dolares_emergentes, use_container_width=True)

        with col2:

            # Gráfico de inflación y tipos de interés

            # Fusionar los datos de inflación y tipos de interés en un solo DataFrame
            combined_df = pd.merge(inflacion_df, tipos_interes_df, on='Date')

            # Crear una figura de Plotly
            fig_combined = go.Figure()

            if tipo_grafico == "Barras":
                fig_combined.add_trace(go.Bar(
                    x=combined_df['Date'],
                    y=combined_df['Inflation'],
                    name='Inflación',
                    marker_color='blue'
                ))
                fig_combined.add_trace(go.Bar(
                    x=combined_df['Date'],
                    y=combined_df['Valor'],
                    name='Tasa de Interés',
                    marker_color='red'
                ))
            else:
                fig_combined.add_trace(go.Line(
                    x=combined_df['Date'],
                    y=combined_df['Inflation'],
                    name='Inflación',
                    marker_color='blue'
                ))
                fig_combined.add_trace(go.Line(
                    x=combined_df['Date'],
                    y=combined_df['Valor'],
                    name='Tasa de Interés',
                    marker_color='red'
                ))

            # Configurar el diseño del gráfico
            fig_combined.update_layout(
                xaxis_title='Fecha',
                yaxis_title='Valor',
                title='Inflación y Tipos de Interés'
            )

            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig_combined, use_container_width=True)




       

        # Fusionar los datos de desempleo y PIB en un solo DataFrame
        combined_df = pd.merge(empleo_df, gdp_df, on='Date')

        # Crear una figura de Plotly
        fig_combined = go.Figure()

        if tipo_grafico == "Barras":
            fig_combined.add_trace(go.Bar(
                x=combined_df['Date'],
                y=combined_df['Cant'],
                name='Desempleo',
                marker_color='orange'
            ))
            fig_combined.add_trace(go.Bar(
                x=combined_df['Date'],
                y=combined_df['gdp'],
                name='PIB',
                marker_color='cyan',
                yaxis='y2'  # Asignar la escala secundaria al eje y del PIB
            ))
        else:
            fig_combined.add_trace(go.Line(
                x=combined_df['Date'],
                y=combined_df['Cant'],
                name='Desempleo',
                marker_color='orange'
            ))
            fig_combined.add_trace(go.Line(
                x=combined_df['Date'],
                y=combined_df['gdp'],
                name='PIB',
                marker_color='cyan',
                yaxis='y2'  # Asignar la escala secundaria al eje y del PIB
            ))

        # Configurar el diseño del gráfico
        fig_combined.update_layout(
            xaxis_title='Fecha',
            title='Desempleo y PIB',
            yaxis=dict(
                title='Desempleo'
            ),
            yaxis2=dict(
                title='PIB',
                overlaying='y',  # Superponer la escala secundaria al eje y principal
                side='right'  # Posicionar la escala secundaria a la derecha
            )
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig_combined, use_container_width=True)



