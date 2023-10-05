import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))

import requests
import streamlit as st
# from dotenv import dotenv_values

from src.pydantic_models import BalanceSheetInsights
from src.utils import insights, get_total_revenue, safe_float

# config = dotenv_values(".env")
# OPENAI_API_KEY = config["OPENAI_API_KEY"]
# AV_API_KEY = config["ALPHA_VANTAGE_API_KEY"]

AV_API_KEY = st.secrets["av_api_key"]

def charts(data):
    report = data['annualReports'][0]
    asset_composition = {"total_current_assets": report['totalCurrentAssets'],
        "total_non_current_assets": report['totalNonCurrentAssets']              
    }

    liabilities_composition = {
        "total_current_liabilities": report['totalCurrentLiabilities'],
        "total_non_current_liabilities": report['totalNonCurrentLiabilities']
    }

    debt_structure = {
        "short_term_debt": report['shortTermDebt'],
        "long_term_debt": report['longTermDebt']
    }

    return {
        "asset_composition": asset_composition,
        "liabilities_composition": liabilities_composition,
        "debt_structure": debt_structure
    }

         

def metrics(data, total_revenue):

    # Extracting values from the data
    totalCurrentAssets = safe_float(data.get("totalCurrentAssets"))
    totalCurrentLiabilities = safe_float(data.get("totalCurrentLiabilities"))
    totalLiabilities = safe_float(data.get("totalLiabilities"))
    totalShareholderEquity = safe_float(data.get("totalShareholderEquity"))
    totalAssets = safe_float(data.get("totalAssets"))
    inventory = safe_float(data.get("inventory"))

    # Calculate metrics, but check for N/A values in operands
    current_ratio = (
        "N/A"
        if "N/A" in (totalCurrentAssets, totalCurrentLiabilities)
        else totalCurrentAssets / totalCurrentLiabilities
    )
    debt_to_equity_ratio = (
        "N/A"
        if "N/A" in (totalLiabilities, totalShareholderEquity)
        else totalLiabilities / totalShareholderEquity
    )
    quick_ratio = (
        "N/A"
        if "N/A" in (totalCurrentAssets, totalCurrentLiabilities, inventory)
        else (totalCurrentAssets - inventory) / totalCurrentLiabilities
    )
    asset_turnover = (
        "N/A" if "N/A" in (total_revenue, totalAssets) else total_revenue / totalAssets
    )
    equity_multiplier = (
        "N/A"
        if "N/A" in (totalAssets, totalShareholderEquity)
        else totalAssets / totalShareholderEquity
    )

    # Returning the results
    return {
        "current_ratio": current_ratio,
        "debt_to_equity_ratio": debt_to_equity_ratio,
        "quick_ratio": quick_ratio,
        "asset_turnover": asset_turnover,
        "equity_multiplier": equity_multiplier,
    }


def balance_sheet(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "BALANCE_SHEET",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    if not data:
            print(f"No data found for {symbol}")
            return None
    
    chart_data = charts(data)

    report = data["annualReports"][0]
    total_revenue = get_total_revenue(symbol)
    met = metrics(report, total_revenue)

    data_for_insights = {
        "annual_report_data": report,
        "historical_data": chart_data,
    }
    ins = insights("balance sheet", data_for_insights, BalanceSheetInsights)

    return {
        "metrics": met,
        "chart_data": chart_data,
        "insights": ins
    }

if __name__ == "__main__":
    data = balance_sheet("MSFT")
    print("Metrics: ", data['metrics'])
    print("Chart Data: ", data['charts'])
    print("Insights", data['insights'])


