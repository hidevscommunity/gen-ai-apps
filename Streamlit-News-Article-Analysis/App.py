# Main Streamlit page
import sys
import os
import streamlit as st
from supabase import create_client, Client
# Get the absolute path to the directory containing this script (app.py)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Add the 'modules' directory to sys.path
LLM_directory = os.path.join(current_directory, 'llm')
Supabase_directory = os.path.join(current_directory, 'Supabase')
utils_directory = os.path.join(current_directory, 'utils')
sys.path.append(Supabase_directory)
sys.path.append(LLM_directory)
sys.path.append(utils_directory)

# Get the OpenAI API key 
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
LANGCHAIN_TRACING_V2 = st.secrets["LANGCHAIN_TRACING_V2"]
LANGCHAIN_ENDPOINT = st.secrets["LANGCHAIN_ENDPOINT"]
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
LANGCHAIN_PROJECT = st.secrets["LANGCHAIN_PROJECT"]
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

import sys
import logging
# import Union
from typing import Union
import json
import requests
import streamlit as st
from streamlit_folium import folium_static
import folium
from newspaper import Article
import streamlit as st 
from datetime import datetime
from llm.agent_main import AgentMain
from Supabase.Insertor import SupabaseInsertor
from Supabase.Extractor import SupabaseExtractor
from utils.Distance import DisruptionEventRanker, GeoCalculator
import multiprocessing
import pandas as pd
# For displaying the output of print() in Streamlit
from contextlib import contextmanager, redirect_stdout
from io import StringIO

supabaseInsertor = SupabaseInsertor(supabase)

@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield

@contextmanager
def st_capture_and_log(output_func):
    # Capture print statements
    with st_capture(output_func):
        # Capture logger information
        root_logger = logging.getLogger()
        original_handlers = root_logger.handlers
        original_level = root_logger.level
        root_logger.handlers = [StreamlitLogHandler(output_func)]

        try:
            yield
        finally:
            root_logger.handlers = original_handlers
            root_logger.setLevel(original_level)

class StreamlitLogHandler(logging.Handler):
    def __init__(self, output_func):
        super().__init__()
        self.output_func = output_func

    def emit(self, record):
        log_message = self.format(record)
        self.output_func(log_message)

class MapManager:
    """Class for managing the map and its components"""
    @classmethod
    def addAll_mirxes_suppliers(cls,map: folium.Map, mirxes_suppliers_info:Union[list[dict],pd.DataFrame]) -> folium.Map:
        """
        Adds Mirxes suppliers to map
        """
        # convert to list of dict if pd.DataFrame
        if isinstance(mirxes_suppliers_info, pd.DataFrame):
            # Convert Pandas DataFrame to list of dict
            mirxes_suppliers_info = mirxes_suppliers_info.to_dict('records')
        
        for supplier in mirxes_suppliers_info:
            folium.Marker(
                [supplier['lat'], supplier['lng']], popup=supplier['Name']
            ).add_to(map)
        return map
    
    @classmethod
    def addSingle_disruption_event(cls,map: folium.Map, disruption_event:dict) -> folium.Map:
        """
        Adds one disruption event to map
        """
        colour_risk_mapping = {
            'Low': 'orange',
            'Medium': 'orange',
            'High': 'red'
        }
        try:
            folium.Circle(
                [disruption_event['lat'], disruption_event['lng']],
                radius=disruption_event['Radius'],
                color=colour_risk_mapping[disruption_event['risk_score']],
                fill=True,
                fill_color=colour_risk_mapping[disruption_event['risk_score']],
                tooltip=disruption_event['Title'],
                popup=f'Risk Score: {disruption_event["risk_score"]},\n\nSeverity: {disruption_event["Severity"]}'
            ).add_to(map)
        except Exception as e:
            print(f'Error adding disruption event: {e}')
            pass

        return map
    @classmethod
    def addAll_disruption_event(cls,map: folium.Map, all_disruption_events:list[dict]) -> folium.Map:
        """
        Adds disruption event to map
        """
        for disruption_event in all_disruption_events:
            cls.addSingle_disruption_event(map, disruption_event)
        return map

