'use client';

import { useState } from 'react';
import CloneForm from '../components/CloneForm';
import CloneResult from '../components/CloneResult';
import LoadingSpinner from '../components/LoadingSpinner';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { CloneJob } from './types';

export default function Home() {
  const [activeJob, setActiveJob] = useState<CloneJob | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCloneStart = (job: CloneJob): void => {
    setActiveJob(job);
    setError(null);
  };

  const handleError = (errorMessage: string): void => {
    setError(errorMessage);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      <Header />
      
      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              AI Website Cloner
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Clone any website's design instantly with advanced AI technology
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 mb-8">
            <CloneForm 
              onJobStart={handleCloneStart}
              onError={handleError}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
            
            {error && (
              <div className="mt-6 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
                <p className="text-red-600 dark:text-red-400">{error}</p>
              </div>
            )}
          </div>

          {activeJob && (
            <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8">
              <CloneResult jobId={activeJob.id} />
            </div>
          )}

          {!activeJob && !isLoading && (
            <div className="grid md:grid-cols-3 gap-6 mt-12">
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                <div className="text-4xl mb-4">🎨</div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Smart Analysis</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  AI analyzes color schemes, layouts, and design patterns
                </p>
              </div>
              
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                <div className="text-4xl mb-4">⚡</div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Lightning Fast</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  Get your cloned website in seconds, not hours
                </p>
              </div>
              
              <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                <div className="text-4xl mb-4">📱</div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800 dark:text-white">Responsive</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  All clones are mobile-friendly and responsive by default
                </p>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
}