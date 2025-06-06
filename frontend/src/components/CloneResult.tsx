import React, { useState, useEffect } from 'react';
import { CloneStatus, ErrorResponse } from '../app/types';

interface CloneResultProps {
  jobId: string;
}

export default function CloneResult({ jobId }: CloneResultProps) {
  const [status, setStatus] = useState<CloneStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showCode, setShowCode] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [viewMode, setViewMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch(`http://localhost:8000/clone/${jobId}`);
        if (!response.ok) {
          const errorData = await response.json() as ErrorResponse;
          throw new Error(errorData.detail || 'Failed to fetch status');
        }
        const data = await response.json() as CloneStatus;
        setStatus(data);

        // Continue polling if not completed or failed
        if (data.status !== 'completed' && data.status !== 'failed') {
          setTimeout(checkStatus, 1000);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      }
    };

    checkStatus();
  }, [jobId]);

  const getProgressColor = (): string => {
    if (!status) return 'bg-gray-500';
    if (status.status === 'failed') return 'bg-red-500';
    if (status.status === 'completed') return 'bg-green-500';
    return 'bg-blue-500';
  };

  const getStatusIcon = (): string => {
    if (!status) return '⏳';
    switch (status.status) {
      case 'pending':
        return '⏳';
      case 'initializing':
        return '🔧';
      case 'scraping':
        return '🔍';
      case 'generating':
        return '🤖';
      case 'completed':
        return '✅';
      case 'failed':
        return '❌';
      default:
        return '⏳';
    }
  };

  if (!status) {
    return (
      <div className="space-y-6">
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <span className="text-2xl">⏳</span>
              <div>
                <h3 className="font-semibold text-gray-800 dark:text-white">
                  Loading...
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">Fetching status...</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Progress Section */}
      <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-2xl">{getStatusIcon()}</span>
            <div>
              <h3 className="font-semibold text-gray-800 dark:text-white">
                {status.status.charAt(0).toUpperCase() + status.status.slice(1)}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">{status.message}</p>
            </div>
          </div>
          <span className="text-lg font-semibold text-gray-700 dark:text-gray-300">
            {status.progress}%
          </span>
        </div>
        
        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
          <div
            className={`h-full transition-all duration-500 ease-out ${getProgressColor()}`}
            style={{ width: `${status.progress}%` }}
          />
        </div>
      </div>

      {/* Result Section */}
      {status.status === 'completed' && (
        <>
          <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow-lg">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-semibold text-gray-800 dark:text-white">
                Generated Website
              </h3>
              <div className="flex space-x-2">
                <button
                  onClick={() => setShowCode(!showCode)}
                  className="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                >
                  {showCode ? 'Hide Code' : 'Show Code'}
                </button>
                <button
                  onClick={() => setIsFullscreen(!isFullscreen)}
                  className="px-4 py-2 text-sm font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                >
                  {isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'}
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
                <h4 className="font-semibold text-blue-700 dark:text-blue-300 mb-2">
                  ℹ️ Clone Information
                </h4>
                <p className="text-sm text-blue-600 dark:text-blue-400">
                  Successfully cloned with AI-powered design analysis. The HTML includes all styles and scripts inline for easy deployment.
                </p>
              </div>
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
                <h4 className="font-semibold text-green-700 dark:text-green-300 mb-2">
                  🚀 Next Steps
                </h4>
                <p className="text-sm text-green-600 dark:text-green-400">
                  Download the HTML file and host it on any web server, or copy the code to customize it further.
                </p>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Error State */}
      {status.status === 'failed' && (
        <div className="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg">
          <h3 className="text-xl font-semibold text-red-700 dark:text-red-300 mb-2">
            Cloning Failed
          </h3>
          <p className="text-red-600 dark:text-red-400">{status.error || 'An unknown error occurred'}</p>
          <p className="text-sm text-red-500 dark:text-red-500 mt-2">
            Please try again with a different URL or check if the website is accessible.
          </p>
        </div>
      )}
    </div>
  );
} 