mirxes_suppliers_info = pd.read_csv('./src/MOCK_Supplier.csv')
article_dict = None
# Setting page title and header
st.markdown("<h1 style='text-align: center;'>Article Disruption Analysis 😬</h1>", unsafe_allow_html=True)
# Add a description
st.subheader("""🌟Goal of the Demonstrating the prowess of using LLM to "Replace" traditional NLP programming 🚀""")
st.markdown("""> This is a lesser talked about application of LLMs, but I personally feel that it is one of the most powerful use cases of LLMs.""")
st.markdown("""The Ability to replace training BinaryClassifers models, NERs, and other traditional NLP programming with LLMs.""")
# Youtube Video Link
st.markdown("---")
# Add more description
st.markdown("""### 📋 Use Case: Identify Potential Disruption Events to Supply chain through News mointoring """)
# Add 3 Sample News article as default
with st.expander(f"📰 Sample News Articles"):
    sample1, sample2, sample3 = st.columns(3)
    sample1.info(f"📰 Sample News Article 1\n\nHurricane Idalia Hits Florida With 125 Mph Winds, Flooding Streets, Snapping Trees and Cutting Power\n\nhttps://www.usnews.com/news/us/articles/2023-08-30/idalia-predicted-to-hit-florida-as-category-4-hurricane-with-catastrophic-storm-surge")
    sample2.info(f'📰 Sample News Article 2\n\nScoot among airlines, suppliers that warn of hit from RTX engine-snag disclosure\n\nhttps://www.straitstimes.com/business/olam-confirms-bond-posted-for-director-of-nigerian-unit-amid-police-probe')
    sample3.info(f'📰 Sample News Article 3\n\nUnrelenting rain causes more than 100 landslides, traps residents in floodwaters in southern China\n\nhttps://www.reuters.com/business/environment/unrelenting-rain-causes-more-than-100-landslides-traps-residents-floodwaters-2023-09-12/')


# Custom Streamlit component to display Article Data
def st_article_data(article_dict):
    st.write(f'📝 Article Data')
    st.table(article_dict)

# Define a custom context manager to capture print statements and log messages
@contextmanager
def st_capture(output_func):
    with StringIO() as stdout, redirect_stdout(stdout):
        old_write = stdout.write

        def new_write(string):
            ret = old_write(string)
            output_func(stdout.getvalue())
            return ret

        stdout.write = new_write
        yield

# Url input
with st.form(key='my_form'):
    url = st.text_input("Enter any News Article url you want to Analyze for Disruption Event to Supply Chain ( or copy the links from the samples )")
    submit_button = st.form_submit_button(label="Run")

if submit_button:
    # Display the logs
    placeholder_logs = st.empty()
    with st.spinner(f"Running Web Scraping + LLM Structed Task Based Chaining on {url}"):
        with st.expander(f"🧾 Logs...",expanded=True):
            with st_capture_and_log(st.write):
                    try:
                        article = AgentMain.processUrl(url)
                    except Exception as e:
                        st.write(f'Error: {e}')
                        sys.exit(1)

                    if isinstance(article, Article):
                        # Insert into Supabase
                        article_dict = supabaseInsertor._formatArticleDict(article)
                        st_article_data(article_dict)

                        # Insert into Supabase
                        try:
                            article_dict = supabaseInsertor.addArticleData(article_dict)
                        except Exception as e:
                            st.write(f'Error inserting into Supabase: {e}')
                            pass

                    else:
                        st.write(article)

output_break = st.markdown("---")

if article_dict:

    article_dict = DisruptionEventRanker.addSupplierMapping(article_dict)
    article_dict = DisruptionEventRanker.addRiskScore(article_dict)
    # Add the Map, starting at disruption event coords
    st.markdown(f"<h3 style='text-align:center;'>Estimated Radius of Impact</h3>", unsafe_allow_html=True)

    m = folium.Map(location=[article_dict['lat'], article_dict['lng']], zoom_start=12)
    # Add all Mirxes suppliers to map
    m = MapManager.addAll_mirxes_suppliers(m, mirxes_suppliers_info)
    m = MapManager.addSingle_disruption_event(m, article_dict)
    folium_static(m)
    
    col1,col2 = st.columns([0.2,0.7])
    col1.markdown(f"<div><h4 style='text-align:center;'>Event Type:\n\n{article_dict['DisruptionType']}</h4></div>", unsafe_allow_html=True)
    # col1.image(f'./src/earthquake.png', use_column_width=True)
    st.markdown(f"<h3 style='text-align:center;'>Severity Metrics</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align:center;'>{article_dict['Severity']}</h4>", unsafe_allow_html=True)
    # Display Potential Suppliers Affected
    st.markdown(f"<h3 style='text-align:center;'>Potential Suppliers Affected</h3>", unsafe_allow_html=True)
    st.table(article_dict['suppliers'][:10])

    # Display output
    st.markdown(f"<h3 style='text-align: center;'>{article_dict['Title']} 😬</h3>", unsafe_allow_html=True)
    st.write(f'Article Url: {article_dict["Url"]}')
    st.image(f'{article_dict["ImageUrl"]}', use_column_width=True)