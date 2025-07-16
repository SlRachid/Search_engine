# Search Engine Backend

This directory contains the backend API for the search engine, built with FastAPI.

## Structure

```
backend/
├── app/
│   ├── __init__.py
│   └── main.py              # FastAPI application
├── api/
│   ├── __init__.py
│   └── search_engine.py     # Search engine API interface
├── models/
│   ├── __init__.py
│   └── schemas.py           # Pydantic models
├── utils/
│   └── __init__.py          # Backend utilities
├── requirements.txt         # Backend dependencies
├── run_server.py           # Server startup script
└── README.md               # This file
```

## Setup

1. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```

2. Make sure you have the main project dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

### Option 1: Using the run script
```bash
python backend/run_server.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Option 3: Using the main app file
```bash
python backend/app/main.py
```

## API Endpoints

Once the server is running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Root**: http://localhost:8000/

### Available Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /stats` - Search engine statistics
- `POST /search` - Perform search (JSON body)
- `GET /search` - Perform search (query parameters)
- `GET /post/{post_id}` - Get specific post
- `GET /search/clustering` - Clustering-based search
- `GET /search/semantic` - Semantic search
- `GET /search/vector` - Vector-based search

## Development

The backend is organized with a clean separation of concerns:

- **API Layer** (`api/`): Business logic and search engine interface
- **Models** (`models/`): Pydantic schemas for request/response validation
- **App** (`app/`): FastAPI application and route definitions
- **Utils** (`utils/`): Backend-specific utilities

## CORS Configuration

The API is configured with CORS middleware to allow cross-origin requests. In production, you should configure the `allow_origins` parameter to only allow specific domains. 