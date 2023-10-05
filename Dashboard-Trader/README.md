## Dashboard de Información Financiera
Este código en Python y Streamlit es un tablero de visualización de datos. Usa la biblioteca Streamlit para crear una interfaz web interactiva que permite a los usuarios visualizar y explorar los datos.

El tablero tiene dos pestañas, "Estadísticas" y "Gráficos/Forecast". En la primera pestaña, se puede seleccionar una fuente de datos de la lista de opciones disponibles en el menú lateral, y luego ver estadísticas generales, estadísticas por rango de fechas, y un mapa de correlaciones para esos datos.

En la segunda pestaña, se utiliza un modelo de regresión para hacer un pronóstico sobre el comportamiento de un activo financiero en el futuro. Además, se pueden ver gráficos interactivos para visualizar los datos y las tendencias.

En resumen, este código permite a los usuarios explorar y visualizar datos financieros de manera intuitiva y interactiva.

## Funcionalidades
1. Visualización de gráficos y datos actualizados en tiempo real sobre el mercado de derivados y los índices mencionados.
2. Posibilidad de realizar análisis y seguimiento de diferentes instrumentos financieros.
3. Interfaz intuitiva y fácil de usar.

## Requisitos
Tener instalado Python 3.x
Instalar las librerías requeridas presentes en el archivo requirements.txt

## Uso
Para ejecutar este proyecto, simplemente clone este repositorio a su equipo local y ejecute el siguiente comando en la terminal:
1. streamlit run main.py


## Contribuciones
Si deseas contribuir al proyecto, por favor envía una solicitud de pull. Para cualquier consulta o problema, abre un issue en este repositorio.

Data source:
    - tipos-interes.csv:https://fred.stlouisfed.org/series/FEDFUNDS
    - empleo.csv: https://fred.stlouisfed.org/series/UNRATE
    - m2.csv: https://fred.stlouisfed.org/series/WM2NS
    - dolares-emergentes.csv:https://fred.stlouisfed.org/series/RTWEXEMEGS
    - inflacion.csv:https://fred.stlouisfed.org/series/CORESTICKM159SFRBATL
    - GDP.csv:https://fred.stlouisfed.org/series/GDP

## Autor
Este proyecto ha sido desarrollado por José Mª Martin jmmartinnu@hotmail.com