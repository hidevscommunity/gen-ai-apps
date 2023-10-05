
# Core Libraries 
import pandas as pd
import numpy as np
# For Pattern
import re

# For Yahoo Data Sets
import yfinance as yf

# Streamlit Web
import streamlit as st
from streamlit_extras.colored_header import colored_header

#Graphs
import plotly.graph_objects as go

#AI
import openai
from langchain.callbacks import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langchain.agents import AgentType, initialize_agent

### Page Configure ###
st.set_page_config(page_title = "Financial Formulas LLM",
                    page_icon ='📊',
                    layout = 'wide')

st.header('Welcome to Financial Formulas with LLM!👨‍💻', divider='blue')

##################################################################################################
#                                   Historical Data                                              #
##################################################################################################
Ticker_list = st.container()

with st.sidebar:
    st.title('Company Ticker or Symbol 📥')
    with Ticker_list:
            ticker_list = st.sidebar.text_input('Write your Ticker (ex. AAPL,HPQ,AMZN)', value="AAPL")
            if ticker_list is not None:
                textsplit = ticker_list.replace(' ',',').replace('.',',').split(',')
    
    st.sidebar.info("If you change Ticker or Symbol, You have to wait a minute !!!")

name = textsplit[0]

if name != None:
        
        datainfo = yf.Ticker(f"{name}")

        info_keys = datainfo.info.keys()          # Company information

        Companyinfo= []

        for i in info_keys:
            v = datainfo.info.get(i)
            Companyinfo.append(v)
        Companyinfo = pd.DataFrame(Companyinfo, index = info_keys, columns=["Information"])
        Companyinfo.index.name = "Title"

        CompanyName = Companyinfo[Companyinfo.index == "longName"]
        CompanyName = CompanyName["Information"].values[0]
        Website = Companyinfo[Companyinfo.index == "website"]
        Website = Website["Information"].values[0]
        Country = Companyinfo[Companyinfo.index == "country"]
        Country = Country["Information"].values[0]
        Industry = Companyinfo[Companyinfo.index == "industry"]
        Industry = Industry["Information"].values[0]
        Sector = Companyinfo[Companyinfo.index == "sector"]
        Sector = Sector["Information"].values[0]
        FinancialCurrency = Companyinfo[Companyinfo.index == "financialCurrency"]
        FinancialCurrency = FinancialCurrency["Information"].values[0]
        SummaryOfInfo = pd.DataFrame({"Company Name":[CompanyName], "Website":[Website],"Country":[Country],
                                "Industry":[Industry],"Sector":[Sector],"Financial Currency":[FinancialCurrency]})
        
        SummaryOfInfo.style \
                            .relabel_index(["Info"], axis=0)
        
        longBusinessSummary = Companyinfo[Companyinfo.index == "longBusinessSummary"]
        longBusinessSummary = longBusinessSummary["Information"].values[0]
    

FirstFrame = st.empty()

Graph = st.container()

