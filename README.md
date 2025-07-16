# AI Search Engine

A sophisticated, modular search engine that combines clustering, semantic search, and vector-based search capabilities. Features a modern React TypeScript frontend and a powerful Python backend API.

## 🚀 Quick Start

### One-Command Startup

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```cmd
start.bat
```

This will automatically:
- Install all dependencies
- Start the backend API on `http://localhost:8000`
- Start the frontend on `http://localhost:3000`
- Open the application in your browser

### Manual Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install Node.js dependencies:**
```bash
cd frontend
npm install
cd ..
```

3. **Start the backend:**
```bash
python backend/run_server.py
```

4. **Start the frontend (in a new terminal):**
```bash
cd frontend
npm start
```

5. **Open your browser:**
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

## 🏗️ Architecture

### Backend (Python)
```
backend/                        # API and web server
├── app/main.py                # FastAPI application
├── api/search_engine.py       # Search engine API interface
├── models/schemas.py          # Pydantic request/response models
├── utils/                     # Backend utilities
└── run_server.py              # Server startup script

src/                           # Core search engine logic
├── core/search_engine.py      # Main SearchEngine class
├── data/text_processor.py     # Text cleaning & preprocessing
├── models/
│   ├── embedding_manager.py   # Sentence transformer models
│   └── clustering_manager.py  # LDA topic modeling
├── search/
│   ├── semantic_search.py     # Semantic similarity
│   └── vector_search.py       # Vector-based search
└── utils/config.py            # Configuration management
```

### Frontend (React TypeScript)
```
frontend/
├── src/
│   ├── components/            # React components
│   │   ├── SearchBar.tsx      # Main search interface
│   │   ├── SearchResults.tsx  # Results display
│   │   └── StatusBar.tsx      # Engine status monitoring
│   ├── services/api.ts        # Backend communication
│   ├── types/index.ts         # TypeScript definitions
│   └── App.tsx                # Main application
├── package.json               # Dependencies
└── tailwind.config.js         # Styling configuration
```

## ✨ Features

### 🔍 Search Capabilities
- **AI Clustering**: Advanced topic clustering using LDA
- **Semantic Search**: Meaning-based search with transformer models
- **Vector Search**: Lightning-fast traditional keyword search

### 🎨 Frontend Features
- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Real-time Status**: Live engine health and statistics monitoring
- **Interactive Results**: Expandable search results with copy functionality
- **Mobile Responsive**: Works perfectly on all device sizes
- **TypeScript**: Full type safety and better development experience

### ⚡ Backend Features
- **Modular Architecture**: Clean separation of concerns
- **API Ready**: RESTful API with FastAPI
- **GPU Support**: Automatic CUDA acceleration
- **Configurable**: Flexible parameter adjustment
- **Health Monitoring**: Comprehensive status endpoints

## 📚 API Endpoints

### Search Endpoints
- `GET /search` - Perform search with query parameters
- `POST /search` - Perform search with JSON body
- `GET /search/clustering` - Clustering-based search
- `GET /search/semantic` - Semantic search
- `GET /search/vector` - Vector-based search

### Utility Endpoints
- `GET /health` - Engine health check
- `GET /stats` - Engine statistics
- `GET /post/{post_id}` - Get specific post

## 🛠️ Development

### Backend Development
```bash
# Run with auto-reload
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

# Run tests
python -m pytest

# Check code style
flake8 src/
```

### Frontend Development
```bash
cd frontend

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

## 📦 Dependencies

### Backend Dependencies
- **PyTorch**: Deep learning framework
- **Sentence Transformers**: Semantic embeddings
- **Scikit-learn**: Machine learning algorithms
- **FastAPI**: Web framework
- **Pandas**: Data manipulation
- **BeautifulSoup**: HTML parsing

### Frontend Dependencies
- **React 18**: UI framework
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Lucide React**: Icons
- **Axios**: HTTP client

## 🔧 Configuration

### Backend Configuration
```python
from src.utils.config import SearchConfig

config = SearchConfig(
    data_path="./data",
    coeff1=0.3,  # Semantic answer weight
    coeff2=0.2,  # Vector similarity weight
    coeff3=0.5,  # Title similarity weight
    batch_size=1024,
    default_top_n=20
)
```

### Frontend Configuration
Create `.env` file in `frontend/`:
```env
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Deployment

### Backend Deployment
```bash
# Build Docker image
docker build -t ai-search-engine .

# Run container
docker run -p 8000:8000 ai-search-engine
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy build/ directory to your web server
```

## 📊 Performance

- **Search Speed**: < 1 second for most queries
- **GPU Acceleration**: Automatic CUDA support
- **Batch Processing**: Memory-efficient operations
- **Caching**: Pre-computed embeddings and models

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🙏 Acknowledgments

- **Sentence Transformers** for semantic embeddings
- **Scikit-learn** for clustering algorithms
- **PyTorch** for deep learning capabilities
- **FastAPI** for the web framework
- **React** and **Tailwind CSS** for the frontend