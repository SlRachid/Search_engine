import React, { useState } from 'react';
import { Search, Filter } from 'lucide-react';
import { SearchType } from '../types';

interface SearchBarProps {
  onSearch: (query: string, searchType: SearchType, topN: number) => void;
  isLoading: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');
  const [searchType, setSearchType] = useState<SearchType>('clustering');
  const [topN, setTopN] = useState(20);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), searchType, topN);
    }
  };

  const searchTypeOptions = [
    { value: 'clustering', label: 'Clustering', description: 'AI-powered topic clustering' },
    { value: 'semantic', label: 'Semantic', description: 'Meaning-based search' },
    { value: 'vector', label: 'Vector', description: 'Traditional keyword search' },
  ];

  return (
    <div className="w-full max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Main Search Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for anything... (e.g., 'how to learn AI', 'python programming', 'machine learning')"
            className="input-field pl-10 pr-4 text-lg"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !query.trim()}
            className="absolute inset-y-0 right-0 px-6 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white font-medium rounded-r-lg transition-colors duration-200"
          >
            {isLoading ? (
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
            ) : (
              'Search'
            )}
          </button>
        </div>

        {/* Advanced Options Toggle */}
        <div className="flex justify-center">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors duration-200"
          >
            <Filter className="h-4 w-4" />
            <span className="text-sm font-medium">
              {showAdvanced ? 'Hide' : 'Show'} Advanced Options
            </span>
          </button>
        </div>

        {/* Advanced Options */}
        {showAdvanced && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-gray-50 rounded-lg animate-slide-up">
            {/* Search Type Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Search Type
              </label>
              <div className="space-y-2">
                {searchTypeOptions.map((option) => (
                  <label key={option.value} className="flex items-start space-x-3 cursor-pointer">
                    <input
                      type="radio"
                      name="searchType"
                      value={option.value}
                      checked={searchType === option.value}
                      onChange={(e) => setSearchType(e.target.value as SearchType)}
                      className="mt-1 h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300"
                    />
                    <div>
                      <div className="text-sm font-medium text-gray-900">
                        {option.label}
                      </div>
                      <div className="text-xs text-gray-500">
                        {option.description}
                      </div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Results Count */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Results
              </label>
              <select
                value={topN}
                onChange={(e) => setTopN(Number(e.target.value))}
                className="input-field"
              >
                <option value={5}>5 results</option>
                <option value={10}>10 results</option>
                <option value={20}>20 results</option>
                <option value={50}>50 results</option>
                <option value={100}>100 results</option>
              </select>
            </div>
          </div>
        )}
      </form>
    </div>
  );
};

export default SearchBar; 