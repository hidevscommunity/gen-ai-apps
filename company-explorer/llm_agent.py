import json
from datetime import datetime

import numpy as np
import pandas as pd
import requests
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.tools import DuckDuckGoSearchRun

from prompt_helper import get_company_name_prompt, get_income_statement_prompt, get_balance_sheet_prompt, \
    get_cash_flow_prompt, get_earnings_prompt


def run(prompt: str, api_key: str, json_result=True, ):
    llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo-0613', openai_api_key=api_key, max_retries=2,
                     max_tokens=500)
    messages = [
        SystemMessage(
            content="You are an expert business analyst."
        ),
        HumanMessage(
            content=prompt
        ),
    ]
    try:
        response = llm(messages)
    except Exception as e:
        print(e)
        return json.loads("")
    return json.loads(response.content) if json_result else response.content


def run_with_search(prompt, api_key):
    messages = [
        SystemMessage(
            content="You are an expert business analyst."
        ),
        HumanMessage(
            content=prompt
        ),
    ]
    try:
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613", openai_api_key=api_key, streaming=True,
                         max_retries=2, max_tokens=1000)
        search = DuckDuckGoSearchRun(name="Search")
        search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                        handle_parsing_errors=True)
        response = search_agent.run(messages)
        return response
    except Exception as e:
        print(f'Exception occurred {e}')
        return "Sorry, couldn't process the request now. Try again after sometime"


def get_company_name(user_query, api_key):
    company_name_prompt = get_company_name_prompt(user_query)
    return run(company_name_prompt, api_key)


def get_ticker(company_name, api_key):
    url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={company_name}&apikey={api_key}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    r = requests.get(url, headers=headers)
    data = r.json()
    distinct_comp_name = set()
    ticker_comp_name_dict = {}
    if matches := data.get('bestMatches'):
        for match in matches:
            if match['2. name'] not in distinct_comp_name:
                distinct_comp_name.add(match['2. name'])
                ticker_comp_name_dict[match['1. symbol']] = match['2. name']
        return ticker_comp_name_dict


def get_news(ticker, api_key):
    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&apikey={api_key}&limit=10&sort=RELEVANCE'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        return data
    except Exception as e:
        print(f'Exception occurred {e}')


def get_income_statement(ticker):
    print(f'Inside get_income_statement {ticker}')
    import streamlit as st
    if ticker:
        comp_ticker = ticker
    else:
        comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        return r.json()
    return None


def get_balance_sheet(ticker):
    import streamlit as st
    if ticker:
        comp_ticker = ticker
    else:
        comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        return r.json()
    return None


def get_cash_flow(ticker):
    import streamlit as st
    if ticker:
        comp_ticker = ticker
    else:
        comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        return r.json()
    return None


def get_earnings(ticker):
    import streamlit as st
    if ticker:
        comp_ticker = ticker
    else:
        comp_ticker = st.session_state.selected_ticker
    print(f'{comp_ticker}')
    if comp_ticker:
        api_key = st.secrets["alpha_vantage_api_key"]
        url = f'https://www.alphavantage.co/query?function=EARNINGS&symbol={comp_ticker}&apikey={api_key}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        return r.json()
    return None


def is_income_statement_query(user_query, api_key):
    income_statement_prompt = get_income_statement_prompt(user_query)
    return run(income_statement_prompt, api_key)


def is_balance_sheet_query(user_query, api_key):
    balance_sheet_prompt = get_balance_sheet_prompt(user_query)
    return run(balance_sheet_prompt, api_key)


def is_cash_flow_query(user_query, api_key):
    cash_flow_prompt = get_cash_flow_prompt(user_query)
    return run(cash_flow_prompt, api_key)


def is_earnings_query(user_query, api_key):
    earnings_prompt = get_earnings_prompt(user_query)
    return run(earnings_prompt, api_key)


