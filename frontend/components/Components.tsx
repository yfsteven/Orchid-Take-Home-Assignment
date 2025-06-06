// components/Header.tsx
export function Header() {
  return (
    <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="text-2xl">🌐</div>
            <div>
              <h1 className="text-xl font-bold text-gray-800 dark:text-white">
                Orchids Web Cloner
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                AI-Powered Website Design Replication
              </p>
            </div>
          </div>
          <nav className="hidden md:flex space-x-6">
            <a href="#" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
              How it Works
            </a>
            <a href="#" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
              API
            </a>
            <a href="#" className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors">
              About
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
}

// components/Footer.tsx
export function Footer() {
  return (
    <footer className="bg-gray-100 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-700 mt-auto">
      <div className="container mx-auto px-4 py-8">
        <div className="grid md:grid-cols-3 gap-8">
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-3">About</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Advanced AI-powered website cloning technology that analyzes and recreates web designs with precision.
            </p>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Technology</h3>
            <ul className="text-sm text-gray-600 dark:text-gray-400 space-y-2">
              <li>• Claude AI Integration</li>
              <li>• Advanced Web Scraping</li>
              <li>• Cloud Browser Support</li>
              <li>• Responsive Design Analysis</li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-3">Contact</h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Orchids Technology<br />
              kevinlu@orchids.app
            </p>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700 text-center">
          <p className="text-sm text-gray-500 dark:text-gray-500">
            © 2024 Orchids Technology. Built for the SWE Internship Challenge.
          </p>
        </div>
      </div>
    </footer>
  );
}

// components/LoadingSpinner.tsx
export function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="relative">
        <div className="animate-spin h-12 w-12 border-4 border-blue-500 border-t-transparent rounded-full"></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-6 w-6 bg-blue-500 rounded-full animate-pulse"></div>
        </div>
      </div>
    </div>
  );
}