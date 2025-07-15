# Migration Guide: From Monolithic to Modular Search Engine

This guide helps you transition from the old monolithic structure to the new modular architecture.

## Overview of Changes

### Old Structure (Monolithic)
```
├── search_engine.py          # Main monolithic file
├── Extract_Clean.py          # Text processing
├── embeddings.py             # Embedding management
├── clustering.py             # Topic clustering
├── semantic_search.py        # Semantic search
├── vectorize.py              # Vector processing
├── vectorize_search.py       # Vector search
└── Data_loading.py           # Data loading
```

### New Structure (Modular)
```
src/
├── core/
│   └── search_engine.py      # Main SearchEngine class
├── data/
│   └── text_processor.py     # Text processing (replaces Extract_Clean.py)
├── models/
│   ├── embedding_manager.py  # Embedding management (replaces embeddings.py)
│   └── clustering_manager.py # Topic clustering (replaces clustering.py)
├── search/
│   ├── semantic_search.py    # Semantic search
│   └── vector_search.py      # Vector search (replaces vectorize_search.py)
└── utils/
    └── config.py             # Configuration management (new)
api.py                        # API interface (new)
fastapi_example.py            # FastAPI example (new)
```

## Migration Steps

### Step 1: Update Imports

**Old Code:**
```python
from Extract_Clean import clean_post
from embeddings import load_embeddings_and_models
from clustering import get_topic_query, get_document_topics
from semantic_search import encode_query, order_similarity
```

**New Code:**
```python
from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig
from src.data.text_processor import TextProcessor
from src.models.embedding_manager import EmbeddingManager
from src.models.clustering_manager import ClusteringManager
from src.search.semantic_search import SemanticSearch
```

### Step 2: Replace Direct Function Calls

**Old Code:**
```python
# Direct function calls
posts = pickle.load(open('data/posts.pkl', 'rb'))
lda_model = pickle.load(open('data/lda_model.pkl', 'rb'))
vectorizer_lda = pickle.load(open('data/vectorizer_lda.pkl', 'rb'))

question_query_model, answer_query_model, embeddings_titles, embeddings_answer = load_embeddings_and_models()
topic_documents = get_document_topics()

# Search function
def search_engine_clustering(query, top_n=None):
    topic_query = get_topic_query(query, vectorizer_lda, lda_model)
    relevant_docs = topic_documents[topic_query]
    # ... rest of search logic
```

**New Code:**
```python
# Initialize with configuration
config = SearchConfig(data_path="./data")
search_engine = SearchEngine(config)

# Simple search call
results = search_engine.search(query, top_n=top_n)
```

### Step 3: Update Configuration

**Old Code:**
```python
# Hard-coded parameters
coeff1 = 0.3
coeff2 = 0.2
coeff3 = 0.5
batch_size = 1024
```

**New Code:**
```python
# Configurable parameters
config = SearchConfig(
    coeff1=0.3,
    coeff2=0.2,
    coeff3=0.5,
    batch_size=1024
)
```

### Step 4: Replace Search Types

**Old Code:**
```python
# Only clustering search available
result = search_engine_clustering(query, top_n=20)
```

**New Code:**
```python
# Multiple search types
clustering_results = search_engine.search(query, top_n=20)  # Default
semantic_results = search_engine.semantic_search(query, top_n=20)
vector_results = search_engine.vector_search(query, top_n=20)
```

## API Migration

### Old Usage Pattern
```python
# Direct script execution
if __name__ == "__main__":
    query = "how to learn AI"
    result = search_engine_clustering(query, top_n=20)
    print(result["Title"])
```

### New Usage Patterns

#### Option 1: Direct SearchEngine Usage
```python
from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig

config = SearchConfig()
search_engine = SearchEngine(config)
results = search_engine.search("how to learn AI", top_n=20)
print(results["Title"])
```

#### Option 2: API Interface Usage
```python
from api import SearchEngineAPI

api = SearchEngineAPI()
result = api.search("how to learn AI", top_n=20, search_type="clustering")
if result['success']:
    for post in result['results']:
        print(post['title'])
```

#### Option 3: FastAPI Backend
```python
# Run the FastAPI server
python fastapi_example.py

# Then make HTTP requests
import requests
response = requests.get("http://localhost:8000/search", params={
    "query": "how to learn AI",
    "top_n": 20,
    "search_type": "clustering"
})
results = response.json()
```

## Data Processing Migration

### Old Data Processing
```python
# Extract_Clean.py
def extract_data(datapath: str) -> pd.DataFrame:
    posts = pd.read_xml(os.path.join(datapath, 'Posts.xml'), parser="etree", encoding="utf8")
    posts['cleaned_body'] = posts.Body.fillna('').apply(clean_post)
    posts['cleaned_title'] = posts.Title.fillna('').apply(clean_post)
    return posts

# embeddings.py
def save_embeddings(model_name: str, savepath: str):
    # ... embedding generation code
```

### New Data Processing
```python
from src.data.text_processor import TextProcessor
from src.models.embedding_manager import EmbeddingManager
from src.utils.config import SearchConfig

# Text processing
processor = TextProcessor()
posts = processor.extract_data("./data")
processor.save_processed_data(posts, "./data")

# Embedding generation
config = SearchConfig()
embedding_manager = EmbeddingManager(config)
embedding_manager.save_embeddings(posts, "./data")
```

## Backward Compatibility

The modular version maintains backward compatibility for data files:
- `data/posts.pkl` - Processed posts data
- `data/lda_model.pkl` - LDA model
- `data/vectorizer_lda.pkl` - TF-IDF vectorizer
- `data/*-embeddings_*.pt` - Pre-computed embeddings

## Testing the Migration

1. **Run the example script:**
```bash
python example_usage.py
```

2. **Test the API:**
```bash
python api.py
```

3. **Test the FastAPI backend:**
```bash
python fastapi_example.py
```

4. **Compare results:**
```python
# Old way
from search_engine import search_engine_clustering
old_results = search_engine_clustering("test query", top_n=10)

# New way
from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig
config = SearchConfig()
search_engine = SearchEngine(config)
new_results = search_engine.search("test query", top_n=10)

# Results should be identical
assert len(old_results) == len(new_results)
```

## Benefits of Migration

1. **Modularity**: Each component is self-contained and testable
2. **Configurability**: Easy to adjust parameters without code changes
3. **Extensibility**: Simple to add new search types or models
4. **API Ready**: Built-in API interface for web applications
5. **Better Error Handling**: Comprehensive error handling and validation
6. **Documentation**: Full type hints and docstrings
7. **Testing**: Easier to write unit tests for individual components

## Troubleshooting

### Common Migration Issues

1. **Import Errors**: Make sure you're using the new import paths
2. **Missing Data Files**: Ensure all required pickle files are in the data directory
3. **Configuration Errors**: Check that SearchConfig parameters are valid
4. **CUDA Issues**: The new version automatically handles CUDA initialization

### Getting Help

If you encounter issues during migration:
1. Check the example scripts for correct usage patterns
2. Verify your data files are in the correct location
3. Test with the provided example scripts
4. Check the comprehensive README for detailed documentation 