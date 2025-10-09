'use client';

import { useState } from 'react';

export default function Home() {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch(`http://localhost:8000/research?query=${encodeURIComponent(query)}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error('Research request failed');
      }

      const data = await response.json();
      
      // Check if the response indicates success
      if (!data.success) {
        throw new Error(data.error || 'Research failed');
      }
      
      setResult(data.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-black">
      {/* Header */}
      <header className="border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-black rounded-lg flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold">Web Research Assistant</h1>
              <p className="text-sm text-gray-600">AI-powered comprehensive research tool</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Search Section */}
        <div className="mb-12">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="query" className="block text-sm font-medium mb-2">
                Research Query
              </label>
              <div className="relative">
                <input
                  id="query"
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Enter your research topic or question..."
                  className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-black transition-colors"
                  disabled={loading}
                />
              </div>
            </div>
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="w-full sm:w-auto px-8 py-3 bg-black text-white rounded-lg font-medium hover:bg-gray-800 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Researching...
                </span>
              ) : (
                'Start Research'
              )}
            </button>
          </form>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-8 p-4 bg-gray-100 border-l-4 border-black rounded">
            <div className="flex items-start gap-3">
              <svg className="w-5 h-5 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <div>
                <h3 className="font-semibold">Error</h3>
                <p className="text-sm text-gray-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="space-y-6">
            <div className="border border-gray-200 rounded-lg p-6">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-2 h-2 bg-black rounded-full animate-pulse"></div>
                <h2 className="text-lg font-semibold">Processing your research...</h2>
              </div>
              <div className="space-y-3">
                <div className="h-4 bg-gray-100 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-100 rounded animate-pulse w-5/6"></div>
                <div className="h-4 bg-gray-100 rounded animate-pulse w-4/6"></div>
              </div>
            </div>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-8">
            {/* Stats Bar */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-2xl font-bold">{result.sources_found || 0}</div>
                <div className="text-sm text-gray-600">Sources Found</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-2xl font-bold">{result.pages_processed || 0}</div>
                <div className="text-sm text-gray-600">Pages Processed</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-2xl font-bold">{result.summaries_generated || 0}</div>
                <div className="text-sm text-gray-600">Summaries</div>
              </div>
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="text-2xl font-bold">{Math.ceil((result.report_length || 0) / 1000)}k</div>
                <div className="text-sm text-gray-600">Characters</div>
              </div>
            </div>

            {/* Research Report */}
            <div className="border border-gray-200 rounded-lg">
              <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
                <h2 className="text-xl font-bold">Research Report</h2>
                <p className="text-sm text-gray-600 mt-1">Query: {result.query}</p>
              </div>
              <div className="p-6">
                <div className="prose prose-sm max-w-none">
                  {result.report ? (
                    <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                      {result.report}
                    </div>
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <p className="mb-2">⚠️ Report generation incomplete</p>
                      <p className="text-sm">The research workflow may have encountered an issue. Check the backend logs for details.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Citations */}
            {result.citations && result.citations.length > 0 && (
              <div className="border border-gray-200 rounded-lg">
                <div className="border-b border-gray-200 bg-gray-50 px-6 py-4">
                  <h2 className="text-xl font-bold">Citations & Sources</h2>
                  <p className="text-sm text-gray-600 mt-1">{result.citations.length} sources referenced</p>
                </div>
                <div className="p-6">
                  <div className="space-y-4">
                    {result.citations.map((citation: any) => (
                      <div key={citation.id} className="border-l-2 border-black pl-4">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-mono text-sm font-semibold">[{citation.id}]</span>
                              <h3 className="font-medium">{citation.title}</h3>
                            </div>
                            <a
                              href={citation.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-sm text-gray-600 hover:text-black hover:underline break-all"
                            >
                              {citation.url}
                            </a>
                            <p className="text-xs text-gray-500 mt-1">
                              Accessed: {citation.access_date}
                            </p>
                          </div>
                          {citation.relevance_score && (
                            <div className="text-xs font-mono bg-gray-100 px-2 py-1 rounded">
                              {(citation.relevance_score * 100).toFixed(0)}%
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Timestamp */}
            {result.timestamp && (
              <div className="text-center text-sm text-gray-500">
                Research completed at {result.timestamp}
              </div>
            )}
          </div>
        )}

        {/* Empty State */}
        {!result && !loading && !error && (
          <div className="text-center py-12">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h3 className="text-lg font-semibold mb-2">Ready to Research</h3>
            <p className="text-gray-600 max-w-md mx-auto">
              Enter a research query above to get started. Our AI will search multiple sources, analyze content, and generate a comprehensive report.
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-200 mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-sm text-gray-600">
            Powered by LangGraph & Google Gemini • Web Research Assistant
          </p>
        </div>
      </footer>
    </div>
  );
}
