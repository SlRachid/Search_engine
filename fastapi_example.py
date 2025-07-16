"""
FastAPI example showing how to convert the search engine to a full web backend.
This is an example of how you can easily extend the modular search engine.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn

from api import SearchEngineAPI
from src.utils.config import SearchConfig


# Pydantic models for request/response
class SearchRequest(BaseModel):
    query: str
    top_n: Optional[int] = 20
    search_type: str = "clustering"  # "clustering", "semantic", "vector"


class SearchResponse(BaseModel):
    success: bool
    query: str
    search_type: str
    results: List[Dict[str, Any]]
    total_results: int
    execution_time: float
    error: Optional[str] = None


class PostResponse(BaseModel):
    success: bool
    post: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class StatsResponse(BaseModel):
    success: bool
    engine_stats: Optional[Dict[str, Any]] = None
    embedding_stats: Optional[Dict[str, Any]] = None
    clustering_stats: Optional[Dict[str, Any]] = None
    vector_stats: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    message: Optional[str] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


# Initialize FastAPI app
app = FastAPI(
    title="Search Engine API",
    description="A modular search engine API with clustering, semantic, and vector search capabilities",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize search engine API
search_api = SearchEngineAPI()


@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Search Engine API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    health = search_api.health_check()
    return HealthResponse(**health)


@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Get search engine statistics."""
    stats = search_api.get_stats()
    return StatsResponse(**stats)


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """Perform a search."""
    if request.search_type not in ["clustering", "semantic", "vector"]:
        raise HTTPException(
            status_code=400,
            detail="search_type must be one of: clustering, semantic, vector"
        )

    result = search_api.search(
        query=request.query,
        top_n=request.top_n,
        search_type=request.search_type
    )

    return SearchResponse(**result)


@app.get("/search", response_model=SearchResponse)
async def search_get(
    query: str = Query(..., description="Search query"),
    top_n: Optional[int] = Query(20, description="Maximum number of results"),
    search_type: str = Query("clustering", description="Type of search")
):
    """Perform a search using GET method."""
    if search_type not in ["clustering", "semantic", "vector"]:
        raise HTTPException(
            status_code=400,
            detail="search_type must be one of: clustering, semantic, vector"
        )

    result = search_api.search(
        query=query,
        top_n=top_n,
        search_type=search_type
    )

    return SearchResponse(**result)


@app.get("/post/{post_id}", response_model=PostResponse)
async def get_post(post_id: int):
    """Get a specific post by ID."""
    result = search_api.get_post(post_id)
    return PostResponse(**result)


@app.get("/search/clustering", response_model=SearchResponse)
async def clustering_search(
    query: str = Query(..., description="Search query"),
    top_n: Optional[int] = Query(20, description="Maximum number of results")
):
    """Perform clustering-based search."""
    result = search_api.search(
        query=query,
        top_n=top_n,
        search_type="clustering"
    )

    return SearchResponse(**result)


@app.get("/search/semantic", response_model=SearchResponse)
async def semantic_search(
    query: str = Query(..., description="Search query"),
    top_n: Optional[int] = Query(20, description="Maximum number of results")
):
    """Perform semantic search."""
    result = search_api.search(
        query=query,
        top_n=top_n,
        search_type="semantic"
    )

    return SearchResponse(**result)


# @app.get("/search/vector", response_model=SearchResponse)
# async def vector_search(
#     query: str = Query(..., description="Search query"),
#     top_n: Optional[int] = Query(20, description="Maximum number of results")
# ):
#     """Perform vector-based search."""
#     result = search_api.search(
#         query=query,
#         top_n=top_n,
#         search_type="vector"
#     )

#     return SearchResponse(**result)


if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(
        "fastapi_example:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
