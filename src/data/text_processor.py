"""
Text processing utilities for the search engine.
"""

import re
from bs4 import BeautifulSoup
import pandas as pd
import os
import pickle
from typing import List, Optional


class TextProcessor:
    """
    Handles text cleaning and preprocessing for the search engine.
    """
    
    def __init__(self):
        """Initialize the text processor."""
        pass
    
    def clean_post(self, text: str) -> str:
        """
        Clean HTML content and normalize text.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text string
        """
        if not text or pd.isna(text):
            return ""
        
        # Parse HTML and extract text
        soup = BeautifulSoup(text, "html.parser")
        sent = soup.get_text()
        
        # Normalize whitespace
        cleaned_text = re.sub(r'\s+', ' ', sent).strip()
        
        # Remove special characters and convert to lowercase
        cleaned_text = re.sub(r'[^\w\s]', '', cleaned_text).lower()
        
        return cleaned_text
    
    def remove_tags(self, text: str) -> str:
        """
        Remove HTML tags and normalize text for embeddings.
        
        Args:
            text: Text with HTML tags
            
        Returns:
            Cleaned text without HTML tags
        """
        if not text or pd.isna(text):
            return ""
        
        text = text.replace('"', '')
        text = text.replace('\n', ' ')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        
        return text
    
    def extract_data(self, datapath: str) -> pd.DataFrame:
        """
        Extract and clean data from XML files.
        
        Args:
            datapath: Path to the data directory
            
        Returns:
            DataFrame with cleaned posts data
        """
        # Read posts XML
        posts = pd.read_xml(
            os.path.join(datapath, 'Posts.xml'), 
            parser="etree", 
            encoding="utf8"
        )
        
        # Clean body and title
        posts['cleaned_body'] = posts.Body.fillna('').apply(self.clean_post)
        posts['cleaned_title'] = posts.Title.fillna('').apply(self.clean_post)
        
        return posts
    
    def save_processed_data(self, posts: pd.DataFrame, savepath: str):
        """
        Save processed data to pickle file.
        
        Args:
            posts: DataFrame to save
            savepath: Path to save the file
        """
        with open(os.path.join(savepath, 'posts.pkl'), 'wb') as f:
            pickle.dump(posts, f)
    
    def load_processed_data(self, datapath: str) -> pd.DataFrame:
        """
        Load processed data from pickle file.
        
        Args:
            datapath: Path to the data directory
            
        Returns:
            DataFrame with posts data
        """
        with open(os.path.join(datapath, 'posts.pkl'), 'rb') as f:
            return pickle.load(f) 