import pandas as pd



df_diarios_ES = pd.read_csv("./Operativa/processed/Diarios-ES.csv")
df_diarios_ES['dia'] = pd.to_datetime(df_diarios_ES['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_ES['dia'] = df_diarios_ES['dia'].dt.date

df_diarios_NQ = pd.read_csv("./Operativa/processed/Diarios-NQ.csv")
df_diarios_NQ['dia'] = pd.to_datetime(df_diarios_NQ['dia'], format='%m/%d/%Y', errors = 'coerce')
df_diarios_NQ['dia'] = df_diarios_NQ['dia'].dt.date

df_semanal_ES = pd.read_csv("./Operativa/processed/Semanal-ES.csv")
df_semanal_ES['dia'] = pd.to_datetime(df_semanal_ES['dia'], errors = 'coerce')
df_semanal_ES['dia'] = df_semanal_ES['dia'].dt.date

df_semanal_NQ = pd.read_csv("./Operativa/processed/Semanal-NQ.csv")
df_semanal_NQ['dia'] = pd.to_datetime(df_semanal_NQ['dia'], errors = 'coerce')
df_semanal_NQ['dia'] = df_semanal_NQ['dia'].dt.date


df_vivienda = pd.read_csv("./Operativa/processed/indicadores_del_mercado_inmobiliario.csv", delimiter=";")

df_volatilidad = pd.read_csv("./Operativa/processed/spx_quotedata.csv", on_bad_lines='skip', delimiter=",")

df_volatilidad_vix = pd.read_csv("./Operativa/processed/vix_quotedata.csv", on_bad_lines='skip', delimiter=",")




df_dix = pd.read_csv("./Operativa/processed/DIX.csv", on_bad_lines='skip', delimiter=",")


#Squeeze metrics
# Cargar el archivo
df_squeeze = pd.read_csv("./Operativa/processed/DIX.csv")


#Acciones Gainers
df_gainers = pd.read_csv('./Operativa/processed/gainers.csv', sep=';')
#Acciones Losers
df_losers = pd.read_csv('./Operativa/processed/losers.csv' , sep=';')
#Acciones mas activas por volumen
df_activas = pd.read_csv('./Operativa/processed/mostActive.csv' , sep=';')


#Acciones DarkPools Shortsqueeze
df_shorteadas = pd.read_csv('./Operativa/processed/shorteadas.csv', sep=';')

#Datos sobre CBOE 
df_cboe = pd.read_csv('./Operativa/processed/volume-options.csv')
df_options = pd.read_csv('./Operativa/processed/options_symbols.csv')

#COT REPORT
df_cotNQ = pd.read_csv('./Operativa/processed/cotreport_NQ.csv')
df_cotSP = pd.read_csv('./Operativa/processed/cotreport_ES.csv')

#CBOE INDICES
data = pd.read_csv('./Operativa/processed/spx_quotedata.csv')
data_spy = pd.read_csv('./Operativa/processed/spy_quotedata.csv')
df_volatilidad_nq = pd.read_csv("./Operativa/processed/ndx_quotedata.csv", on_bad_lines='skip', delimiter=",")


#CBOE INDICES TODA EXPIRACION COMPLETA
data_all = pd.read_csv('./Operativa/processed/spx_quotedata_all.csv')
data_vix_all = pd.read_csv('./Operativa/processed/vix_quotedata_all.csv')

#CBOE Acciones
data_apple = pd.read_csv('./Operativa/processed/aapl_quotedata.csv')
data_goog = pd.read_csv('./Operativa/processed/goog_quotedata.csv')
data_meta = pd.read_csv('./Operativa/processed/meta_quotedata.csv')
data_msft = pd.read_csv('./Operativa/processed/msft_quotedata.csv')
data_amzn = pd.read_csv('./Operativa/processed/amzn_quotedata.csv')
data_nvda = pd.read_csv('./Operativa/processed/nvda_quotedata.csv')
data_amd = pd.read_csv('./Operativa/processed/amd_quotedata.csv')
df_tesla = pd.read_csv("./Operativa/processed/tsla_quotedata.csv", on_bad_lines='skip', delimiter=",")
df_cvna = pd.read_csv('./Operativa/processed/cvna_quotedata.csv')
#Acciones Esporadicas
data_otros = pd.read_csv('./Operativa/processed/ko_quotedata.csv')
df_ares =  pd.read_csv('./Operativa/processed/ares_quotedata.csv')
df_pypl = pd.read_csv('./Operativa/processed/pypl_quotedata.csv')
df_spce = pd.read_csv('./Operativa/processed/spce_quotedata.csv')
df_vale = pd.read_csv('./Operativa/processed/vale_quotedata.csv')
df_intc = pd.read_csv('./Operativa/processed/intc_quotedata.csv')
df_hyg = pd.read_csv('./Operativa/processed/hyg_quotedata.csv')

#Acciones Memes
df_lcid = pd.read_csv('./Operativa/processed/lcid_quotedata.csv')
df_amc = pd.read_csv('./Operativa/processed/amc_quotedata.csv')
df_sofi = pd.read_csv('./Operativa/processed/sofi_quotedata.csv')
df_pltr = pd.read_csv('./Operativa/processed/pltr_quotedata.csv')
df_rivn = pd.read_csv('./Operativa/processed/rivn_quotedata.csv')

#Union Acciones Memes
df_memestock = pd.concat([df_lcid, df_amc, df_sofi, df_pltr, df_rivn ], ignore_index=True)


#Union Acciones 
df_acciones = pd.concat([data_apple, data_goog, data_meta, data_msft, data_amzn, data_nvda, data_amd, df_tesla], ignore_index=True)

#Acciones tecnologicas puras
df_acciones_tech = pd.concat([data_apple, data_goog, data_msft, data_nvda], ignore_index=True)

#Union Indices
df_index = pd.concat([data, data_spy, df_volatilidad_nq], ignore_index=True)






#DIccionario de Acciones e Indices
data_files = {
    "spx_quotedata.csv": df_volatilidad,
    "ndx_quotedata.csv": df_volatilidad_nq,
    "aapl_quotedata.csv": data_apple,
    "goog_quotedata.csv": data_goog,
    "meta_quotedata.csv": data_meta,
    "msft_quotedata.csv": data_msft,
    "amzn_quotedata.csv": data_amzn,
    "vix_quotedata.csv": df_volatilidad_vix,
    "ko_quotedata.csv": data_otros,
    "spy_quotedata.csv": data_spy,
    "tsla_quotedata.csv": df_tesla,
    "nvda_quotedata.csv": data_nvda,
    "amd_quotedata.csv": data_amd,
    "lcid_quotedata.csv": df_lcid,
    "ares_quotedata.csv": df_ares,
    "amc_quotedata.csv": df_amc,
    "sofi_quotedata.csv": df_sofi,
    "pltr_quotedata.csv": df_pltr,
    "rivn_quotedata.csv": df_rivn,
    "pypl_quotedata.csv": df_pypl,
    "spx_all_quotedata.csv": data_all,
    "cvna_quotedate.csv": df_cvna,
    "spce_quotedata.csv": df_spce,
    "vale_quotedata.csv": df_vale,
    "intc_quotedata.csv": df_intc,
    "hyg_quotedata.csv": df_hyg,
    "vix_all_quotedata.csv": data_vix_all
}






#CotReport
data_cot = pd.read_csv('./Operativa/processed/cot-report.csv')
data_cot_noncommercial = pd.read_csv('./Operativa/processed/cot-report-noncommercial.csv')


#Open Interest
data_OI = pd.read_csv('./Operativa/processed/openinterest.csv')



inflacion_df = pd.read_csv('./Operativa/processed/inflacion.csv', names=['Date', 'Inflation'])
tipos_interes_df = pd.read_csv('./Operativa/processed/tipos-interes.csv', names=['Date', 'Valor'])
m2_df = pd.read_csv('./Operativa/processed/m2.csv', names=['Date', 'Dato'])
empleo_df = pd.read_csv('./Operativa/processed/empleo.csv', names=['Date', 'Tax'])
dolar_df = pd.read_csv('./Operativa/processed/dolar.csv', names=['Date', 'Price'])
dolaresEmergentes_df = pd.read_csv('./Operativa/processed/dolares-emergentes.csv', names=['Date', 'Cant'])
gdp_df = pd.read_csv('./Operativa/processed/GDP.csv', names=['Date', 'gdp'])


#elimino la fila 0
# Eliminar la fila 0 de inflacion_df
inflacion_df = inflacion_df.drop(0)

# Eliminar la fila 0 de tipos_interes_df
tipos_interes_df = tipos_interes_df.drop(0)

# Eliminar la fila 0 de m2_df
m2_df = m2_df.drop(0)

# Eliminar la fila 0 de empleo_df
empleo_df = empleo_df.drop(0)


# Eliminar la fila 0 de dolar_df
empleo_df = dolar_df.drop(0)

# Eliminar la fila 0 de dolaresEmergentes_df
empleo_df = dolaresEmergentes_df.drop(0)

#df_inflacion = pd.read_csv("./Operativa/inflacion.csv", on_bad_lines='skip', delimiter=",")

## Renombro algunas columnas 
def rename_columns(df):
    df = df.rename(columns={
        "high": "Day's High",
        "low": "Day's Low",
        "close": "Closing Price",
        "vol": "Volume",
        "range": "Range in ticks",
        "vix_close": "VIX Closing Price",
        "vwap": "Vwap",
        "vol_vpoc": "Volume in Vpoc Zone",
        "vol_val": "Volume Value Area Low",
        "vol_vah": "Volume Value Area High",
        "open": "Opening",
        "vpoc": "Vpoc",
        "dia": "Date",
        "vah": "Value Area High",
        "val": "Value Area Low",
        "poc_naked": "Naked Open Poc",
        "rango_area": "Range of Area in points",
        "delta": "Delta",
        "dia_semanal": "Weekday",
        "tendencia": "Trend",
        "cot_commercial": "Cot Commercial",
        "cot_noncommercial": "Cot Non Commercial",
        "cot_dealer": "Cot Dealer",
        "cot_institutional": "Cot Institutional",
        "cot_leveragedfunds": "Cot Leveraged Funds",
        "cot_other": "Cot Other"
        
    })
    return df

df_diarios_ES = rename_columns(df_diarios_ES)
df_diarios_NQ = rename_columns(df_diarios_NQ)
""" df_semanal_ES = rename_columns(df_semanal_ES)
df_semanal_NQ = rename_columns(df_semanal_NQ) """




renombre = {
    "./Operativa/processed/Diarios-ES.csv": "Mini S&P500 daily data",
    "./Operativa/processed/Diarios-NQ.csv": "Daily mini NASDAQ100 data"
}


