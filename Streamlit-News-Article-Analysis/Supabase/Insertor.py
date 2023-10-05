import pandas as pd
from dotenv import load_dotenv
import os

import postgrest
from postgrest.exceptions import APIError
from tqdm import tqdm
# Supabase
from supabase import create_client, Client
import newspaper
from newspaper import Config, Article, Source
# # Load variables from the .env file
# load_dotenv('.env')
# # Access the variables
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

import logging
logger = logging.getLogger(__name__)
class SupabaseInsertor:
    """
    TLDR: "Fancy INSERT INTO statement for the supabase" (Need to migrate over)

    Methods:
        * addDisruptionEvent(self, DisruptionEvent: dict)
        * addEventDataRelation
    """
        
    # supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    def __init__(self, supabase_client:Client):
        self.supabase = supabase_client

    def addArticleData(self,article:Article):
        article_dict = self._formatArticleDict(article)
        try:
            data, count = self._insertArticleData(article_dict)
            id = self._extractArticleId(data)
            article_dict['id'] = id
            logger.info(f'Successfully Inserted article: {article.title} with id: {id}')
            return article_dict
        except postgrest.exceptions.APIError as e:
            return self._handleInsertError(e, article_dict, "Article")


    def _formatArticleDict(self,article:Article) -> dict:
        print(article.publish_date.isoformat())
        # Round the coordinates to 7 decimal places
        article.additional_data["coordinates"] = [round(coord, 7) for coord in article.additional_data["coordinates"]]
        return {
            "Title": article.title,
            "Text": article.text,
            "Location": article.additional_data["location"],
            
            "lat": article.additional_data["coordinates"][0],
            "lng": article.additional_data["coordinates"][1],
            "DisruptionType": article.additional_data["disruptionType"],
            "Severity": article.additional_data["severity"],
            # "SourceName": article.source_url,
            "Url": article.url,
            "ImageUrl": article.top_image,
            "PublishedDate": article.publish_date.isoformat(),
            "Radius": article.additional_data["radius"]*1000, # Convert to meters
        }
    def _insertArticleData(self, article_dict:dict):
        return self.supabase.table("Article").insert(article_dict).execute()

    def _extractArticleId(self,data):
        return data[1][0]['id']

    def _handleInsertError(self,error, article_dict:dict,table):
        # logger.error(f'Error inserting into Supabase: {error}')
        # logger.error(error.code, error.message, error.details)
        if error.code == '23505':
            logger.error(f'Article with URL {article_dict["Url"]} already exists in the database.')
            existing_data = self.supabase.table(table).select('*').eq('Url', article_dict['Url']).execute()
            return existing_data.data[0]
        else:
            logger.error(f'Unexpected error: {error}')