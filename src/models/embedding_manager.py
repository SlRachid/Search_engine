"""
Embedding management for the search engine.
"""

import torch
import pandas as pd
import os
from sentence_transformers import SentenceTransformer
from typing import Dict, Tuple
from ..utils.config import SearchConfig


class EmbeddingManager:
    """
    Manages sentence transformer models and embeddings.
    """
    
    def __init__(self, config: SearchConfig):
        """
        Initialize the embedding manager.
        
        Args:
            config: SearchConfig object
        """
        self.config = config
        self.question_query_model = None
        self.answer_query_model = None
        self.embeddings_titles = {}
        self.embeddings_answer = {}
        
        self._load_models()
        self._load_embeddings()
    
    def _load_models(self):
        """Load sentence transformer models."""
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.question_query_model = SentenceTransformer(
            f'sentence-transformers/{self.config.question_query_model_name}', 
            device=device
        )
        
        self.answer_query_model = SentenceTransformer(
            f'sentence-transformers/{self.config.answer_query_model_name}', 
            device=device
        )
    
    def _load_embeddings(self):
        """Load pre-computed embeddings."""
        # Load title embeddings
        title_embeddings_path = os.path.join(
            self.config.data_path, 
            f'{self.config.question_query_model_name}-embeddings_titles_dict.pt'
        )
        if os.path.exists(title_embeddings_path):
            self.embeddings_titles = torch.load(title_embeddings_path)
        
        # Load answer embeddings
        answer_embeddings_path = os.path.join(
            self.config.data_path, 
            f'{self.config.answer_query_model_name}-embeddings_bodies_dict.pt'
        )
        if os.path.exists(answer_embeddings_path):
            self.embeddings_answer = torch.load(answer_embeddings_path)
    
    def save_embeddings(self, posts: pd.DataFrame, savepath: str):
        """
        Generate and save embeddings for posts.
        
        Args:
            posts: DataFrame containing posts data
            savepath: Path to save embeddings
        """
        # Clean posts data
        clean_posts = posts[['Id', 'Body', 'Title']].copy()
        clean_posts['Clean Body'] = clean_posts['Body'].fillna('').apply(self._remove_tags)
        clean_posts['Clean Title'] = clean_posts['Title'].fillna('').apply(self._remove_tags)
        
        # Generate embeddings for both models
        self._generate_embeddings_for_model(
            clean_posts, 
            self.question_query_model, 
            self.config.question_query_model_name,
            savepath,
            'titles'
        )
        
        self._generate_embeddings_for_model(
            clean_posts, 
            self.answer_query_model, 
            self.config.answer_query_model_name,
            savepath,
            'bodies'
        )
    
    def _generate_embeddings_for_model(self, clean_posts: pd.DataFrame, model: SentenceTransformer, 
                                     model_name: str, savepath: str, field: str):
        """
        Generate embeddings for a specific model and field.
        
        Args:
            clean_posts: Cleaned posts data
            model: Sentence transformer model
            model_name: Name of the model
            savepath: Path to save embeddings
            field: Field to embed ('titles' or 'bodies')
        """
        field_map = {'titles': 'Clean Title', 'bodies': 'Clean Body'}
        text_field = field_map[field]
        
        embeddings = []
        clean_texts = list(clean_posts[text_field])
        post_ids = list(clean_posts['Id'])
        batch_size = 10000
        
        print(f"Generating {field} embeddings with {model_name}...")
        
        for i in range(0, len(clean_texts), batch_size):
            batch_texts = clean_texts[i:i+batch_size]
            batch_embeddings = model.encode(
                batch_texts, 
                convert_to_tensor=True, 
                normalize_embeddings=True
            )
            embeddings.extend(batch_embeddings)
            print(f"Processed {i + len(batch_texts)}/{len(clean_texts)} documents", flush=True)
        
        # Save embeddings as dict with post ID as key
        embeddings_dict = dict(zip(post_ids, embeddings))
        torch.save(
            embeddings_dict, 
            os.path.join(savepath, f'{model_name}-embeddings_{field}_dict.pt')
        )
        
        print(f"Saved {field} embeddings to {savepath}")
    
    def _remove_tags(self, text: str) -> str:
        """
        Remove HTML tags from text.
        
        Args:
            text: Text with HTML tags
            
        Returns:
            Cleaned text
        """
        if not text or pd.isna(text):
            return ""
        
        text = text.replace('"', '')
        text = text.replace('\n', ' ')
        text = text.replace('<p>', '')
        text = text.replace('</p>', '')
        
        return text
    
    def encode_query(self, query: str, model: SentenceTransformer) -> torch.Tensor:
        """
        Encode a query using a sentence transformer model.
        
        Args:
            query: Query string
            model: Sentence transformer model to use
            
        Returns:
            Query embedding as tensor
        """
        return model.encode([query], normalize_embeddings=True, convert_to_tensor=True)
    
    def get_embeddings_stats(self) -> Dict:
        """
        Get statistics about loaded embeddings.
        
        Returns:
            Dictionary with embedding statistics
        """
        return {
            'titles_embeddings_loaded': len(self.embeddings_titles) > 0,
            'answer_embeddings_loaded': len(self.embeddings_answer) > 0,
            'num_title_embeddings': len(self.embeddings_titles),
            'num_answer_embeddings': len(self.embeddings_answer),
            'question_model_loaded': self.question_query_model is not None,
            'answer_model_loaded': self.answer_query_model is not None
        } 