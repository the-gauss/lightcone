import { useState } from "react";
import { submitYoutubeUrl } from "./api/client.js";

const SAMPLE_URLS = [
  "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "https://youtu.be/aqz-KE-bpKQ"
];

export default function App() {
  const [url, setUrl] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError("");
    setResult(null);

    const trimmed = url.trim();
    if (!trimmed) {
      setError("Please enter a valid YouTube URL.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await submitYoutubeUrl(trimmed);
      setResult(response);
    } catch (submitError) {
      setError(submitError.message || "Failed to process the video. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSample = (sample) => {
    setUrl(sample);
  };

  return (
    <div className="page">
      <header className="hero">
        <span className="badge">AI Powered Workflow</span>
        <h1>Lightcone Studio</h1>
        <p>
          Transform YouTube videos into concise summaries using the power of Gemini 1.5 Pro.
          Multimodal processing for accurate insights.
        </p>
      </header>

      <main className="panel">
        <form className="form" onSubmit={handleSubmit}>
          <div className="input-group">
            <input
              className="input-field"
              type="url"
              placeholder="Paste YouTube URL here..."
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={isSubmitting}
              autoComplete="off"
            />
            <button 
              className="submit-btn" 
              type="submit" 
              disabled={isSubmitting || !url.trim()}
            >
              {isSubmitting ? <span className="loading-dots">Processing</span> : "Generate Summary"}
            </button>
          </div>
          
          <div className="samples">
            {SAMPLE_URLS.map((sample) => (
              <button
                key={sample}
                type="button"
                className="sample-chip"
                onClick={() => handleSample(sample)}
                disabled={isSubmitting}
              >
                Sample: {sample.split('v=')[1] || sample.split('/').pop()}
              </button>
            ))}
          </div>
        </form>

        {error && (
          <div className="result-card error">
            <div className="result-header">
              <span className="result-title">Error</span>
            </div>
            <p>{error}</p>
          </div>
        )}

        {result && (
          <div className={`result-card ${result.status === 'failed' ? 'error' : ''}`}>
            <div className="result-header">
              <span className="result-title">
                {result.status === 'completed' ? 'Analysis Complete' : 'Processing Failed'}
              </span>
            </div>

            <div className="meta-grid">
              <div className="meta-item">
                <label>Request ID</label>
                <strong>{result.request_id}</strong>
              </div>
              <div className="meta-item">
                <label>Video URL</label>
                <strong>{result.received_url}</strong>
              </div>
            </div>

            {result.summary && (
              <div className="summary-content">
                {result.summary}
              </div>
            )}
            
            {result.error && (
              <p>{result.error}</p>
            )}
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by LangGraph & Google Gemini 1.5 Pro</p>
      </footer>
    </div>
  );
}
