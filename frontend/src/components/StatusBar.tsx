import React, { useEffect, useState } from 'react';
import { Activity, Server, Database, Cpu, CheckCircle, AlertCircle, XCircle } from 'lucide-react';
import { searchAPI } from '../services/api';
import { HealthResponse, StatsResponse } from '../types';

const StatusBar: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        setLoading(true);
        const [healthData, statsData] = await Promise.all([
          searchAPI.healthCheck(),
          searchAPI.getStats(),
        ]);
        setHealth(healthData);
        setStats(statsData);
        setError(null);
      } catch (err) {
        setError('Failed to fetch status');
        console.error('Status fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'degraded':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />;
      case 'unhealthy':
        return <XCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Activity className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-600';
      case 'degraded':
        return 'text-yellow-600';
      case 'unhealthy':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="bg-white border-t border-gray-200 px-4 py-2">
        <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
          <span>Checking engine status...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white border-t border-gray-200 px-4 py-2">
        <div className="flex items-center justify-center space-x-2 text-sm text-red-600">
          <XCircle className="h-4 w-4" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white border-t border-gray-200 px-4 py-2">
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center space-x-6">
          {/* Health Status */}
          <div className="flex items-center space-x-2">
            {getStatusIcon(health?.status || 'unknown')}
            <span className={`font-medium ${getStatusColor(health?.status || 'unknown')}`}>
              Engine: {health?.status || 'Unknown'}
            </span>
          </div>

          {/* Stats */}
          {stats?.success && stats.engine_stats && (
            <>
              <div className="flex items-center space-x-2 text-gray-600">
                <Database className="h-4 w-4" />
                <span>{stats.engine_stats.total_posts.toLocaleString()} posts</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <Server className="h-4 w-4" />
                <span>{stats.engine_stats.total_topics} topics</span>
              </div>
              <div className="flex items-center space-x-2 text-gray-600">
                <Cpu className="h-4 w-4" />
                <span>{stats.engine_stats.cuda_available ? 'GPU' : 'CPU'} mode</span>
              </div>
            </>
          )}
        </div>

        {/* Last Updated */}
        <div className="text-gray-500">
          Last updated: {new Date().toLocaleTimeString()}
        </div>
      </div>

      {/* Health Details */}
      {health?.details && (
        <div className="mt-2 pt-2 border-t border-gray-100">
          <div className="flex items-center space-x-4 text-xs text-gray-500">
            <div className="flex items-center space-x-1">
              <span>Models:</span>
              {Object.entries(health.details.models_loaded).map(([model, loaded]) => (
                <span
                  key={model}
                  className={`px-1 rounded ${
                    loaded ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}
                >
                  {model}
                </span>
              ))}
            </div>
            <div className="flex items-center space-x-1">
              <span>Embeddings:</span>
              {Object.entries(health.details.embeddings_loaded).map(([type, loaded]) => (
                <span
                  key={type}
                  className={`px-1 rounded ${
                    loaded ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                  }`}
                >
                  {type}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default StatusBar; 