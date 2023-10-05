import newspaper 
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Type # Import Type for forward declarations
from abc import ABC, abstractmethod
from newspaper import Config, Article, Source

class Scraper:
    """Main class for scraping news articles, using the newspaper3k library."""

    def _filter(self,article:Article):
        """
        Purpose: Filter out articles that are not vaild news articles
            1. Check if Text/Title is empty
            2. Check if article is in English
            3. Check if article.publish_date is not None

        Parameters:
            > article: Article object
        Returns:
            >  True if article is a vaild news article
            > False if article is not a vaild news article (or if there is an error in webscraping)
        """
        if article.text == '' or article.title == '':
            print(f'Article text/title is empty: {article.url}')
            return False
        # Check if article text is shorter then 100 characters
        if len(article.text) < 100:
            print(f'Article text is too short. Text: {article.text} {article.url}')
            return False
        if article.meta_lang != 'en':
            print(f'Article is not in English: {article.url}')
            return False
        if article.publish_date is None:
            print(f'Article publish date is None: {article.url}')
            return False
        
        return True
    def _remove_whitespace(text:str) -> str:
        """
        Remove trailing whitespace and newlines from text or title
        """
        return text.strip().replace('\n', ' ')
    
    @classmethod
    def get_source_url(cls,base_source):
        """Given a base news source, returns all the urls for the articles on that source."""
        source = newspaper.build(base_source)
        return [article.url for article in source.articles]


    @classmethod
    def scrape(cls,url:str) -> Article:
        """Given a url, returns a dictionary of the article's title, image url, and text."""
        article = newspaper.Article(url)
        article.download()
        article.parse()

        # clean up the text and title
        article.title = cls._remove_whitespace(article.title)
        article.text = cls._remove_whitespace(article.text)

        return article

        