with FirstFrame.container():
     with Graph:
            
        colored_header(label = f"{CompanyName} Historical Prices",description= None ,color_name="blue-70")
        
        data = yf.download(textsplit)


        
        Graph_1,Graph_2,Dataframe = st.columns(3)
     
        SelectBox = st.selectbox(
            'How would you like to see Visulazation?',
            ('Line Graph', 'Candlestick Graph',"Data Table"))
        st.write('You selected:',SelectBox)
        
        with Graph_1:
            if SelectBox == "Line Graph":
                number = st.number_input('Insert Moving Average number', value= 50)

                data["MA100"] = data["Close"].rolling(100).mean()
                data["MA200"] = data["Close"].rolling(200).mean()
                data["MA"] = data["Close"].rolling(number).mean()

                MainModelGraph = go.Figure()
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["Open"], name = "Open Price",visible='legendonly'))
                MainModelGraph.add_trace(go.Line(x= data.index,  y = data["High"], name = "High Price",visible='legendonly'))
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["Low"], name = "Low Price",visible='legendonly'))
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["Close"],name ="Close Price"))
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["MA100"],name = f"MA 100",visible='legendonly'))
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["MA200"],name = f"MA 200",visible='legendonly'))
                MainModelGraph.add_trace(go.Line(x= data.index,  y= data["MA"],name = f"MA {number}",visible='legendonly'))
                
                MainModelGraph.update_xaxes(title_text = 'Date')
                MainModelGraph.update_yaxes(title_text = 'Price')
                MainModelGraph.update_layout(autosize=False, width = 1400, height = 500,title = f"{CompanyName} Historical Prices",legend_title_text='Parameters',
                                            legend = dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(count=1,
                     label="Current Year",
                     step="year",
                     stepmode="todate"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    ))
                Graph.plotly_chart(MainModelGraph)

                
            elif SelectBox == 'Candlestick Graph':
                with Graph_2:
                     
                    CandleStick = go.Figure(data=[go.Candlestick(x=data.index,
                                                     open=data["Open"],
                                                     high=data['High'],
                                                     low=data['Low'],
                                                     close=data['Close'])])
                    CandleStick.update_xaxes(title_text = 'Date')
                    CandleStick.update_yaxes(title_text = 'Price')
                    CandleStick.update_layout(autosize=False, width = 1400, height = 500,title = f"{CompanyName} Candlestick Graph",
                                              legend_title_text='Parameters',)
                    Graph.plotly_chart(CandleStick)
            
            else:
                with Dataframe:
                    Graph.dataframe(data,use_container_width=True)
        
        df_close = data[["Close"]].copy()
        df_close["CloseShift"] = df_close.shift()
        df_close["PriceRelative"] = df_close["Close"] / df_close["CloseShift"]
        df_close["Daily Return"] = np.log(df_close["PriceRelative"])
        df_close = df_close.reset_index()
        
        DailyVolatility = np.std(df_close['Daily Return'][1:])
        AnnualizedDailyVolatilityTradingDays = DailyVolatility*np.sqrt(252)
        AnnualizedDailyVolatilityCalendarDays = DailyVolatility*np.sqrt(365)

        weekly = pd.DataFrame(df_close.groupby([pd.Grouper(key="Date", freq="W")])["Close"].mean())
        weekly["CloseShift"] = weekly["Close"].shift()
        weekly["PriceRelative"] = weekly["Close"] / weekly["CloseShift"]
        weekly["Weekly Return"] = np.log(weekly["PriceRelative"])

        WeeklyVolatility = np.std(weekly['Weekly Return'][1:])
        AnnualizedWeeklyVolatilityTradingWeeks = WeeklyVolatility*np.sqrt(52)

        monthly = pd.DataFrame(df_close.groupby([pd.Grouper(key="Date", freq="M")])["Close"].mean())
        monthly["CloseShift"] = monthly["Close"].shift()
        monthly["PriceRelative"] = monthly["Close"] / monthly ["CloseShift"]
        monthly["Monthly Return"] = np.log(monthly ["PriceRelative"])

        MonthlyVolatility = np.std(monthly['Monthly Return'][1:])
        AnnualizedMonthlyVolatility = MonthlyVolatility*np.sqrt(12)

        annually = pd.DataFrame(df_close.groupby([pd.Grouper(key="Date", freq="Y")])["Close"].mean())
        annually = annually.dropna()
        annually["CloseShift"] = annually["Close"].shift()
        annually["PriceRelative"] = annually["Close"] / annually["CloseShift"]
        annually["Annually Return"] = np.log(annually["PriceRelative"])

        AnnualVolatility = np.std(annually['Annually Return'][1:])

        models = ['Annualized Daily Volatility by Trading Days','Annualized Daily Volatility by Calendar Days',
                'Annualized Weekly Volatility by Trading Weeks', 'Annualized Monthly Volatility',
                'Annual Volatility']
        volatilities = [AnnualizedDailyVolatilityTradingDays,AnnualizedDailyVolatilityCalendarDays,
                        AnnualizedWeeklyVolatilityTradingWeeks, AnnualizedMonthlyVolatility,
                        AnnualVolatility]
        new_volatilities = [f'{i*100:.2f}%' for i in volatilities]
        compare_models = pd.DataFrame({ "Estimators": models, "Estimates": new_volatilities})
        
        st.dataframe(compare_models,use_container_width=True)
             
