import streamlit as st
import yfinance as yf
from langchain.agents import AgentType
from datetime import datetime
import pandas as pd
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler
import plotly.graph_objs as go

def financials(stock_symbol):
    stock_data = yf.Ticker(stock_symbol)
    stock_df = stock_data.quarterly_financials
    return stock_df

def actions(stock_symbol):
    stock_data = yf.Ticker(stock_symbol)
    stock_df = stock_data.actions
    return stock_df

def cashflow(stock_symbol):
    stock_data = yf.Ticker(stock_symbol)
    stock_df = stock_data.quarterly_cashflow
    return stock_df

def create_candlestick_chart(data):
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])

    fig.update_layout(
        title='Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        template='plotly_dark'  # Dark theme
    )

    return fig

def create_volume_chart(data):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        marker=dict(color='blue'),
        opacity=0.6,
        name='Volume'
    ))

    fig.update_layout(
        title='Volume Chart',
        xaxis_title='Date',
        yaxis_title='Volume',
        template='plotly_dark'  # Dark theme
    )

    return fig



def create_line_chart(data):
        line_fig = go.Figure()
        line_fig = go.Figure(data=[go.Scatter(x=data.index, y=data['Close'], mode="lines")])

        line_fig.update_layout(
            title=f'Line Chart for Stock Price',
            xaxis_title='Date',
            yaxis_title='Price',
            template='plotly_dark'  
        )
        return line_fig


def main():
    OPENAI_API_BASE = st.secrets["OPENAI_API_BASE"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    # Clear the content of the current page
    st.experimental_set_query_params()
    
    st.sidebar.subheader("""Stock Search Web App""")
    selected_stock = "GOOGL"
    if selected_stock not in st.session_state:
         st.session_state[selected_stock] = "GOOGL"
    selected_stock = st.sidebar.text_input("Enter a valid stock ticker...", "GOOGL")
    st.session_state.selected_stock = selected_stock
    search_button = st.sidebar.button("Search")
    if search_button:
        stock_data = yf.Ticker(st.session_state.selected_stock)
        st.session_state.stock_data = stock_data.history(period='1d', start='2020-01-01', end=None)

    chatbot_key = "chatbot_checkbox"
    if chatbot_key not in st.session_state:
        st.session_state[chatbot_key] = False

    chatbot = st.sidebar.checkbox("Chat bot 🤖 ", key="chatbot_checkbox")
    

    chart_placeholder = st.empty()
    financials_placeholder = st.empty()
    actions_placeholder = st.empty()
    cashflow_placeholder = st.empty()

    if chatbot:
        Clear = st.button("Clear conversation history", key="clear_button_key")
        if "messages" not in st.session_state or Clear:
            st.session_state["messages"] = [{"role": "stock assistant", "content": "How can I help you analyze the stock prices?"}]
        
        # Display chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input(placeholder="What is this data about?", key='chat_input'):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            llm = OpenAI(
                temperature=0.1, openai_api_key=openai_api_key
            )

            stock_df = yf.Ticker(st.session_state.selected_stock)
            stock_df = stock_df.history(period='1d', start='2020-01-01', end=None)
            display_financials = financials(st.session_state.selected_stock)
            display_actions = actions(st.session_state.selected_stock)
            display_cashflow = cashflow(st.session_state.selected_stock)
            
            pandas_df_agent = create_pandas_dataframe_agent(
                llm,
                [stock_df, display_financials, display_actions, display_cashflow],
                verbose=True
            )

            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = pandas_df_agent.run(st.session_state.messages, callbacks=[st_cb])
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)
        
        if Clear:
            st.session_state.messages = [] 

        chart_placeholder.empty()
        financials_placeholder.empty()
        actions_placeholder.empty()
        cashflow_placeholder.empty()
    else:
        if "stock_data" in st.session_state:
            stock_data = st.session_state.stock_data
            ticker=st.session_state.selected_stock
            ticker = yf.Ticker(st.session_state.selected_stock)
            company_name = ticker.info['longName']
            st.title(company_name)
            stock_data_utc = stock_data.tz_localize(None)
            min_date = stock_data_utc.index.min().date()
            max_date = stock_data_utc.index.max().date()
            default_start_date = min_date + pd.DateOffset(days=1)  
            default_end_date = max_date

            start_date = st.sidebar.date_input("Select Start Date", min_value=min_date, max_value=max_date, value=default_start_date)
            end_date = st.sidebar.date_input("Select End Date", min_value=min_date, max_value=max_date, value=default_end_date)
            filtered_data = stock_data_utc.loc[start_date:end_date]
            today_price = filtered_data['Close'][-1]
            yesterday_price = filtered_data['Close'][-2]
            percentage_change_today = ((today_price - yesterday_price) / yesterday_price) * 100


            percentage_change_string = f"{percentage_change_today:.2f}%"
            if percentage_change_today < 0:
                percentage_change_string =   percentage_change_string

            max_price = filtered_data['Close'].max()
            min_price = filtered_data['Close'].min()
            date_of_max_price = filtered_data[filtered_data['Close'] == max_price].index[0]
            date_of_min_price = filtered_data[filtered_data['Close'] == min_price].index[0]

            # Create the widget
            col1, col2, col3 , col4= st.columns(4)
            col1.metric("Today's Price", f"${today_price:.2f}")
            col2.metric("Percentage Change", percentage_change_string)
            col3.metric("Max Price", f"${max_price:.2f}", f"Date: {date_of_max_price.date()}")
            col4.metric("Min Price", f"${min_price:.2f}", f"Date: {date_of_min_price.date()}")


            tab1, tab2 = st.tabs(["🗃 Data","📈 Chart"])
            with tab1:
                st.write(stock_data)
            with tab2:
                line_fig=create_line_chart(filtered_data)
                st.plotly_chart(line_fig)

            
            candlestick_fig = create_candlestick_chart(filtered_data)
            volume_fig = create_volume_chart(filtered_data)
            st.plotly_chart(candlestick_fig)
            st.plotly_chart(volume_fig)
    

            
            st.subheader("""Stock **actions** for """ + selected_stock)
            stock_data = yf.Ticker(st.session_state.selected_stock)
            display_actions = actions(st.session_state.selected_stock)
            if display_actions.empty == True:
                st.write("No data available at the moment")
            else:
                st.write(display_actions)

            st.subheader(f"**Quarterly financials** for {selected_stock}")
            

            display_financials = financials(st.session_state.selected_stock)
            
            if display_financials.empty:
                st.write("No data available at the moment")
            else:
                st.write(display_financials)

            st.subheader("""**Quarterly cashflow** for """ + selected_stock)
            stock_data = st.session_state.stock_data
            display_cashflow = cashflow(st.session_state.selected_stock)
            if display_cashflow.empty == True:
                st.write("No data available at the moment")
            else:
                st.write(display_cashflow)

if __name__ == "__main__":
    main()
