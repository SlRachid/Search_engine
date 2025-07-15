"""
Configuration management for the search engine.
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class SearchConfig:
    """
    Configuration class for the search engine.
    """
    
    # Paths
    data_path: str = "./data"
    main_path: str = "."
    
    # Model names
    question_query_model_name: str = "all-MiniLM-L6-v2"
    answer_query_model_name: str = "multi-qa-mpnet-base-cos-v1"
    
    # Search coefficients
    coeff1: float = 0.3  # Semantic answer similarity weight
    coeff2: float = 0.2  # Vector similarity weight (currently unused)
    coeff3: float = 0.5  # Title similarity weight
    
    # Batch processing
    batch_size: int = 1024
    
    # Search parameters
    default_top_n: int = 20
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not os.path.exists(self.data_path):
            raise ValueError(f"Data path does not exist: {self.data_path}")
        
        if not (0 <= self.coeff1 <= 1):
            raise ValueError("coeff1 must be between 0 and 1")
        
        if not (0 <= self.coeff2 <= 1):
            raise ValueError("coeff2 must be between 0 and 1")
        
        if not (0 <= self.coeff3 <= 1):
            raise ValueError("coeff3 must be between 0 and 1")
        
        # Normalize coefficients to sum to 1
        total = self.coeff1 + self.coeff2 + self.coeff3
        if total != 1.0:
            self.coeff1 /= total
            self.coeff2 /= total
            self.coeff3 /= total


def create_default_config() -> SearchConfig:
    """
    Create a default configuration.
    
    Returns:
        SearchConfig with default values
    """
    return SearchConfig()


def create_config_from_dict(config_dict: dict) -> SearchConfig:
    """
    Create a configuration from a dictionary.
    
    Args:
        config_dict: Dictionary containing configuration parameters
        
    Returns:
        SearchConfig object
    """
    return SearchConfig(**config_dict) 