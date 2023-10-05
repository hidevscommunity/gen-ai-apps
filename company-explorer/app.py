import streamlit as st

from custom_agent import get_company_information, get_company_income, get_final_answer
from llm_agent import get_company_name, get_ticker, is_income_statement_query, get_data_as_string, \
    run, extract_income_statement_data, is_balance_sheet_query, \
    get_income_statement_data, get_balance_sheet_data, extract_balance_sheet_data, is_cash_flow_query, \
    extract_cash_flow_data, get_cash_flow_data, get_earnings_data, extract_earnings_data, get_news
from prompt_helper import get_summary_prompt

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"


st.title("👲Company Explorer")
st.write("Company Explorer, is a versatile tool for in-depth research on publicly traded companies."
         " Whether you're seeking information or considering an investment, it offers features like company analysis, income statement and balance sheet access, and simplification of financial terminology."
         " This app aims to improve your understanding of the company you're interested in.")


def get_selected_ticker():
    session_tickers = st.session_state.tickers
    if session_tickers and len(session_tickers) > 1:
        values = []
        for key, val in session_tickers.items():
            values.append(key)
        selected_ticker = st.radio(
            "We found multiple companies with similar ticker symbol or name. Please change below 👇 options to use a different company.",
            options=values, format_func=lambda x: session_tickers[x] if x != '' else '',
            key="company_selected", captions=values)
        return selected_ticker, session_tickers[selected_ticker]
    else:
        return list(session_tickers.items())[0]


company_name = None
with st.form("my_form"):
    query = st.text_input("Enter your Query:", "Analyse the performance of Tesla this year")
    submitted = st.form_submit_button("Submit")
    openai_api_key = api_key = st.secrets["openai_api_key"]
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        st.empty()
        st.session_state.openai_api_key = openai_api_key
        company_name_resp = get_company_name(query, openai_api_key)
        print(company_name_resp)
        if 'tickers' in st.session_state:
            del st.session_state['tickers']
        if 'selected_ticker' in st.session_state:
            del st.session_state['selected_ticker']
        if 'company_name' in st.session_state:
            del st.session_state['company_name']
        if 'matched_token' in st.session_state:
            del st.session_state['matched_token']
        if company_name_resp and company_name_resp['company_present']:
            api_key = st.secrets["alpha_vantage_api_key"]
            matched_token = company_name_resp['name']
            tickers = get_ticker(matched_token, api_key)
            print(tickers)
            if not tickers:
                st.error("I'm sorry, I couldn't find any information for the above company")
                st.stop()
            st.session_state.tickers = tickers
            st.session_state.matched_token = matched_token
        if not company_name_resp or not company_name_resp['company_present']:
            if 'company_name' in st.session_state:
                company_name = st.session_state.company_name
            else:
                st.error("I'm sorry, I didn't quite understand your input."
                         " I can only help you with Company related queries.")
                st.stop()

if 'tickers' in st.session_state:
    ticker = get_selected_ticker()
    company_name = ticker[1]
    st.session_state.company_name = company_name

