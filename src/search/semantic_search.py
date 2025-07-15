"""
Semantic search functionality using sentence transformers.
"""

import torch
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from typing import Dict, List
from ..models.embedding_manager import EmbeddingManager


class SemanticSearch:
    """
    Handles semantic search using sentence transformer embeddings.
    """
    
    def __init__(self, embedding_manager: EmbeddingManager, posts: pd.DataFrame):
        """
        Initialize semantic search.
        
        Args:
            embedding_manager: EmbeddingManager instance
            posts: DataFrame containing posts data
        """
        self.embedding_manager = embedding_manager
        self.posts = posts
    
    def encode_query(self, query: str, model: SentenceTransformer) -> torch.Tensor:
        """
        Encode a query using a sentence transformer model.
        
        Args:
            query: Query string
            model: Sentence transformer model
            
        Returns:
            Query embedding as tensor
        """
        return self.embedding_manager.encode_query(query, model)
    
    def similarity(self, query: str, model: SentenceTransformer, 
                  embeddings: torch.Tensor, batch_size: int = 1024) -> np.ndarray:
        """
        Calculate semantic similarity between query and documents.
        
        Args:
            query: Query string
            model: Sentence transformer model
            embeddings: Document embeddings
            batch_size: Batch size for processing
            
        Returns:
            Array of similarity scores
        """
        query_embedding = self.encode_query(query, model)
        scores = []
        
        for i in range(0, len(embeddings), batch_size):
            key_embedding = torch.stack(embeddings[i:i+batch_size])
            with torch.no_grad():
                score = torch.cosine_similarity(query_embedding, key_embedding)
            scores.extend(score.cpu().detach().numpy())
        
        return np.array(scores)
    
    def similarity_order(self, matrix_similarity: np.ndarray) -> List[int]:
        """
        Get ordered indices based on similarity scores.
        
        Args:
            matrix_similarity: Array of similarity scores
            
        Returns:
            List of indices ordered by similarity (descending)
        """
        return list(np.argsort(-np.array(matrix_similarity)))
    
    def closest_semantic_doc(self, query: str, model: SentenceTransformer, 
                           embeddings: torch.Tensor, top_n: int = 10) -> pd.DataFrame:
        """
        Find the most semantically similar documents.
        
        Args:
            query: Query string
            model: Sentence transformer model
            embeddings: Document embeddings
            top_n: Number of top results to return
            
        Returns:
            DataFrame with top similar documents
        """
        matrix_similarity = self.similarity(query, model, embeddings)
        ordre = self.similarity_order(matrix_similarity)
        return self.posts.iloc[ordre[:top_n]]
    
    def similarities_title(self, query: str, model: SentenceTransformer, 
                          embeddings: torch.Tensor, batch_size: int = 1024) -> np.ndarray:
        """
        Calculate title similarities with parent-child relationship handling.
        
        Args:
            query: Query string
            model: Sentence transformer model
            embeddings: Title embeddings
            batch_size: Batch size for processing
            
        Returns:
            Array of title similarity scores
        """
        query_embedding = self.encode_query(query, model)
        scores = []
        
        for i in range(0, len(embeddings)):
            title_id = self.posts['ParentId'].iloc[i]
            if pd.isna(title_id):
                key_embedding = embeddings[i]
            else:
                title_id = int(title_id)
                index_parent = self.posts[self.posts['Id'] == title_id].index.values.tolist()[0]
                key_embedding = embeddings[index_parent]
            
            with torch.no_grad():
                score = torch.cosine_similarity(query_embedding, key_embedding)
            scores.extend(score.cpu().detach().numpy())
        
        return np.array(scores)
    
    def similarity_clustering(self, query: str, model: SentenceTransformer, 
                            relevant_posts: pd.DataFrame, embeddings: Dict[int, torch.Tensor], 
                            batch_size: int = 1024) -> np.ndarray:
        """
        Calculate semantic similarity for clustering-based search.
        
        Args:
            query: Query string
            model: Sentence transformer model
            relevant_posts: DataFrame of relevant posts
            embeddings: Dictionary of embeddings keyed by post ID
            batch_size: Batch size for processing
            
        Returns:
            Array of similarity scores
        """
        query_embedding = self.encode_query(query, model)
        relevant_ids = list(relevant_posts["Id"])
        filtered_embeddings = {post_id: embeddings[post_id] for post_id in relevant_ids}
        
        if len(filtered_embeddings) == 0:
            raise ValueError("No embeddings found for relevant posts")
        
        scores = []
        for i in range(0, len(filtered_embeddings), batch_size):
            key_embedding = torch.stack(list(filtered_embeddings.values())[i:i+batch_size])
            with torch.no_grad():
                score = torch.cosine_similarity(query_embedding, key_embedding)
            scores.extend(list(score.cpu().detach().numpy()))
        
        return np.array(scores)
    
    def similarities_title_clustering(self, query: str, model: SentenceTransformer, 
                                    relevant_posts: pd.DataFrame, embeddings: Dict[int, torch.Tensor], 
                                    batch_size: int = 1024) -> np.ndarray:
        """
        Calculate title similarities for clustering-based search.
        
        Args:
            query: Query string
            model: Sentence transformer model
            relevant_posts: DataFrame of relevant posts
            embeddings: Dictionary of title embeddings keyed by post ID
            batch_size: Batch size for processing
            
        Returns:
            Array of title similarity scores
        """
        query_embedding = self.encode_query(query, model)
        scores = []
        relevant_ids = list(relevant_posts["Id"])
        filtered_embeddings = [embeddings[post_id] for post_id in relevant_ids]
        
        for i in range(0, len(filtered_embeddings), batch_size):
            key_embedding = torch.stack(filtered_embeddings[i:i+batch_size])
            with torch.no_grad():
                score = torch.cosine_similarity(query_embedding, key_embedding)
            scores.extend(score.cpu().detach().numpy())
        
        return np.array(scores)
    
    def order_similarity(self, matrix_similarity: np.ndarray) -> List[int]:
        """
        Get ordered indices based on similarity scores.
        
        Args:
            matrix_similarity: Array of similarity scores
            
        Returns:
            List of indices ordered by similarity (descending)
        """
        return list(np.argsort(-np.array(matrix_similarity))) 