##################################################################################################
#                                   Financial Statments                                          #
##################################################################################################

FinancialStatement = st.container()

with FinancialStatement:
    FinancialStatement.header(f"{CompanyName} Financial Statements and Formulas", divider="blue")

    FS_data = yf.Ticker(f"{name}")

    FS_radio = st.radio(
    "Please Choose of One Financial Statement",
    ["**Income Statement📑**", "**Balance Sheet📑**", "**Statement of Cashflow📑**"], horizontal=True)

    if name is not None:
        if FS_radio == "**Statement of Cashflow📑**":
            CF = pd.DataFrame(FS_data.cash_flow).iloc[::-1]
            st.dataframe(CF,use_container_width=True)
        
        elif FS_radio == "**Balance Sheet📑**":
            BS = pd.DataFrame(FS_data.balance_sheet).iloc[::-1]
            st.dataframe(BS,use_container_width=True)
        
        else: 
            IS = pd.DataFrame(FS_data.income_stmt).iloc[::-1]
            st.dataframe(IS,use_container_width=True)
    else:
        pass
    
    FinancialStatement.subheader('Important Formulas')
    Formula_info_keys = FS_data.info.keys()          # Company information

    Formula_Companyinfo= []

    for i in Formula_info_keys:
        v = FS_data.info.get(i)
        Formula_Companyinfo.append(v)
    Formula_Companyinfo = pd.DataFrame(Formula_Companyinfo, index = Formula_info_keys, columns=["Information"])
    Formula_Companyinfo.index.name = "Title"

    remove = ["address1","city","state","zip","country","phone","website","industry","industryDisp","sector",
          "sectorDisp","longBusinessSummary","fullTimeEmployees","companyOfficers","currency","symbol","underlyingSymbol",
          "shortName","longName","uuid","messageBoardId","financialCurrency"]
    
    Formula_Companyinfo_new = Formula_Companyinfo.drop(remove)
    Companyindex = Formula_Companyinfo_new.index.to_list()

    pattern = '[A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z]*|[A-Z]*[^A-Z][^A-Z][^A-Z][^A-Z]*'

    CompanyTitle = []

    for i in np.arange(0, len(Companyindex)):
        patternlist = Companyindex[i]
        findall = re.findall(pattern,patternlist)
        CompanyTitle.append(" ".join(findall).title())

    Formula_Companyinfo_new.index = CompanyTitle

    FinancialStatement.dataframe(Formula_Companyinfo_new,use_container_width=True)


##################################################################################################
#                                   Company Information                                          #
##################################################################################################

Info = st.container()

with Info:
    Info.header('About Company', divider='blue')
    
    
    st.table(SummaryOfInfo)
    st.markdown(f"**{longBusinessSummary}**")


##################################################################################################
#                                           AI                                                   #
##################################################################################################

ai = st.container()

with ai:
    
    ai.subheader('Ask a Question ?', divider="blue")

    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        "[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)"

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can learn more financial terms. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="What is the Beta Coefficient?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        try:
            llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
            search = DuckDuckGoSearchRun(name="Search")
            search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
        
        except openai.error.APIError as e:
            #Handle API error here, e.g. retry or log
            st.error(f"OpenAI API returned an API Error: {e}")
            pass
        except openai.error.APIConnectionError as e:
            #Handle connection error here
            st.error(f"Failed to connect to OpenAI API: {e}")
            pass
        except openai.error.RateLimitError as e:
            #Handle rate limit error (we recommend using exponential backoff)
            st.error(f"OpenAI API request exceeded rate limit: {e}")
            pass
    st.divider()
##################################################################################################
#                                      About Me                                                  #
##################################################################################################


Information = st.container()

