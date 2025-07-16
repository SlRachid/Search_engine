"""
Simple API interface for the search engine.
This can be easily extended to a full FastAPI or Flask backend.
"""

import time
from typing import Dict, List, Optional, Any
import pandas as pd

from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig


class SearchEngineAPI:
    """
    API interface for the search engine.
    """
    
    def __init__(self, config: Optional[SearchConfig] = None):
        """
        Initialize the search engine API.
        
        Args:
            config: Optional SearchConfig. If None, uses default config.
        """
        if config is None:
            config = SearchConfig()
        
        self.config = config
        self.search_engine = SearchEngine(config)
    
    def search(self, query: str, top_n: Optional[int] = None, 
               search_type: str = "clustering") -> Dict[str, Any]:
        """
        Perform a search.
        
        Args:
            query: Search query
            top_n: Maximum number of results
            search_type: Type of search ("clustering", "semantic", "vector")
            
        Returns:
            Dictionary with search results and metadata
        """
        start_time = time.time()
        
        try:
            if search_type == "clustering":
                results = self.search_engine.search(query, top_n)
            elif search_type == "semantic":
                results = self.search_engine.semantic_search(query, top_n or self.config.default_top_n)
            elif search_type == "vector":
                results = self.search_engine.vector_search(query, top_n or self.config.default_top_n)
            else:
                raise ValueError(f"Unknown search type: {search_type}")
            
            # Convert results to list of dictionaries
            results_list = []
            for _, row in results.iterrows():
                result_dict = {
                    'id': int(row['Id']),
                    'title': str(row['Title']) if pd.notna(row['Title']) else "",
                    'body': str(row['Body']) if pd.notna(row['Body']) else "",
                    'parent_id': int(row['ParentId']) if pd.notna(row['ParentId']) else None,
                    'score': float(row.get('Score', 0)) if pd.notna(row.get('Score', 0)) else 0,
                    'creation_date': str(row['CreationDate']) if pd.notna(row['CreationDate']) else None
                }
                results_list.append(result_dict)
            
            return {
                'success': True,
                'query': query,
                'search_type': search_type,
                'results': results_list,
                'total_results': len(results_list),
                'execution_time': time.time() - start_time
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': query,
                'search_type': search_type,
                'execution_time': time.time() - start_time
            }
    
    def get_post(self, post_id: int) -> Dict[str, Any]:
        """
        Get a specific post by ID.
        
        Args:
            post_id: Post ID
            
        Returns:
            Dictionary with post data
        """
        try:
            post = self.search_engine.get_post_by_id(post_id)
            
            if post is None:
                return {
                    'success': False,
                    'error': f'Post with ID {post_id} not found'
                }
            
            return {
                'success': True,
                'post': {
                    'id': int(post['Id']),
                    'title': str(post['Title']) if pd.notna(post['Title']) else "",
                    'body': str(post['Body']) if pd.notna(post['Body']) else "",
                    'parent_id': int(post['ParentId']) if pd.notna(post['ParentId']) else None,
                    'score': float(post.get('Score', 0)) if pd.notna(post.get('Score', 0)) else 0,
                    'creation_date': str(post['CreationDate']) if pd.notna(post['CreationDate']) else None
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get search engine statistics.
        
        Returns:
            Dictionary with engine statistics
        """
        try:
            engine_stats = self.search_engine.get_stats()
            embedding_stats = self.search_engine.embedding_manager.get_embeddings_stats()
            clustering_stats = self.search_engine.clustering_manager.get_topic_stats()
            vector_stats = self.search_engine.vector_search.get_vectorizer_stats()
            
            return {
                'success': True,
                'engine_stats': engine_stats,
                'embedding_stats': embedding_stats,
                'clustering_stats': clustering_stats,
                'vector_stats': vector_stats
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the search engine.
        
        Returns:
            Dictionary with health status
        """
        try:
            stats = self.get_stats()
            
            if not stats['success']:
                return {
                    'status': 'unhealthy',
                    'error': stats['error']
                }
            
            # Check if all components are loaded
            engine_stats = stats['engine_stats']
            embedding_stats = stats['embedding_stats']
            
            all_models_loaded = all(engine_stats['models_loaded'].values())
            embeddings_loaded = (embedding_stats['titles_embeddings_loaded'] and 
                               embedding_stats['answer_embeddings_loaded'])
            
            if all_models_loaded and embeddings_loaded:
                return {
                    'status': 'healthy',
                    'message': 'All components loaded successfully'
                }
            else:
                return {
                    'status': 'degraded',
                    'message': 'Some components not loaded',
                    'details': {
                        'models_loaded': engine_stats['models_loaded'],
                        'embeddings_loaded': {
                            'titles': embedding_stats['titles_embeddings_loaded'],
                            'answers': embedding_stats['answer_embeddings_loaded']
                        }
                    }
                }
                
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e)
            } 