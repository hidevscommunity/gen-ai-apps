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

# Load variables from the .env file
success = load_dotenv('.env')
if success:
    print('Successfully loaded .env file')
# Access the variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
class SupabaseExtractor:
    """
    TLDR: "Fancy INSERT INTO statement for the supabase" (Need to migrate over)
    Already initilized with the supabase client
    Methods:
        * addDisruptionEvent(self, DisruptionEvent: dict)
        * addEventDataRelation
    """
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    @classmethod
    def extractSources(cls) -> list[dict]:
        """Extracts all the sources from the Supabase database.
        Default source_name is ['straitstimes'].
        Example ouput:
        [{'Name': 'straitstimes', 'domain_url': 'https://www.straitstimes.com/', 'created_at': '2023-09-04T07:24:24.143487+00:00'}, {'Name': 'scmp', 'domain_url': 'https://www.scmp.com/', 'created_at': '2023-09-04T08:38:51.475122+00:00'}, {'Name': 'reuters', 'domain_url': 'https://www.reuters.com/', 'created_at': '2023-09-04T08:39:49.793189+00:00'}]"""
        # Check if each source name is valid
        sources = cls.supabase.table("Source").select("*").execute()
        return sources.data
    
    @classmethod
    def extractAllArticles(cls) -> list[dict]:
        """Extract all articles from the Article table in Supabase."""
        all_articles = cls.supabase.table("Article").select("*").execute()
        return all_articles.data
    
    @classmethod
    def extractIdArticle(cls,id) -> dict:
        """wah"""
        try:
            article = cls.supabase.table("Article").select("*").eq('id',id).execute()
            return article.data[0]
        except Exception as e:
            print(e)
            return None

    
    @classmethod
    def extractAllArticleUrl(cls) -> list[str]:
        """Extract all urls from the Article table in Supabase."""
        all_articles = cls.supabase.table("Article").select("Url").execute()
        return [article['Url'] for article in all_articles.data]

    @classmethod
    def extractAllSupplierInfo(cls) -> list[dict]:
        """Extract all supplier info from the Supplier table in Supabase."""
        all_suppliers = cls.supabase.table("Supplier").select("*").execute()
        return all_suppliers.data
    

# Test for now
if __name__ == "__main__":

    sources = SupabaseExtractor.extractSources()
    print(f'Sources: {sources}, type: {type(sources)}')
    article_url = SupabaseExtractor.extractAllArticleUrl()
    print(f'Article url: {article_url}, type: {type(article_url)}')
    
