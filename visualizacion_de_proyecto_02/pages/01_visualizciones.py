import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np
import plotly.figure_factory as ff
import json
import re


doc5=pd.read_csv('dataset/doc 5.csv')


doc5['ADSL']= doc5['ADSL'].apply(lambda x: x.replace(".","")).astype(int)
doc5['Cablemodem']=doc5['Cablemodem'].apply(lambda x: x.replace(".","")).astype(int)
doc5['Fibra óptica']= doc5['Total'].apply(lambda x: x.replace(".","")).astype(int)
doc5['Total']= doc5['Total'].apply(lambda x: x.replace(".","")).astype(int)
doc5['Año']= doc5['Año'].astype('category')
doc5['Trimestre']= doc5['Trimestre'].astype('category')

st.markdown('## accesos a internet por tecnologia en un rango de tiempo')
if st.checkbox('mostrar data'):
    st.dataframe(doc5)

st.markdown('-------------------------------------------------------------------')


ani=st.slider('definir el año',2014,2022,2022)
st.markdown('diagrama de caja  para 5 tecnologias')
fig = plt.figure(1, figsize=(9, 6))
data_to_plot1=doc5[doc5['Año']==ani]  #,'ADSL','Cablemodem','Fibra óptica','Wireless','Otros'
#sns.boxplot(data=data_to_plot1, x="age", y=)
ax = fig.add_subplot(111)
bp = ax.boxplot(data_to_plot1[['ADSL','Cablemodem','Fibra óptica','Wireless','Otros']])
ax.set_xticklabels(['ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless','Otros'])
plt.grid()
st.pyplot(fig)

if ani<=1950631:
    st.dataframe(data_to_plot1[['Año','ADSL','Cablemodem','Fibra óptica','Wireless','Otros']])

# Add histogram data
#x1 = np.random.randn(200) - 2
#x2 = np.random.randn(200)
#x3 = np.random.randn(200) + 2

# Group data together
#hist_data = [x1, x2, x3]

#group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
#fig = ff.create_distplot(
#        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
#st.plotly_chart(fig, use_container_width=True)
d=doc5[['Año','Periodo','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].sort_values('Año',ascending=True)
#fig2=plt.figure(1, figsize=(10, 8))
st.markdown('-------------------------------------------------------------------')

st.markdown('Accesos a internet segun tipo de tecnologia')
# cramos opciones por año y periodo
eleccion= st.radio('***',('Año','trimestre por año'),horizontal=True)

if eleccion=='trimestre por año':
    
    fig1 = px.line(d, x='Periodo',title='el numero de acceso a internet por periodo segun tipo de tecnologia en Millones',markers = True)
    fig1.add_scatter(x=d['Periodo'], y=d['ADSL'],name='tec. ADSL')
    fig1.add_scatter(x=d['Periodo'], y=d['Cablemodem'],name='tec. Cablemodems')
    fig1.add_scatter(x=d['Periodo'], y=d['Fibra óptica'],name='tec. Fibra óptica')
    fig1.add_scatter(x=d['Periodo'], y=d['Wireless'],name='tec. Wirelesss')
    fig1.add_scatter(x=d['Periodo'], y=d['Otros'],name='otros')
    fig1.update_layout(width=8000, height=500)
    st.plotly_chart(fig1, use_container_width=True)

else :
    fig1 = px.line(doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index(), x='Año',title='el numero de acceso a internet por año segun tipo de tecnologia en Millones',markers = True)
    fig1.add_scatter(x=doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Año'], y=doc5[['Año','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['ADSL'],name='tec. ADSL')
    fig1.add_scatter(x=doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Año'], y=doc5[['Año','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Cablemodem'],name='tec. Cablemodems')
    fig1.add_scatter(x=doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Año'], y=doc5[['Año','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Fibra óptica'],name='tec. Fibra óptica')
    fig1.add_scatter(x=doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Año'], y=doc5[['Año','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Wireless'],name='tec. Wirelesss')
    fig1.add_scatter(x=doc5[['Año','ADSL','Cablemodem',	'Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Año'], y=doc5[['Año','ADSL','Cablemodem','Fibra óptica',	'Wireless',	'Otros']].groupby('Año').mean().reset_index()['Otros'],name='otros')
    fig1.update_layout(width=8000, height=500)
    st.plotly_chart(fig1, use_container_width=True)

# mostrar filas y columnas

st.markdown('-------------------------------------------------------------------')

st.markdown('Mapa Coropleth : Accesos a internet por Provincias')

doc1=pd.read_csv('dataset/doc 1.csv')

# convesrion tipo de dato en cada columna de doc1 
doc1['Accesos por cada 100 hogares']= doc1['Accesos por cada 100 hogares'].str.replace(",", ".").astype(float)
doc1['Trimestre']= doc1['Trimestre'].astype('category')
doc1['Año']= doc1['Año'].astype('category')
doc1['Provincia']= doc1['Provincia'].astype('category')

df=doc1.groupby('Provincia')['Accesos por cada 100 hogares'].agg([('promedio acessos por cada 100 hogares','mean')]).sort_values(by='promedio acessos por cada 100 hogares',ascending=False).reset_index()
df.Provincia=df.Provincia.replace({'Santiago Del Estero':'Santiago del Estero', 'Tierra Del Fuego': 'Tierra del Fuego','Capital Federal':'Capital Federal'})

lista_De_regiones= df['Provincia'].unique().tolist()   #['jujuy','la rioja','cordoba']
regiones=st.multiselect('***',lista_De_regiones,default=['Jujuy','Corrientes'])

df1=df[df['Provincia'].isin(regiones)]

with open('dataset/ProvinciasArgentina.geojson',encoding='utf-8') as f:
    data = json.load(f)

# realizamos el mapa choropleth el numero de acceso en promedio  en cada 100 hogares por provincia
import plotly.express as px
fig3 = px.choropleth_mapbox(df1, geojson=data,featureidkey='properties.nombre', locations='Provincia', color='promedio acessos por cada 100 hogares',
                           color_continuous_scale="Viridis",
                           range_color=(26, 114),
                           mapbox_style= "open-street-map",         #"carto-positron",   #, #       #"white-bg",
                           zoom=3, center = {"lat": -38.40, "lon": -63.60}, #latitud y longitud de Argentina
                           opacity=0.4,
                           labels={'promedio acessos por cada 100 hogares':'acceso a internet por 100 hogares'}
                          )
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
#fig3.show()
st.plotly_chart(fig3, use_container_width=True)


# other functions ----------------------------------------------------------------------

g=pd.read_csv('dataset/df111.csv')
st.markdown('-------------------------------------------------------------------')

st.markdown('### Promedio total de accesos a internet por velocidad de bajada entre los años 2017 a 2022 en Provincias')

lista_De_provincia= g['Provincia'].unique().tolist()   #['jujuy','la rioja','cordoba']
regio=st.multiselect('***',lista_De_provincia,default=['Catamarca','Capital Federal'])

df4=g[g['Provincia'].isin(regio)]

#

# evaluamos el promedio por provincia : en este caso elegimos las provincias 'Buenos Aires','Santiago Del Estero','Capital Federal'
fig6 = px.line(df4, x = "Año",
              y = "promedio total" ,
              color ='Provincia',markers = True)
#fig.show()
st.plotly_chart(fig6, use_container_width=True)

st.dataframe(g)
