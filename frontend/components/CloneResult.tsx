'use client';

import { useState, useEffect } from 'react';
import { CloneJob, CloneStatus } from '../src/app/types';

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
          throw new Error('Failed to fetch status');
        }
        const data: CloneStatus = await response.json();
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

  const getProgressColor = () => {
    if (status?.status === 'failed') return 'bg-red-500';
    if (status?.status === 'completed') return 'bg-green-500';
    return 'bg-blue-500';
  };

  const getStatusIcon = () => {
    switch (status?.status) {
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

  const downloadHTML = () => {
    if (!status?.html) return;
    
    const blob = new Blob([status.html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cloned-website.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const copyToClipboard = async () => {
    if (!status?.html) return;
    
    try {
      await navigator.clipboard.writeText(status.html);
      alert('HTML copied to clipboard!');
    } catch (err) {
      alert('Failed to copy to clipboard');
    }
  };

  const getViewportDimensions = () => {
    switch (viewMode) {
      case 'mobile':
        return { width: '375px', height: '667px' };
      case 'tablet':
        return { width: '768px', height: '1024px' };
      default:
        return { width: '100%', height: '100%' };
    }
  };

  if (error) {
    return (
      <div className="p-6 bg-red-50 dark:bg-red-900/20 rounded-lg">
        <p className="text-red-600 dark:text-red-400">Error: {error}</p>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full"></div>
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
      {status.status === 'completed' && status.html && (
        <>
          {/* Controls */}
          <div className="flex flex-wrap gap-4 justify-between items-center">
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('desktop')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  viewMode === 'desktop'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                }`}
              >
                💻 Desktop
              </button>
              <button
                onClick={() => setViewMode('tablet')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  viewMode === 'tablet'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                }`}
              >
                📱 Tablet
              </button>
              <button
                onClick={() => setViewMode('mobile')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  viewMode === 'mobile'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600'
                }`}
              >
                📱 Mobile
              </button>
            </div>
            
            <div className="flex gap-2">
              <button
                onClick={() => setShowCode(!showCode)}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                {showCode ? '👁️ Preview' : '</> Code'}
              </button>
              <button
                onClick={() => setIsFullscreen(!isFullscreen)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                {isFullscreen ? '🗗 Exit' : '⛶ Fullscreen'}
              </button>
              <button
                onClick={copyToClipboard}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                📋 Copy
              </button>
              <button
                onClick={downloadHTML}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                ⬇️ Download
              </button>
            </div>
          </div>

          {/* Preview/Code View */}
          <div className={`transition-all duration-300 ${
            isFullscreen 
              ? 'fixed inset-0 z-50 bg-white dark:bg-gray-900 p-4' 
              : 'relative'
          }`}>
            {isFullscreen && (
              <button
                onClick={() => setIsFullscreen(false)}
                className="absolute top-4 right-4 z-10 px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700"
              >
                ✕ Close
              </button>
            )}
            
            <div className={`${
              isFullscreen ? 'h-full' : 'h-[600px]'
            } bg-white dark:bg-gray-800 rounded-lg shadow-2xl overflow-hidden`}>
              {showCode ? (
                <div className="h-full overflow-auto p-4 bg-gray-900">
                  <pre className="text-sm text-gray-300">
                    <code>{formatHTML(status.html)}</code>
                  </pre>
                </div>
              ) : (
                <div className="h-full flex justify-center items-center bg-gray-100 dark:bg-gray-900 p-4">
                  <div
                    className={`bg-white shadow-2xl transition-all duration-300 ${
                      viewMode !== 'desktop' ? 'border-8 border-gray-800 rounded-xl' : ''
                    }`}
                    style={getViewportDimensions()}
                  >
                    <iframe
                      srcDoc={status.html}
                      className="w-full h-full"
                      title="Cloned Website Preview"
                      sandbox="allow-scripts"
                    />
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Additional Info */}
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

// Helper function to format HTML with basic indentation
function formatHTML(html: string): string {
  // Basic HTML formatting for better readability
  let formatted = html;
  let indent = 0;
  
  formatted = formatted.replace(/></g, '>\n<');
  const lines = formatted.split('\n');
  
  const formattedLines = lines.map(line => {
    const trimmed = line.trim();
    
    if (trimmed.startsWith('</')) {
      indent = Math.max(0, indent - 1);
    }
    
    const indented = '  '.repeat(indent) + trimmed;
    
    if (trimmed.startsWith('<') && !trimmed.startsWith('</') && 
        !trimmed.endsWith('/>') && !trimmed.includes('</')) {
      indent++;
    }
    
    return indented;
  });
  
  return formattedLines.join('\n');
}