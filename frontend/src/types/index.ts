export interface SearchResult {
  id: number;
  title: string;
  body: string;
  parent_id: number | null;
  score: number;
  creation_date: string | null;
}

export interface SearchResponse {
  success: boolean;
  query: string;
  search_type: string;
  results: SearchResult[];
  total_results: number;
  execution_time: number;
  error?: string;
}

export interface PostResponse {
  success: boolean;
  post?: SearchResult;
  error?: string;
}

export interface StatsResponse {
  success: boolean;
  engine_stats?: {
    total_posts: number;
    total_topics: number;
    cuda_available: boolean;
    models_loaded: {
      question_model: boolean;
      answer_model: boolean;
      lda_model: boolean;
      vectorizer: boolean;
    };
  };
  embedding_stats?: {
    titles_embeddings_loaded: boolean;
    answer_embeddings_loaded: boolean;
    num_title_embeddings: number;
    num_answer_embeddings: number;
    question_model_loaded: boolean;
    answer_model_loaded: boolean;
  };
  clustering_stats?: {
    total_topics: number;
    total_documents: number;
    topic_sizes: Record<string, number>;
    avg_documents_per_topic: number;
    lda_model_loaded: boolean;
    vectorizer_loaded: boolean;
  };
  vector_stats?: {
    vocabulaire_loaded: boolean;
    docs_matrix_loaded: boolean;
    vocabulary_size: number;
    num_documents: number;
  };
  error?: string;
}

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  message?: string;
  error?: string;
  details?: {
    models_loaded: Record<string, boolean>;
    embeddings_loaded: {
      titles: boolean;
      answers: boolean;
    };
  };
}

export type SearchType = 'clustering' | 'semantic' | 'vector'; 