def get_income_statement_data(ticker, year):
    print(f'{ticker} {year}')
    income_statement = get_income_statement(ticker)
    currentYear = datetime.now().year
    data = {}
    annual_report = []
    quarterly_report = []
    if income_statement:
        for annual_rep in income_statement.get('annualReports'):
            if year and year != 'None':
                if str(year) in annual_rep.get('fiscalDateEnding') or str(year - 1) in annual_rep.get(
                        'fiscalDateEnding'):
                    annual_report.append({key: value for key, value in annual_rep.items()})
            else:
                annual_report.append({key: value for key, value in annual_rep.items()})
        for quarterly_rep in income_statement.get('quarterlyReports'):
            if year and year != 'None':
                if str(year) in quarterly_rep.get('fiscalDateEnding') or str(year - 1) in quarterly_rep.get(
                        'fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})
            else:
                if str(currentYear) in quarterly_rep.get('fiscalDateEnding') or str(
                        currentYear - 1) in quarterly_rep.get('fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})

        data['annualReports'] = annual_report
        data['quarterlyReports'] = quarterly_report

    return data


def get_balance_sheet_data(ticker, year):
    print(f'{ticker} {year}')
    balance_sheet = get_balance_sheet(ticker)
    currentYear = datetime.now().year
    data = {}
    annual_report = []
    quarterly_report = []
    if balance_sheet:
        for annual_rep in balance_sheet.get('annualReports'):
            print('Got Balance sheet data ')
            if year and year != 'None':
                if str(year) in annual_rep.get('fiscalDateEnding') or str(year - 1) in annual_rep.get(
                        'fiscalDateEnding'):
                    annual_report.append({key: value for key, value in annual_rep.items()})
            else:
                annual_report.append({key: value for key, value in annual_rep.items()})
        for quarterly_rep in balance_sheet.get('quarterlyReports'):
            if year and year != 'None':
                if str(year) in quarterly_rep.get('fiscalDateEnding') or str(year - 1) in quarterly_rep.get(
                        'fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})
            else:
                if str(currentYear) in quarterly_rep.get('fiscalDateEnding') or str(
                        currentYear - 1) in quarterly_rep.get('fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})

        data['annualReports'] = annual_report
        data['quarterlyReports'] = quarterly_report

    return data


def get_cash_flow_data(ticker, year):
    print(f'{ticker} {year}')
    cash_flow = get_cash_flow(ticker)
    # print(cash_flow)
    currentYear = datetime.now().year
    data = {}
    annual_report = []
    quarterly_report = []
    if cash_flow:
        for annual_rep in cash_flow.get('annualReports'):
            if year and year != 'None':
                if str(year) in annual_rep.get('fiscalDateEnding') or str(year - 1) in annual_rep.get(
                        'fiscalDateEnding'):
                    annual_report.append({key: value for key, value in annual_rep.items()})
            else:
                annual_report.append({key: value for key, value in annual_rep.items()})
        for quarterly_rep in cash_flow.get('quarterlyReports'):
            if year and year != 'None':
                if str(year) in quarterly_rep.get('fiscalDateEnding') or str(year - 1) in quarterly_rep.get(
                        'fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})
            else:
                if str(currentYear) in quarterly_rep.get('fiscalDateEnding') or str(
                        currentYear - 1) in quarterly_rep.get('fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})

        data['annualReports'] = annual_report
        data['quarterlyReports'] = quarterly_report

    return data


def get_earnings_data(ticker, year):
    print(f'{ticker} {year}')
    earnings = get_earnings(ticker)
    currentYear = datetime.now().year
    data = {}
    annual_report = []
    quarterly_report = []
    if earnings:
        for annual_rep in earnings.get('annualEarnings'):
            if year and year != 'None':
                if str(year) in annual_rep.get('fiscalDateEnding') or str(year - 1) in annual_rep.get(
                        'fiscalDateEnding'):
                    annual_report.append({key: value for key, value in annual_rep.items()})
            else:
                if str(currentYear) in annual_rep.get('fiscalDateEnding') or str(
                        currentYear - 1) in annual_rep.get('fiscalDateEnding') or str(
                    currentYear - 2) in annual_rep.get('fiscalDateEnding'):
                    annual_report.append({key: value for key, value in annual_rep.items()})
        for quarterly_rep in earnings.get('quarterlyEarnings'):
            if year and year != 'None':
                if str(year) in quarterly_rep.get('fiscalDateEnding') or str(year - 1) in quarterly_rep.get(
                        'fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})
            else:
                if str(currentYear) in quarterly_rep.get('fiscalDateEnding') or str(
                        currentYear - 1) in quarterly_rep.get('fiscalDateEnding'):
                    quarterly_report.append({key: value for key, value in quarterly_rep.items()})

        data['annualReports'] = annual_report
        data['quarterlyReports'] = quarterly_report

    return data


def get_data_as_string(data):
    temp_data = []
    for map in data:
        for key, value in map.items():
            data_str = f'{key} : {value}'
            temp_data.append(data_str)

    return ', '.join(temp_data)


def extract_income_statement_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'grossProfit': 'GrossProfit', 'totalRevenue': 'TotalRevenue',
                       'costOfRevenue': 'CostOfRevenue',
                       'costofGoodsAndServicesSold': 'CostofGoodsAndServicesSold',
                       'operatingIncome': 'OperatingIncome',
                       'sellingGeneralAndAdministrative': 'SellingGeneralAndAdministrative',
                       'researchAndDevelopment': 'ResearchAndDevelopment',
                       'operatingExpenses': 'OperatingExpenses',
                       'investmentIncomeNet': 'InvestmentIncomeNet',
                       'netInterestIncome': 'NetInterestIncome',
                       'interestIncome': 'InterestIncome',
                       'interestExpense': 'InterestExpense',
                       'nonInterestIncome': 'NonInterestIncome',
                       'otherNonOperatingIncome': 'OtherNonOperatingIncome',
                       'depreciation': 'Depreciation',
                       'depreciationAndAmortization': 'DepreciationAndAmortization',
                       'incomeBeforeTax': 'IncomeBeforeTax',
                       'incomeTaxExpense': 'IncomeTaxExpense',
                       'interestAndDebtExpense': 'InterestAndDebtExpense',
                       'netIncomeFromContinuingOperations': 'NetIncomeFromContinuingOperations',
                       'comprehensiveIncomeNetOfTax': 'ComprehensiveIncomeNetOfTax',
                       'ebit': 'Ebit',
                       'ebitda': 'Ebitda', 'netIncome': 'NetIncome', }, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)


def extract_balance_sheet_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'totalAssets': 'TotalAssets', 'totalCurrentAssets': 'TotalCurrentAssets',
                       'inventory': 'Inventory',
                       'currentNetReceivables': 'CurrentNetReceivables',
                       'totalLiabilities': 'TotalLiabilities',
                       'totalCurrentLiabilities': 'TotalCurrentLiabilities',
                       'currentAccountsPayable': 'CurrentAccountsPayable',
                       'currentDebt': 'CurrentDebt',
                       'shortTermDebt': 'ShortTermDebt',
                       'longTermDebt': 'LongTermDebt',
                       'totalShareholderEquity': 'TotalShareholderEquity',
                       'shortLongTermDebtTotal': 'ShortLongTermDebtTotal',
                       'commonStockSharesOutstanding': 'CommonStockSharesOutstanding'}, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)


def extract_cash_flow_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.astype({'reportedCurrency': 'str'})
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedCurrency': 'Currency',
                       'operatingCashflow': 'OperatingCashflow', 'netIncome': 'NetIncome',
                       'profitLoss': 'ProfitLoss',
                       'paymentsForOperatingActivities': 'PaymentsForOperatingActivities',
                       'proceedsFromOperatingActivities': 'ProceedsFromOperatingActivities',
                       'changeInOperatingLiabilities': 'ChangeInOperatingLiabilities',
                       'changeInOperatingAssets': 'ChangeInOperatingAssets',
                       'depreciationDepletionAndAmortization': 'DepreciationDepletionAndAmortization',
                       'capitalExpenditures': 'CapitalExpenditures',
                       'changeInReceivables': 'ChangeInReceivables',
                       'changeInInventory': 'ChangeInInventory',
                       'cashflowFromInvestment': 'CashflowFromInvestment',
                       'cashflowFromFinancing': 'CashflowFromFinancing',
                       'dividendPayout': 'DividendPayout',
                       'dividendPayoutCommonStock': 'DividendPayoutCommonStock',
                       'dividendPayoutPreferredStock': 'DividendPayoutPreferredStock', }, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Currency', 'Fiscal-Date'], sort=False)


def extract_earnings_data(data):
    df = pd.DataFrame.from_records(data)
    df = df.apply(pd.to_numeric, errors='ignore')
    df["fiscalDateEnding"] = pd.to_datetime(df["fiscalDateEnding"], format="%Y-%m-%d")
    df.rename(columns={'fiscalDateEnding': 'Fiscal-Date', 'reportedEPS': 'EPS'}, inplace=True)
    df = df.replace(to_replace='None', value=np.nan)
    df.dropna(axis=1, inplace=True)
    df.sort_values(by='Fiscal-Date', ascending=False)
    return pd.pivot_table(data=df, index=['Fiscal-Date'], sort=False)
