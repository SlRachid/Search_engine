import axios from 'axios';
import { SearchResponse, PostResponse, StatsResponse, HealthResponse, SearchType } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const searchAPI = {
  // Perform search
  search: async (
    query: string, 
    topN: number = 20, 
    searchType: SearchType = 'clustering'
  ): Promise<SearchResponse> => {
    const response = await api.get('/search', {
      params: {
        query,
        top_n: topN,
        search_type: searchType,
      },
    });
    return response.data;
  },

  // Get specific post
  getPost: async (postId: number): Promise<PostResponse> => {
    const response = await api.get(`/post/${postId}`);
    return response.data;
  },

  // Get engine statistics
  getStats: async (): Promise<StatsResponse> => {
    const response = await api.get('/stats');
    return response.data;
  },

  // Health check
  healthCheck: async (): Promise<HealthResponse> => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api; 