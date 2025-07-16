#!/usr/bin/env python3
"""
Script to run the FastAPI server for the search engine backend.
"""

import uvicorn
import sys
import os

# Add the parent directory to the Python path to import src modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.main import app

if __name__ == "__main__":
    print("Starting Search Engine API server...")
    print("API documentation available at: http://localhost:8000/docs")
    print("Health check available at: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 