"""
Clustering management for topic modeling and document organization.
"""

import pickle
import os
from collections import defaultdict
import pandas as pd
from typing import Dict, List, Any


class ClusteringManager:
    """
    Manages LDA topic modeling and document clustering.
    """
    
    def __init__(self, lda_model: Any, vectorizer: Any, posts: pd.DataFrame):
        """
        Initialize the clustering manager.
        
        Args:
            lda_model: Pre-trained LDA model
            vectorizer: Pre-trained TF-IDF vectorizer
            posts: DataFrame containing posts data
        """
        self.lda_model = lda_model
        self.vectorizer = vectorizer
        self.posts = posts
        self.topic_documents = None
        
        # Initialize topic documents mapping
        self._initialize_topic_documents()
    
    def _initialize_topic_documents(self):
        """Initialize the topic-documents mapping."""
        self.topic_documents = self.get_document_topics()
    
    def get_document_topics(self) -> Dict[int, List[int]]:
        """
        Get the mapping of topics to document IDs.
        
        Returns:
            Dictionary mapping topic IDs to lists of document IDs
        """
        # Transform documents using the vectorizer
        train_data = self.vectorizer.transform(self.posts.cleaned_body.values)
        
        # Get topic assignments for all documents
        topic_assignments = self.lda_model.transform(train_data)
        
        # Get top 3 most probable topics for each document
        most_probable_topics = []
        for sublist in topic_assignments:
            max_indices = sorted(enumerate(sublist), key=lambda x: x[1], reverse=True)[:3]
            most_probable_topics.append([index for index, _ in max_indices])
        
        # Create topic-documents mapping
        topic_documents = defaultdict(list)
        for i, document_id in enumerate(self.posts.Id.values):
            for j in range(3):
                topic_documents[most_probable_topics[i][j]].append(document_id)
        
        return dict(topic_documents)
    
    def get_topic_query(self, query: str) -> int:
        """
        Get the most probable topic for a query.
        
        Args:
            query: Query string
            
        Returns:
            Topic ID for the query
        """
        # Transform query using the vectorizer
        vector = self.vectorizer.transform([query])
        
        # Get topic assignments for the query
        topic_assignments = self.lda_model.transform(vector)
        
        # Get the most probable topic
        most_probable_topic = topic_assignments.argmax(axis=1)[0]
        
        return most_probable_topic
    
    def get_topics_for_document(self, document_id: int) -> List[int]:
        """
        Get the top topics for a specific document.
        
        Args:
            document_id: ID of the document
            
        Returns:
            List of topic IDs for the document
        """
        # Find the document in posts
        doc_mask = self.posts['Id'] == document_id
        if not doc_mask.any():
            return []
        
        doc_index = doc_mask.idxmax()
        doc_text = self.posts.loc[doc_index, 'cleaned_body']
        
        # Transform document using vectorizer
        vector = self.vectorizer.transform([doc_text])
        
        # Get topic assignments
        topic_assignments = self.lda_model.transform(vector)
        
        # Get top 3 most probable topics
        max_indices = sorted(enumerate(topic_assignments[0]), key=lambda x: x[1], reverse=True)[:3]
        return [index for index, _ in max_indices]
    
    def get_documents_for_topic(self, topic_id: int) -> List[int]:
        """
        Get all documents assigned to a specific topic.
        
        Args:
            topic_id: ID of the topic
            
        Returns:
            List of document IDs for the topic
        """
        return self.topic_documents.get(topic_id, [])
    
    def get_topic_stats(self) -> Dict:
        """
        Get statistics about topics and clustering.
        
        Returns:
            Dictionary with clustering statistics
        """
        topic_sizes = {topic_id: len(docs) for topic_id, docs in self.topic_documents.items()}
        
        return {
            'total_topics': len(self.topic_documents),
            'total_documents': len(self.posts),
            'topic_sizes': topic_sizes,
            'avg_documents_per_topic': sum(topic_sizes.values()) / len(topic_sizes) if topic_sizes else 0,
            'lda_model_loaded': self.lda_model is not None,
            'vectorizer_loaded': self.vectorizer is not None
        }
    
    def save_models(self, savepath: str):
        """
        Save LDA model and vectorizer to files.
        
        Args:
            savepath: Path to save the models
        """
        with open(os.path.join(savepath, 'lda_model.pkl'), 'wb') as f:
            pickle.dump(self.lda_model, f)
        
        with open(os.path.join(savepath, 'vectorizer_lda.pkl'), 'wb') as f:
            pickle.dump(self.vectorizer, f)
    
    def load_models(self, savepath: str):
        """
        Load LDA model and vectorizer from files.
        
        Args:
            savepath: Path to load the models from
        """
        with open(os.path.join(savepath, 'lda_model.pkl'), 'rb') as f:
            self.lda_model = pickle.load(f)
        
        with open(os.path.join(savepath, 'vectorizer_lda.pkl'), 'rb') as f:
            self.vectorizer = pickle.load(f) 