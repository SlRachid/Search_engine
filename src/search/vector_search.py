"""
Vector-based search functionality using TF-IDF and count vectors.
"""

import numpy as np
import torch
import pandas as pd
from typing import List, Tuple, Optional
import pickle
import os
from ..data.text_processor import TextProcessor


class VectorSearch:
    """
    Handles vector-based search using TF-IDF and count vectors.
    """
    
    def __init__(self, text_processor: TextProcessor, posts: pd.DataFrame):
        """
        Initialize vector search.
        
        Args:
            text_processor: TextProcessor instance
            posts: DataFrame containing posts data
        """
        self.text_processor = text_processor
        self.posts = posts
        self.vocabulaire = None
        self.docs_matrix = None
        
        # Load vectorizer data if available
        self._load_vectorizer_data()
    
    def _load_vectorizer_data(self):
        """Load vocabulary and document matrix if available."""
        try:
            with open(os.path.join('data', 'Vocabulaire.pkl'), 'rb') as f:
                self.vocabulaire = pickle.load(f)
            
            with open(os.path.join('data', 'docs_matrix.pkl'), 'rb') as f:
                self.docs_matrix = pickle.load(f)
        except FileNotFoundError:
            print("Vectorizer data not found. Run vectorize.py first to generate vectorizer data.")
    
    def vectorize_query(self, query: str, vocabulaire: np.ndarray) -> List[int]:
        """
        Vectorize a query using the vocabulary.
        
        Args:
            query: Query string
            vocabulaire: Vocabulary array
            
        Returns:
            Query vector
        """
        query = self.text_processor.clean_post(query)
        words = query.split()
        
        vector_L = [0] * len(vocabulaire)
        for word in words:
            if word in vocabulaire:
                index = np.where(vocabulaire == word)[0][0]
                vector_L[index] += 1
        
        return vector_L
    
    def vectorizer_search(self, query: str, vocabulaire: np.ndarray, 
                         docs_matrix: np.ndarray) -> List[float]:
        """
        Perform vector-based search.
        
        Args:
            query: Query string
            vocabulaire: Vocabulary array
            docs_matrix: Document matrix
            
        Returns:
            List of similarity scores
        """
        vector_query = self.vectorize_query(query, vocabulaire)
        vector_query = torch.Tensor(vector_query).to("cuda")
        
        scores = []
        Acoo = docs_matrix.tocoo()
        sparse_docs_matrix = torch.sparse.LongTensor(
            torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
            torch.LongTensor(Acoo.data.astype(np.int32))
        ).to("cuda")
        
        for i in range(0, docs_matrix.shape[0]):
            with torch.no_grad():
                vector_key = sparse_docs_matrix[i].to_dense().unsqueeze(0)
                score = torch.cosine_similarity(vector_query, vector_key).cpu().numpy()[0]
                scores.append(score)
        
        return scores
    
    def vectorizer_search_clustering(self, query: str, docs_matrix: np.ndarray, 
                                   vocabulaire: np.ndarray) -> List[float]:
        """
        Perform vector-based search for clustering approach.
        
        Args:
            query: Query string
            docs_matrix: Document matrix
            vocabulaire: Vocabulary array
            
        Returns:
            List of similarity scores
        """
        vector_query = self.vectorize_query_clustering(query, docs_matrix, vocabulaire)
        vector_query = torch.Tensor(vector_query).to("cuda")
        
        Acoo = docs_matrix.tocoo()
        sparse_docs_matrix = torch.sparse.LongTensor(
            torch.LongTensor([Acoo.row.tolist(), Acoo.col.tolist()]),
            torch.LongTensor(Acoo.data.astype(np.int32))
        ).to("cuda")
        
        scores = []
        for i in range(0, docs_matrix.shape[0]):
            with torch.no_grad():
                score = torch.cosine_similarity(
                    vector_query, 
                    sparse_docs_matrix[i].to_dense().unsqueeze(0)
                ).cpu().numpy()
                scores.extend(score)
        
        return scores
    
    def vectorize_query_clustering(self, query: str, matrix_docs: np.ndarray, 
                                 vocabulaire: np.ndarray) -> List[int]:
        """
        Vectorize query for clustering approach.
        
        Args:
            query: Query string
            matrix_docs: Document matrix
            vocabulaire: Vocabulary array
            
        Returns:
            Query vector
        """
        query = self.text_processor.clean_post(query)
        words = query.split()
        
        vector_L = [0] * len(vocabulaire)
        for word in words:
            if word in vocabulaire:
                index = np.where(vocabulaire == word)[0][0]
                vector_L[index] += 1
        
        return vector_L
    
    def search(self, query: str, top_n: int = 10) -> pd.DataFrame:
        """
        Perform vector-based search and return top results.
        
        Args:
            query: Query string
            top_n: Number of top results to return
            
        Returns:
            DataFrame with top results
        """
        if self.vocabulaire is None or self.docs_matrix is None:
            raise ValueError("Vectorizer data not loaded. Run vectorize.py first.")
        
        scores = self.vectorizer_search(query, self.vocabulaire, self.docs_matrix)
        order = list(np.argsort(-np.array(scores)))
        
        return self.posts.iloc[order[:top_n]]
    
    def search_with_scores(self, query: str, top_n: int = 10) -> Tuple[pd.DataFrame, List[float]]:
        """
        Perform vector-based search and return results with scores.
        
        Args:
            query: Query string
            top_n: Number of top results to return
            
        Returns:
            Tuple of (DataFrame with results, list of scores)
        """
        if self.vocabulaire is None or self.docs_matrix is None:
            raise ValueError("Vectorizer data not loaded. Run vectorize.py first.")
        
        scores = self.vectorizer_search(query, self.vocabulaire, self.docs_matrix)
        order = list(np.argsort(-np.array(scores)))
        
        results = self.posts.iloc[order[:top_n]]
        top_scores = [scores[i] for i in order[:top_n]]
        
        return results, top_scores
    
    def get_vectorizer_stats(self) -> dict:
        """
        Get statistics about the vectorizer.
        
        Returns:
            Dictionary with vectorizer statistics
        """
        return {
            'vocabulaire_loaded': self.vocabulaire is not None,
            'docs_matrix_loaded': self.docs_matrix is not None,
            'vocabulary_size': len(self.vocabulaire) if self.vocabulaire is not None else 0,
            'num_documents': self.docs_matrix.shape[0] if self.docs_matrix is not None else 0
        } 