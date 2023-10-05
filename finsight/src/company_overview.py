import requests
import streamlit as st


AV_API_KEY = st.secrets["av_api_key"]


def company_overview(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": AV_API_KEY
    }

    # Send a GET request to the API
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if not data:
            print(f"No data found for {symbol}")
            return None
        extracted_data = {
            "Symbol": data.get("Symbol"),
            "AssetType": data.get("AssetType"),
            "Name": data.get("Name"),
            "Description": data.get("Description"),
            "CIK": data.get("CIK"),
            "Exchange": data.get("Exchange"),
            "Currency": data.get("Currency"),
            "Country": data.get("Country"),
            "Sector": data.get("Sector"),
            "Industry": data.get("Industry"),
            "Address": data.get("Address"),
            "FiscalYearEnd": data.get("FiscalYearEnd"),
            "LatestQuarter": data.get("LatestQuarter"),
            "MarketCapitalization": float(data.get("MarketCapitalization")),
        }
        
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return extracted_data


if __name__ == "__main__":
    ans = company_overview("TSLA")
    print(ans)
