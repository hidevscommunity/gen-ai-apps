"""
Main Script to Scrape and process all the news articles in real time and store them Supabase
Should be ran every 24hours?
"""
# Author: Kaleb-Nim
# Date: 11th September 2023 
from utils.Webscraper import Webscraper
from Supabase.Extractor import SupabaseExtractor
from Supabase.Insertor import SupabaseInsertor
from llm.agent_main import AgentMain
import logging
import os
from newspaper import Config, Article, Source
from time import time
from dotenv import load_dotenv
import random
from colorlog import ColoredFormatter
import logging
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)-8s%(reset)s %(message)s",
    datefmt=None,
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    },
    secondary_log_colors={},
    style='%'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

success = load_dotenv('.env')

TEMP_ARTICLES_URL =['https://www.reuters.com/business/environment/remnants-typhoon-haikui-cause-floods-southeastern-china-2023-09-06/',
 'https://www.scmp.com/comment/opinion/article/3233689/beyond-china-economies-us-and-europe-are-no-less-vulnerable',
 'https://www.scmp.com/economy/global-economy/article/3234140/vietnam-ups-durian-trade-china-land-border-offers-cost-advantage-challenge-thai-dominance',
 'https://www.straitstimes.com/world/race-to-find-survivors-as-morocco-quake-deaths-top-1300',
 'https://www.scmp.com/business/companies/article/3234156/farming-flies-freeze-drying-ugly-fruit-and-jewellery-scraps-how-hong-kong-start-ups-are-reducing?module=live&pgtype=homepage',
 'https://www.scmp.com/comment/opinion/article/3230344/how-ais-rise-could-be-boon-manufacturing-and-healthcare-sectors-asia',
 'https://www.scmp.com/comment/opinion/article/3233610/china-must-slow-down-investment-if-it-wants-rebalance-its-debt-laden-economy',
 'https://www.scmp.com/comment/opinion/article/3230626/us-china-tech-war-semiconductors-heart-competition-driving-world-towards-new-cold-war',
 'https://www.scmp.com/week-asia/politics/article/3234129/malaysian-pm-anwar-spend-billions-5-year-plan-reduce-poverty-boost-economic-growth',
 'https://www.scmp.com/comment/opinion/article/3234037/hong-kong-floods-even-climate-change-sceptics-must-see-need-prepare-extreme-weather?module=opinion&pgtype=homepage']
class MDE:
    """Main Monitoring Disruption Event class that handles Main Script to Scrape and process all the news articles in real time and store them in Supabase. Should be run every 24 hours."""

    def __init__(self):
        self.source_objects = []  # Placeholder for source objects
        self.articles = []  # Articles to be processed by llm agents, articles will be filtered step by step
        self.processed_articles = []  # Articles that have been processed by llm agents
        self.supabase_base_Sources_url = self.loadSourcesSupabase()
        self.supabase_Articles_url = self.loadArticlesSupabase()
    
    def loadSourcesSupabase(self) -> list[str]:
        """Load all news sources we want to webscrape from Supabase Source Table
        Returns:
            > list[dict]: List of all the base_urls of news sources in Supabase"""
        baseSources = SupabaseExtractor.extractSources()
        logger.info(f'Number of base news sources in Supabase: {len(baseSources)}')
        # Get the base_url for each source
        base_urls = [source['domain_url'] for source in baseSources]
        return base_urls

    def loadArticlesSupabase(self) -> list[str]:
        """Load all the article urls from Supabase Articles Table"""
        return SupabaseExtractor.extractAllArticleUrl()

    def downloadSources(self, base_urls: list[str]) -> list[Source]:
        """
        Build all the source objects, takes ~1min per number of sources
        Takes in a list of base_urls and builds the source objects
        """
        logger.info(f"Start: {time()}")
        source_objects = Webscraper.downloadAllSources(base_urls=base_urls)
        self.source_objects = source_objects

    def extract_non_duplicate_articles(self) -> list[Article]:
        """Purpose: Filter out the article objects that we already have in our Supabase database
        Args:
            > source_objects: list[Source]
            > supabase_Articles_url: list[str]
        Returns:
            > self.articles: list[Article]
        """
        # Get all the urls from the sources
        all_url_list = [article.url for source in self.source_objects for article in source.articles]

        # all_url_list = TEMP_ARTICLES_URL # For testing purposes
        print(f'Number of articles scraped: {len(all_url_list)}')

        # Filter out the urls that we already have in our database
        # Compare the two lists and remove any duplicates
        new_urls = [url for url in all_url_list if url not in self.supabase_Articles_url]

        # Remove articles that are duplicates from the source
        new_articles = [article for source in self.source_objects for article in source.articles if article.url in new_urls]
        logger.info(f'Number of non-duplicate articles: {len(new_articles)}')

        # Randomly get 20 articles from the list
        new_articles = random.sample(new_articles, 20)
        self.articles = new_articles

    def parseNlpAllArticles(self) -> list[Article]:
        """Parse all the article objects with NLP, This step must be done before the llm agents can process the articles"""
        self.articles = Webscraper.parseNlpAllArticles(self.articles)

    def processArticles(self):
        """Process all the articles using the llm agents
        Will add the processed for Location,coordinates and severity stuff to the articles.additional_data dict"""
        # Process all the articles using the llm agents
        for article in self.articles:
            processed_article = AgentMain.process(article)
            if isinstance(processed_article, Article):
                # Add to supabasae directly for storage
                try:
                    SupabaseInsertor.addArticleData(processed_article)
                except Exception as e:
                    logger.error(f"Error inserting articles into Supabase: {str(e)}")
            else:
                # Display the message from LLM Agent (Most likely is News not disruption event)
                logger.info(processed_article)


# run the main script
if __name__ == '__main__':
    # Initialise the MDE class, extracting News Sources and Stored Articles from Supabase
    mde = MDE()
    # base_urls = mde.loadSourcesSupabase()
    # Start the Live Web Scraping of articles from the pre-defined News Sources
    mde.downloadSources(['https://www.straitstimes.com/']) # Takes ~1.5min per number of sources
    # Filter out all the articles that are not duplicates from the Articles already found in our Supabase
    mde.extract_non_duplicate_articles()
    # Process and Format the articles webscraped, to be ready for the llm agents to run 
    mde.parseNlpAllArticles()
    # Extracts out, Location+Coordinates, Disaster Type, Severity, and other data from the articles Using LLM Agents
    # Insert all the processed articles into Supabase with all the above information
    mde.processArticles() #This will also Insert all the processed articles into Supabase with all the above information