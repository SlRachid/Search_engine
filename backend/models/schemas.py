"""
Pydantic models for API request/response schemas.
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class SearchRequest(BaseModel):
    """Request model for search operations."""
    query: str
    top_n: Optional[int] = 20
    search_type: str = "clustering"  # "clustering", "semantic", "vector"


class SearchResponse(BaseModel):
    """Response model for search operations."""
    success: bool
    query: str
    search_type: str
    results: List[Dict[str, Any]]
    total_results: int
    execution_time: float
    error: Optional[str] = None


class PostResponse(BaseModel):
    """Response model for post retrieval."""
    success: bool
    post: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class StatsResponse(BaseModel):
    """Response model for statistics."""
    success: bool
    engine_stats: Optional[Dict[str, Any]] = None
    embedding_stats: Optional[Dict[str, Any]] = None
    clustering_stats: Optional[Dict[str, Any]] = None
    vector_stats: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Response model for health checks."""
    status: str
    message: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None 