import React, { useState } from 'react';
import { Clock, MessageSquare, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';
import { SearchResult } from '../types';

interface SearchResultsProps {
  results: SearchResult[];
  query: string;
  searchType: string;
  executionTime: number;
  totalResults: number;
}

const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  query,
  searchType,
  executionTime,
  totalResults,
}) => {
  const [expandedResults, setExpandedResults] = useState<Set<number>>(new Set());

  const toggleResult = (id: number) => {
    const newExpanded = new Set(expandedResults);
    if (newExpanded.has(id)) {
      newExpanded.delete(id);
    } else {
      newExpanded.add(id);
    }
    setExpandedResults(newExpanded);
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Unknown date';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  const truncateText = (text: string, maxLength: number = 200) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getSearchTypeColor = (type: string) => {
    switch (type) {
      case 'clustering':
        return 'bg-blue-100 text-blue-800';
      case 'semantic':
        return 'bg-green-100 text-green-800';
      case 'vector':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSearchTypeLabel = (type: string) => {
    switch (type) {
      case 'clustering':
        return 'AI Clustering';
      case 'semantic':
        return 'Semantic Search';
      case 'vector':
        return 'Vector Search';
      default:
        return type;
    }
  };

  if (results.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-gray-500 text-lg">No results found for "{query}"</div>
        <div className="text-gray-400 text-sm mt-2">Try adjusting your search terms or search type</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search Summary */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600">
              Found {totalResults} results for "{query}"
            </span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSearchTypeColor(searchType)}`}>
              {getSearchTypeLabel(searchType)}
            </span>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Clock className="h-4 w-4" />
            <span>{executionTime.toFixed(3)}s</span>
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="space-y-4">
        {results.map((result, index) => (
          <div
            key={result.id}
            className="card hover:shadow-md transition-shadow duration-200 cursor-pointer"
            onClick={() => toggleResult(result.id)}
          >
            <div className="space-y-3">
              {/* Header */}
              <div className="flex items-start justify-between">
                <div className="flex-1 min-w-0">
                  <h3 className="text-lg font-semibold text-gray-900 hover:text-primary-600 transition-colors duration-200">
                    {result.title || 'Untitled'}
                  </h3>
                  <div className="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                    <span>ID: {result.id}</span>
                    {result.parent_id && <span>Parent: {result.parent_id}</span>}
                    <span>Score: {result.score.toFixed(3)}</span>
                    <span className="flex items-center space-x-1">
                      <Clock className="h-3 w-3" />
                      <span>{formatDate(result.creation_date)}</span>
                    </span>
                  </div>
                </div>
                <button className="ml-4 p-1 text-gray-400 hover:text-gray-600 transition-colors duration-200">
                  {expandedResults.has(result.id) ? (
                    <ChevronUp className="h-5 w-5" />
                  ) : (
                    <ChevronDown className="h-5 w-5" />
                  )}
                </button>
              </div>

              {/* Preview */}
              <div className="text-gray-700 leading-relaxed">
                {truncateText(result.body, expandedResults.has(result.id) ? 1000 : 200)}
              </div>

              {/* Expanded Content */}
              {expandedResults.has(result.id) && (
                <div className="animate-fade-in border-t pt-4 mt-4">
                  <div className="prose max-w-none">
                    <div className="text-gray-800 whitespace-pre-wrap">
                      {result.body}
                    </div>
                  </div>
                  <div className="flex items-center justify-between mt-4 pt-4 border-t">
                    <div className="flex items-center space-x-4 text-sm text-gray-500">
                      <span className="flex items-center space-x-1">
                        <MessageSquare className="h-4 w-4" />
                        <span>Full content displayed</span>
                      </span>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        // Copy to clipboard
                        navigator.clipboard.writeText(result.body);
                      }}
                      className="btn-secondary text-sm"
                    >
                      Copy Content
                    </button>
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex items-center justify-between pt-2 border-t">
                <div className="flex items-center space-x-2 text-sm text-gray-500">
                  <span>Result #{index + 1}</span>
                  <span>•</span>
                  <span>{result.body.length} characters</span>
                </div>
                <div className="flex items-center space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      window.open(`/post/${result.id}`, '_blank');
                    }}
                    className="flex items-center space-x-1 text-primary-600 hover:text-primary-700 text-sm font-medium transition-colors duration-200"
                  >
                    <ExternalLink className="h-4 w-4" />
                    <span>View Details</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SearchResults; 