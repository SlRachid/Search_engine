# Modular Search Engine

A sophisticated, modular search engine that combines clustering, semantic search, and vector-based search capabilities. This refactored version is designed to be easily integrated into backend APIs and frontend applications.

## Features

- **Multi-Modal Search**: Combines clustering, semantic, and vector-based search approaches
- **Topic Clustering**: Uses LDA (Latent Dirichlet Allocation) for document topic modeling
- **Semantic Search**: Leverages sentence transformers for semantic similarity
- **Vector Search**: Traditional TF-IDF and count vector-based search
- **Modular Architecture**: Clean separation of concerns for easy maintenance and extension
- **API Ready**: Simple interface that can be easily converted to REST APIs
- **CUDA Support**: GPU acceleration for faster processing
- **Configurable**: Flexible configuration system for different use cases

## Architecture

The search engine is organized into modular components:

```
src/
├── core/                    # Core search engine functionality
│   └── search_engine.py    # Main SearchEngine class
├── data/                   # Data processing
│   └── text_processor.py   # Text cleaning and preprocessing
├── models/                 # Model management
│   ├── embedding_manager.py    # Sentence transformer models
│   └── clustering_manager.py   # LDA topic modeling
├── search/                 # Search algorithms
│   ├── semantic_search.py      # Semantic similarity
│   └── vector_search.py        # Vector-based search
└── utils/                  # Utilities
    └── config.py          # Configuration management
```

## Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Search_engine
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Prepare your data**:
   - Place your XML data files in the `data/` directory
   - Run the data processing scripts to generate embeddings and models

## Quick Start

### Basic Usage

```python
from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig

# Create configuration
config = SearchConfig(data_path="./data")

# Initialize search engine
search_engine = SearchEngine(config)

# Perform a search
results = search_engine.search("how to learn AI", top_n=10)
print(results[['Title', 'Body']])
```

### Using the API Interface

```python
from api import SearchEngineAPI

# Initialize API
api = SearchEngineAPI()

# Perform different types of searches
clustering_results = api.search("python programming", search_type="clustering")
semantic_results = api.search("machine learning", search_type="semantic")
vector_results = api.search("data science", search_type="vector")

# Get specific post
post = api.get_post(post_id=12345)

# Get engine statistics
stats = api.get_stats()
```

### FastAPI Backend

Run the FastAPI example:

```bash
python fastapi_example.py
```

This starts a web server at `http://localhost:8000` with:
- Interactive API documentation at `/docs`
- Health check endpoint at `/health`
- Search endpoints at `/search`
- Post retrieval at `/post/{post_id}`

## Search Types

### 1. Clustering Search (Default)
Combines topic clustering with semantic similarity:
- Uses LDA to identify relevant topic clusters
- Applies semantic search within relevant clusters
- Combines title and content similarity scores
- Best for large document collections

### 2. Semantic Search
Pure semantic similarity using sentence transformers:
- Encodes query and documents using transformer models
- Computes cosine similarity between embeddings
- Best for understanding meaning and context

### 3. Vector Search
Traditional vector-based search:
- Uses TF-IDF and count vectors
- Computes cosine similarity between vectors
- Best for exact keyword matching

## Configuration

The `SearchConfig` class allows you to customize:

```python
from src.utils.config import SearchConfig

config = SearchConfig(
    data_path="./data",
    question_query_model_name="all-MiniLM-L6-v2",
    answer_query_model_name="multi-qa-mpnet-base-cos-v1",
    coeff1=0.3,  # Semantic answer weight
    coeff2=0.2,  # Vector similarity weight
    coeff3=0.5,  # Title similarity weight
    batch_size=1024,
    default_top_n=20
)
```

## Data Processing

### 1. Extract and Clean Data
```python
from src.data.text_processor import TextProcessor

processor = TextProcessor()
posts = processor.extract_data("./data")
processor.save_processed_data(posts, "./data")
```

### 2. Generate Embeddings
```python
from src.models.embedding_manager import EmbeddingManager
from src.utils.config import SearchConfig

config = SearchConfig()
embedding_manager = EmbeddingManager(config)
embedding_manager.save_embeddings(posts, "./data")
```

### 3. Train Clustering Models
```python
# This requires scikit-learn LDA implementation
# See clustering.py for details
```

## API Endpoints (FastAPI)

### Search Endpoints
- `POST /search` - Perform search with JSON body
- `GET /search?query=...&top_n=20&search_type=clustering` - GET search
- `GET /search/clustering?query=...` - Clustering search
- `GET /search/semantic?query=...` - Semantic search
- `GET /search/vector?query=...` - Vector search

### Utility Endpoints
- `GET /health` - Health check
- `GET /stats` - Engine statistics
- `GET /post/{post_id}` - Get specific post

## Performance Considerations

- **GPU Acceleration**: The engine automatically uses CUDA if available
- **Batch Processing**: Large operations are batched for memory efficiency
- **Caching**: Pre-computed embeddings and models are cached
- **Lazy Loading**: Components are loaded only when needed

## Extending the Engine

### Adding New Search Types
```python
class CustomSearch:
    def __init__(self, config):
        self.config = config
    
    def search(self, query, top_n=10):
        # Implement custom search logic
        pass

# Add to SearchEngine class
def custom_search(self, query, top_n=10):
    return self.custom_search.search(query, top_n)
```

### Adding New Models
```python
# Extend EmbeddingManager
def load_custom_model(self, model_name):
    # Load custom model
    pass
```

### Adding New Data Sources
```python
# Extend TextProcessor
def process_custom_data(self, data_source):
    # Process custom data format
    pass
```

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**: Reduce batch size in config
2. **Missing Data Files**: Ensure all required pickle files are in data directory
3. **Model Loading Errors**: Check if sentence transformer models are available

### Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license information here]

## Acknowledgments

- Sentence Transformers for semantic embeddings
- Scikit-learn for clustering algorithms
- PyTorch for deep learning capabilities