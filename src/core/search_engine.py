"""
Main Search Engine class that orchestrates all search functionality.
This is the primary interface for the search engine API.
"""

import torch
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import os
import pickle

from ..data.text_processor import TextProcessor
from ..models.embedding_manager import EmbeddingManager
from ..models.clustering_manager import ClusteringManager
from ..search.semantic_search import SemanticSearch
from ..search.vector_search import VectorSearch
from ..utils.config import SearchConfig


class SearchEngine:
    """
    Main search engine class that combines clustering, semantic search, and vector search.
    """
    
    def __init__(self, config: SearchConfig):
        """
        Initialize the search engine with configuration.
        
        Args:
            config: SearchConfig object containing all necessary paths and parameters
        """
        self.config = config
        
        # Initialize CUDA if available
        if torch.cuda.is_available():
            torch.cuda.init()
            torch.rand(1).to("cuda")
        
        # Load data and models
        self._load_data()
        self._initialize_components()
        
    def _load_data(self):
        """Load posts data and pre-trained models."""
        # Load posts data
        with open(os.path.join(self.config.data_path, 'posts.pkl'), 'rb') as f:
            self.posts = pickle.load(f)
        
        # Load LDA model and vectorizer
        with open(os.path.join(self.config.data_path, 'lda_model.pkl'), 'rb') as f:
            self.lda_model = pickle.load(f)
            
        with open(os.path.join(self.config.data_path, 'vectorizer_lda.pkl'), 'rb') as f:
            self.vectorizer_lda = pickle.load(f)
    
    def _initialize_components(self):
        """Initialize all search engine components."""
        # Initialize text processor
        self.text_processor = TextProcessor()
        
        # Initialize embedding manager
        self.embedding_manager = EmbeddingManager(self.config)
        
        # Initialize clustering manager
        self.clustering_manager = ClusteringManager(
            self.lda_model, 
            self.vectorizer_lda, 
            self.posts
        )
        
        # Initialize search components
        self.semantic_search = SemanticSearch(
            self.embedding_manager,
            self.posts
        )
        
        self.vector_search = VectorSearch(
            self.text_processor,
            self.posts
        )
        
        # Get topic documents mapping
        self.topic_documents = self.clustering_manager.get_document_topics()
    
    def search(self, query: str, top_n: Optional[int] = None) -> pd.DataFrame:
        """
        Perform a search using clustering-based approach.
        
        Args:
            query: Search query string
            top_n: Maximum number of results to return
            
        Returns:
            DataFrame containing search results
        """
        # Get topic for the query
        topic_query = self.clustering_manager.get_topic_query(query)
        relevant_docs = self.topic_documents[topic_query]
        
        # Filter posts to relevant documents
        relevant_posts = self.posts[self.posts['Id'].isin(relevant_docs)]
        
        if len(relevant_posts) == 0:
            return pd.DataFrame()
        
        # Calculate similarities
        similarity_semantic_answer = self.semantic_search.similarity_clustering(
            query, 
            self.embedding_manager.answer_query_model, 
            relevant_posts, 
            self.embedding_manager.embeddings_answer
        )
        
        similarity_title = self.semantic_search.similarities_title_clustering(
            query, 
            self.embedding_manager.question_query_model, 
            relevant_posts, 
            self.embedding_manager.embeddings_titles
        )
        
        # Combine similarities with weights
        similarity_pond = (
            similarity_semantic_answer * self.config.coeff1 + 
            similarity_title * self.config.coeff3
        )
        
        # Order results
        ordre = self.semantic_search.order_similarity(similarity_pond)
        top_posts = relevant_posts.iloc[ordre]
        
        # Handle parent-child relationships
        top_posts["ParentId"] = top_posts["ParentId"].fillna(top_posts["Id"])
        top_posts_id = top_posts["ParentId"].drop_duplicates(keep='first')
        top_posts = top_posts[top_posts["ParentId"].isin(top_posts_id)]
        
        # Limit results if specified
        if top_n is not None:
            top_posts = top_posts.iloc[:top_n]
        
        return top_posts
    
    def semantic_search(self, query: str, top_n: int = 10) -> pd.DataFrame:
        """
        Perform semantic search on all documents.
        
        Args:
            query: Search query string
            top_n: Maximum number of results to return
            
        Returns:
            DataFrame containing search results
        """
        return self.semantic_search.closest_semantic_doc(
            query, 
            self.embedding_manager.answer_query_model, 
            self.embedding_manager.embeddings_answer, 
            top_n
        )
    
    def vector_search(self, query: str, top_n: int = 10) -> pd.DataFrame:
        """
        Perform vector-based search.
        
        Args:
            query: Search query string
            top_n: Maximum number of results to return
            
        Returns:
            DataFrame containing search results
        """
        return self.vector_search.search(query, top_n)
    
    def get_post_by_id(self, post_id: int) -> Optional[pd.Series]:
        """
        Get a specific post by its ID.
        
        Args:
            post_id: Post ID to retrieve
            
        Returns:
            Post data as pandas Series or None if not found
        """
        post = self.posts[self.posts['Id'] == post_id]
        return post.iloc[0] if len(post) > 0 else None
    
    def get_stats(self) -> Dict:
        """
        Get search engine statistics.
        
        Returns:
            Dictionary containing engine statistics
        """
        return {
            'total_posts': len(self.posts),
            'total_topics': len(self.topic_documents),
            'cuda_available': torch.cuda.is_available(),
            'models_loaded': {
                'question_model': self.embedding_manager.question_query_model is not None,
                'answer_model': self.embedding_manager.answer_query_model is not None,
                'lda_model': self.lda_model is not None,
                'vectorizer': self.vectorizer_lda is not None
            }
        } 