

""" with tab3:
    # Mostrar resumen operativo
    st.subheader('Resumen Operativo')

    # Función para leer y procesar archivos
    def read_and_process_file(file_type):
        if file_type == "resultados_operativa":
            try:
                df = pd.read_csv("./Operativa/resumen.csv", sep=',')
                df = df.fillna(0)
                df = df.drop(columns = ["Unnamed: 4"], axis = 1)
            except:
                st.error("No se puede leer el archivo de resultados operativos")
                return None
        elif file_type == "trades":
            try:
                df = pd.read_excel("./Operativa/trades-excel.xlsx", sheet_name="Sheet1")
                df = df.drop(columns = ["#"], axis = 1)
                new_columns = {
                    "Period": "Período",
                    "Instrument": "Instrumento",
                    "Side": "Lado",
                    "Quantity": "Cantidad",
                    "Price": "Precio",
                    "Commission": "Comisión",
                    "P&L": "Ganancias/Pérdidas",
                    "Cum. net profit": "Beneficio neto acumulado"
                }
                df = df.rename(columns=new_columns)
            except:
                st.error("No se puede leer el archivo de trades")
                return None
        elif file_type == "ordenes_ejecutadas":
            try:
                df = pd.read_csv("./Operativa/ordenes.csv", sep=',')
                df = df.drop(columns = ["Connection","Strategy","Unnamed: 18"], axis = 1)
            except:
                st.error("No se puede leer el archivo de órdenes ejecutadas")
                return None
        elif file_type == "ejecuciones":
            try:
                df = pd.read_csv("./Operativa/ejecuciones.csv", sep=',')
                df = df.drop(columns = ["Connection","Unnamed: 14","Commission"], axis = 1)
            except:
                st.error("No se puede leer el archivo de ejecuciones")
                return None
        else:
            st.error(f"Tipo de archivo inválido: {file_type}")
            return None
        return df

    
    # Leer y procesar archivo de resultados de operativa
    resultados_operativa = read_and_process_file("resultados_operativa")
    # Mostrar los resultados de operativa en un dataframe
    st.dataframe(resultados_operativa)

    # Leer y procesar archivo de trades
    trades = read_and_process_file("trades")
    # Mostrar los trades en un dataframe
    st.dataframe(trades)

    # Agregar un título a la sección de visualización de resultados
    st.subheader('Visualización de resultados')

    # Mostrar una lista desplegable para elegir el tipo de gráfico
    chart_type = st.selectbox("Elige el tipo de gráfico:", ["Línea", "Dispersión", "Barras"])

    # Definir la columna para el eje X como "Período"
    x_col = "Período"
    # Mostrar una lista desplegable para elegir la columna para el eje Y
    y_col = st.selectbox("Elige la columna para el eje Y:", [col for col in trades.columns if col != "Período"])

    # Verificar el tipo de gráfico seleccionado y crear el gráfico correspondiente
    if chart_type == "Línea":
        # Crear un gráfico de línea utilizando la librería altair
        line_chart = alt.Chart(trades).mark_line().encode(
            x=alt.X(x_col, type="nominal"),
            y=alt.Y(y_col, sort="descending")
        )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(line_chart.properties(width=800, height=600))

    elif chart_type == "Dispersión":
        # Crear un gráfico de dispersión utilizando la librería altair
        scatter_chart = alt.Chart(trades).mark_point().encode(
        x=alt.X(x_col, type="nominal"),
        y=alt.Y(y_col, sort="descending")
    )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(scatter_chart.properties(width=800, height=600))

    elif chart_type == "Barras":
        # Crear un gráfico de barras utilizando la librería altair
        bar_chart = alt.Chart(trades).mark_bar().encode(
        x=alt.X(x_col, type="nominal"),
        y=alt.Y(y_col, sort="descending")
    )
        # Mostrar el gráfico en la sección de visualización de resultados
        st.altair_chart(bar_chart.properties(width=800, height=600))


        ordenes_ejecutadas = read_and_process_file("ordenes_ejecutadas")

        ejecuciones = read_and_process_file("ejecuciones")


        

with tab4:
    # Función para descargar datos de cotización de un instrumento financiero específico
    def download_data(ticker, start_date, end_date):
        df = yf.download(ticker, start=start_date, end=end_date)
        info = yf.Ticker(ticker).info
        description = info.get("longBusinessSummary")
        df["Media móvil de 200 sesiones"] = df["Close"].rolling(window=200).mean()
        df["Close"].rolling(200).mean().plot(color='orange', label='Media móvil de 200 sesiones')
        df["Close"].plot(label='Precio de cierre')
        plt.legend()
       
        st.set_option('deprecation.showPyplotGlobalUse', False)

        return df, description

    # Interfaz de usuario de Streamlit
    with st.container():
        st.title("Buscador de Acciones")
        
        # Filtramos por fechas
        start_date = st.date_input("Ingrese la fecha de inicio:", dt.date(2020, 1, 1))
        end_date = st.date_input("Ingrese la fecha final:", dt.date.today())
        
        # Dinamicamente buscara el ticker.. Ojo! solo el ticker 
        ticker = st.text_input("Ingrese el ticker de la empresa:", "AAPL")



        if st.button("Mostrar datos"):    
            df,description = download_data(ticker, start_date, end_date)
            st.markdown("**Descripción de la empresa:** \n\n" + description)
            st.line_chart(df[["Close", "Media móvil de 200 sesiones"]])

            
with tab5:

    # Hacer una solicitud a la URL
    url = "https://finance.yahoo.com/gainers"
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Crear un objeto BeautifulSoup con el contenido de la página web
        soup = BeautifulSoup(response.content, "html.parser")

        # Buscar un elemento específico en la página web, por ejemplo, una tabla
        table = soup.find("table")

        # Procesar la información en la tabla y crear un DataFrame
        rows = []
        for row in table.find_all("tr"):
            cells = [cell.text for cell in row.find_all("td")]
            rows.append(cells)
        df = pd.DataFrame(rows, columns=["Symbol","Name", "Price(Intraday)", "Change","% Change","Volume","Avg Vol(3 month)","Market Cap","PE Ratio (TTM)", "52 Week Range"])
        # Eliminar la fila 0 del DataFrame
        df = df.drop(0)
        # Mostrar el DataFrame con Streamlit
        st.subheader("Acciones Ganadoras")
        st.table(df)
    else:
        st.write("Error al hacer la solicitud")






with tab6:
    st.subheader('Tab para critpoactivos')
    # Sección para Análisis de rendimiento
    if st.checkbox("Ver Análisis de rendimiento"):
        # Cargar los datos de rendimiento de las inversiones
        rendimiento = pd.read_csv("./Operativa/resumen.csv")
        
        # Mostrar el rendimiento histórico en un gráfico de línea
        st.line_chart(rendimiento)
        
        # Calcular el rendimiento actual y la rentabilidad proyectada
        rendimiento_actual = rendimiento["Rendimiento"].iloc[-1]
        rentabilidad_proyectada = rendimiento["Rendimiento"].mean()
        
        # Mostrar el rendimiento actual y la rentabilidad proyectada
        st.write("Rendimiento actual:", rendimiento_actual)
        st.write("Rentabilidad proyectada:", rentabilidad_proyectada)

    
    

with tab7:
    st.subheader("Tab para Defi")


 """