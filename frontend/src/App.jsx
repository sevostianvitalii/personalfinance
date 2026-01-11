import React, { useState, useEffect } from 'react'
import UploadZone from './components/UploadZone'
import Dashboard from './components/Dashboard'
import './index.css'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("ErrorBoundary caught an error", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '2rem', color: 'red' }}>
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            {this.state.error && this.state.error.toString()}
          </details>
          <button className="btn btn-outline" onClick={() => window.location.reload()}>Reload Page</button>
        </div>
      );
    }

    return this.props.children;
  }
}

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0)
  const [isUploading, setIsUploading] = useState(false)

  const handleUploadComplete = () => {
    setRefreshTrigger(prev => prev + 1)
    setIsUploading(false)
  }

  return (
    <ErrorBoundary>
      <div className="container animate-fade-in">
        <header style={{ marginBottom: '3rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>Finance Analyzer</h1>
            <p style={{ color: 'var(--text-secondary)' }}>Private, local, secure.</p>
          </div>
          <button
            className="btn btn-outline"
            onClick={() => setIsUploading(!isUploading)}
          >
            {isUploading ? 'Close Upload' : 'Upload Statement'}
          </button>
        </header>

        {isUploading && (
          <div className="glass-panel" style={{ padding: '2rem', marginBottom: '2rem' }}>
            <h2 style={{ fontSize: '1.5rem' }}>Upload Bank Statement</h2>
            <UploadZone onUploadComplete={handleUploadComplete} />
          </div>
        )}

        <Dashboard key={refreshTrigger} />
      </div>
    </ErrorBoundary>
  )
}

export default App
