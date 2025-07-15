import React, { useState } from 'react';
import { Brain, Zap, Search as SearchIcon } from 'lucide-react';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import StatusBar from './components/StatusBar';
import { SearchResult, SearchType } from './types';
import { searchAPI } from './services/api';

const App: React.FC = () => {
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [currentQuery, setCurrentQuery] = useState('');
  const [currentSearchType, setCurrentSearchType] = useState('');
  const [executionTime, setExecutionTime] = useState(0);
  const [totalResults, setTotalResults] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query: string, searchType: SearchType, topN: number) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);

    try {
      const response = await searchAPI.search(query, topN, searchType);
      
      if (response.success) {
        setSearchResults(response.results);
        setCurrentQuery(response.query);
        setCurrentSearchType(response.search_type);
        setExecutionTime(response.execution_time);
        setTotalResults(response.total_results);
      } else {
        setError(response.error || 'Search failed');
        setSearchResults([]);
      }
    } catch (err) {
      console.error('Search error:', err);
      setError('Failed to connect to search engine. Please check if the backend is running.');
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      icon: <Brain className="h-6 w-6" />,
      title: 'AI Clustering',
      description: 'Advanced topic clustering using LDA for intelligent document organization',
      color: 'text-blue-600',
    },
    {
      icon: <SearchIcon className="h-6 w-6" />,
      title: 'Semantic Search',
      description: 'Understand meaning and context using state-of-the-art transformer models',
      color: 'text-green-600',
    },
    {
      icon: <Zap className="h-6 w-6" />,
      title: 'Vector Search',
      description: 'Lightning-fast traditional keyword search with TF-IDF vectors',
      color: 'text-purple-600',
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">AI Search Engine</h1>
                <p className="text-sm text-gray-500">Advanced document search with AI</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                API Docs
              </a>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Hero Section */}
          {!hasSearched && (
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Discover Intelligent Search
              </h2>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Experience the power of AI-driven search with clustering, semantic understanding, 
                and lightning-fast vector search capabilities.
              </p>

              {/* Features Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                {features.map((feature, index) => (
                  <div
                    key={index}
                    className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200"
                  >
                    <div className={`${feature.color} mb-4`}>
                      {feature.icon}
                    </div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 text-sm">
                      {feature.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Search Section */}
          <div className="mb-8">
            <SearchBar onSearch={handleSearch} isLoading={isLoading} />
          </div>

          {/* Error Display */}
          {error && (
            <div className="mb-8 bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 text-red-800">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-sm font-medium">Search Error</h3>
                  <p className="text-sm mt-1">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Results Section */}
          {hasSearched && !isLoading && (
            <div className="animate-fade-in">
              <SearchResults
                results={searchResults}
                query={currentQuery}
                searchType={currentSearchType}
                executionTime={executionTime}
                totalResults={totalResults}
              />
            </div>
          )}

          {/* Loading State */}
          {isLoading && (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto mb-4"></div>
              <p className="text-gray-600">Searching through documents...</p>
              <p className="text-sm text-gray-500 mt-2">This may take a few seconds</p>
            </div>
          )}

          {/* Empty State */}
          {hasSearched && !isLoading && searchResults.length === 0 && !error && (
            <div className="text-center py-12">
              <div className="max-w-md mx-auto">
                <SearchIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your search terms or try a different search type.
                </p>
                <div className="space-y-2 text-sm text-gray-500">
                  <p>• Use more specific keywords</p>
                  <p>• Try semantic search for meaning-based results</p>
                  <p>• Use clustering search for topic-based results</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Status Bar */}
      <StatusBar />
    </div>
  );
};

export default App; 