with st.empty():
        with Information:
                html_info = '<h2 align="center"> INFORMATION </h2>'
                st.markdown(html_info,unsafe_allow_html=True)
                html_name = '<h2 align="center"> Designed By Batuhan YILDIRIM </h2>'
                st.markdown(html_name,unsafe_allow_html=True)
                html = ''' <h2 align="center"> I'm a Finance and Data Analyst 💻 </h2> '''
                st.markdown(html,unsafe_allow_html=True)
                col1,col2 = st.columns(2)
                with col1:
                    st.markdown("### 🤝 Connect with me:")
                    html_2 = '''<a href="https://www.linkedin.com/in/batuhannyildirim/"><img align="left" src="https://raw.githubusercontent.com/yushi1007/yushi1007/main/images/linkedin.svg" alt="Batuhan YILDIRIM | LinkedIn" width="21px"/></a>
            <a href="https://twitter.com/batuhan1148"><img align="left" src="https://camo.githubusercontent.com/ac6e1101f110e5f500287cf70dac72519687620deefb5e8de1fa7ba6a3ba2407/68747470733a2f2f6564656e742e6769746875622e696f2f537570657254696e7949636f6e732f696d616765732f706e672f747769747465722e706e67" alt="Batuhan YILDIRIM | Twitter" width="22px"/></a>
            <a href="https://medium.com/@BatuhanYildirim1148"><img align="left" src="https://raw.githubusercontent.com/yushi1007/yushi1007/main/images/medium.svg" alt="Batuhan YILDIRIM | Medium" width="21px"/></a><a href="https://github.com/Ybatuhan-EcoBooster"><img align="left" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white" alt="Batuhan YILDIRIM | GitHub"/>
            <a href="https://www.kaggle.com/ecobooster"><img align="left" src="https://img.shields.io/badge/Kaggle-035a7d?style=for-the-badge&logo=kaggle&logoColor=white" alt="Batuhan YILDIRIM | Kaggle" /></br>'''
                    st.markdown(html_2,unsafe_allow_html=True)
                    st.markdown("### 🤓 About Me:")
                    st.write('''I am a Finance and Accounting student at Akademia Ekonomiczno-Humanistyczna w Warszawie. I was a student of the Turkish Aetheraeronauticall Association University Industrial Engineering and Anadolu University Finance Department. I gained business and cultural experience by participating in the Work and Travel program, which is held every year from June 22 to September 28, 2019. In 2019-2020, I became the student representative of the IEEE Turkish Aeronautical Association University Student Society IAS (Industrial Applications Association). During my student representation, I conducted 3 different workshops and 2 projects. "Horizon Solar Rover", one of these projects, participated in the competition organized by Turkey's IEEE PES (Power and Energy Community) by leading a project team of 26 people, and we came second out of 20 teams. IEEE Turkey is preparing for the competition I started my job as Entrepreneur Network and continued to strengthen entrepreneurs. In 2020, I increased my business and cultural experience by participating in the work and travel program in America again. At the same time, I started secondary education by applying to Anadolu University's second university records. I love being involved in organizations, speaking in public, leading and working in a team, analyzing and solving problems, researching startups and being inspired by their stories, producing and marketing, and sharing. One of my biggest goals is to share my knowledge and experience with everyone and to be inspired by them. 
    Taking part in organizations, speaking in public, leading a team and working in a team, analyzing problems and producing solutions, researching startups and being inspired by their stories, producing and marketing them, and sharing the knowledge I have gained are among my favorite qualities. 
    One of my biggest goals is to tell everyone about the experiences I have had and to be inspired by them.''')
                with col2:
                    st.markdown("## 💼 Technical Skills")
                    st.markdown("### 📋 Languages")
                    html_3 = '''![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white)'''
                    st.markdown(html_3,unsafe_allow_html=True)
                    st.markdown("### 💻 IDEs/Editors")
                    html_4 = "![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)"
                    st.markdown(html_4, unsafe_allow_html=True)
                    st.markdown("### 🧭 ML/DL")
                    html_5 = "![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)"
                    st.markdown(html_5,unsafe_allow_html=True)