if 'tickers' in st.session_state and ticker:
    session_tickers = st.session_state.tickers
    selected_ticker = ticker[0]
    print(f'selected ticker: {selected_ticker}')
    st.session_state.selected_ticker = selected_ticker

    st.write(f"""
            #### :orange[{company_name}]
            
            """)

    # Company Overview
    with st.status("""###### Generating Company Information""", expanded=True) as status:
        company_info = get_company_information(f'Provide an Overview about {company_name}.', openai_api_key)
        st.write(company_info)
        status.update(label="""###### Company Overview""", state="complete", expanded=True)

    # Company Income
    income_statement_query = is_income_statement_query(query, openai_api_key)
    print(income_statement_query)
    if income_statement_query and income_statement_query.get('income_statement_useful'):
        with st.status("""###### Analyzing Income Statement...""", expanded=True) as status:
            if data := get_income_statement_data(
                    selected_ticker, income_statement_query.get('year')):

                st.markdown(''' ###### :blue[Annual Income Statement]

                ''')
                annual_data = data.get('annualReports')
                pivot_table = extract_income_statement_data(annual_data)
                st.dataframe(pivot_table, column_order=(
                    "GrossProfit", "TotalRevenue", "NetIncome", "OperatingIncome", "NetInterestIncome", "CostOfRevenue",
                    "InterestIncome", "InterestExpense", "IncomeBeforeTax", "InterestAndDebtExpense", "Ebit",
                    "Ebitda"), column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)

                st.markdown(''' ###### :blue[Quarterly Income Statement]

                ''')
                quarterly_data = data.get('quarterlyReports')
                pivot_table = extract_income_statement_data(quarterly_data)
                st.dataframe(pivot_table, column_order=(
                    "GrossProfit", "TotalRevenue", "OperatingIncome", "NetInterestIncome", "NetIncome", "CostOfRevenue",
                    "InterestIncome", "InterestExpense", "IncomeBeforeTax", "InterestAndDebtExpense", "Ebit",
                    "Ebitda"), column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)
                if data1 := get_earnings_data(
                        selected_ticker, income_statement_query.get('year')):
                    st.markdown(''' ###### :blue[Annual Earnings]

                            ''')
                    annual_data1 = data1.get('annualReports')
                    pivot_table = extract_earnings_data(annual_data1)
                    st.dataframe(pivot_table, column_config={
                        "Fiscal-Date": st.column_config.DateColumn(
                            "Date",
                            format="YYYY-MM-DD",
                        )
                    }, use_container_width=True)

                st.markdown(''' ###### :blue[Answer]

                        ''')
                status.update(label="""###### Generating Summary...""", expanded=True)
                annual_text_data = get_data_as_string(annual_data)
                quarterly_data_string = get_data_as_string(quarterly_data)
                income_prompt = get_summary_prompt(st.session_state.company_name, 'Interest Statement',
                                                   f"Annual Income Data = {annual_text_data} \n "
                                                   f"Quarterly Income Data = {quarterly_data_string}")
                resp1 = run(income_prompt, openai_api_key, False)
                st.markdown(f'''```{resp1}\n```''')
            else:
                company_income = get_company_income(f'Provide a summary like an expert business analyst for '
                                                    f'{st.session_state.company_name}. {query}',
                                                    openai_api_key)
                st.write(f'{company_income}')

            status.update(label="""###### Income Statement""", state="complete", expanded=True)

    # Balance Sheet
    balance_sheet_query = is_balance_sheet_query(query, openai_api_key)
    print(balance_sheet_query)
    if balance_sheet_query and balance_sheet_query.get('balance_sheet_useful'):
        with st.status("""###### Analyzing Balance Sheet...""", expanded=True) as status:
            if data := get_balance_sheet_data(
                    selected_ticker, balance_sheet_query.get('year')):

                st.markdown(''' ###### :blue[Annual Balance Sheet]

                ''')
                annual_data = data.get('annualReports')
                pivot_table = extract_balance_sheet_data(annual_data)
                st.dataframe(pivot_table, column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)

                st.markdown(''' ###### :blue[Quarterly Balance Sheet]

                ''')
                quarterly_data = data.get('quarterlyReports')
                pivot_table = extract_balance_sheet_data(quarterly_data)
                st.dataframe(pivot_table, column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)

                st.markdown(''' ###### :blue[Answer]

                        ''')
                status.update(label="""###### Generating Summary...""", expanded=True)
                annual_text_data = get_data_as_string(annual_data)
                balance_sheet_prompt = get_summary_prompt(st.session_state.company_name, 'Balance Sheet',
                                                          f"Balance Sheet : {annual_text_data}")
                resp1 = run(balance_sheet_prompt, openai_api_key, False)
                st.write(f'''```{resp1}\n```''')
            else:
                st.write(f"Sorry to inform you that currently we don't have enough information about "
                         f"the Balance Sheet of {company_name}")

            status.update(label="""###### Balance Sheet""", state="complete", expanded=True)

    # Cash Flow
    cash_flow_query = is_cash_flow_query(query, openai_api_key)
    print(cash_flow_query)
    if cash_flow_query and cash_flow_query.get('cash_flow_useful'):
        with st.status("""###### Analyzing Cash Flow...""", expanded=True) as status:
            if data := get_cash_flow_data(
                    selected_ticker, cash_flow_query.get('year')):

                st.markdown(''' ###### :blue[Annual Cash Flow]

                ''')
                annual_data = data.get('annualReports')
                pivot_table = extract_cash_flow_data(annual_data)
                st.dataframe(pivot_table, column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)
                st.markdown(''' ###### :blue[Quarterly Cash Flow]

                ''')
                quarterly_data = data.get('quarterlyReports')
                pivot_table = extract_cash_flow_data(quarterly_data)
                st.dataframe(pivot_table, column_config={
                    "Fiscal-Date": st.column_config.DateColumn(
                        "Date",
                        format="YYYY-MM-DD",
                    )
                }, use_container_width=True)

                st.markdown(''' ###### :blue[Answer]

                        ''')
                status.update(label="""###### Generating Summary...""", expanded=True)
                annual_text_data = get_data_as_string(annual_data)
                quarterly_data_string = get_data_as_string(quarterly_data)
                quarterly_prompt = get_summary_prompt(st.session_state.company_name, 'Cash Flow',
                                                      f"Annual Cash Flow : {annual_text_data} \n "
                                                      f"Quarterly Cash Flow : {quarterly_data_string}")
                resp1 = run(quarterly_prompt, openai_api_key, False)
                st.write(f'''```{resp1}\n```''')
            else:
                st.write(f"Sorry to inform you that currently we don't have enough information about "
                         f"the Cash Flow of {company_name}")

            status.update(label="""###### Cash Flow""", state="complete", expanded=True)

    if not income_statement_query and not income_statement_query.get('income_statement_useful') \
            and not balance_sheet_query and not balance_sheet_query.get('balance_sheet_useful') \
            and not cash_flow_query and not cash_flow_query.get('cash_flow_useful'):
        with st.status("""###### Analyzing Data...""", expanded=True) as status:
            final_resp = get_final_answer(openai_api_key, query)
            st.markdown(final_resp, unsafe_allow_html=True)
            status.update(label="""###### Response""", state="complete", expanded=True)

    api_key = st.secrets["alpha_vantage_api_key"]
    news = get_news(selected_ticker, api_key)
    if news and news.get('feed'):
        selected_news = []
        for curr_news in news.get('feed'):
            selected_comp_news = None
            for tick in curr_news.get('ticker_sentiment'):
                if tick.get('ticker') == selected_ticker:
                    selected_comp_news = True
            if selected_comp_news:
                selected_news.append(f"[{curr_news.get('title')}]({curr_news.get('url')})")
        if selected_news:
            st.markdown(''' ###### :orange[News]
            
                        ''')
            for curr_news in selected_news[:6]:
                st.markdown(f'{curr_news}\n', unsafe_allow_html=True)
