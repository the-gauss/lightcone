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
      setError("Paste a YouTube URL to continue.");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await submitYoutubeUrl(trimmed);
      setResult(response);
    } catch (submitError) {
      setError(submitError.message || "Failed to submit the URL.");
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
        <span className="badge">LangGraph + FastAPI</span>
        <h1>Lightcone Studio</h1>
        <p>
          Drop in a YouTube link to queue a processing workflow and generate
          downstream insights.
        </p>
      </header>

      <main className="panel">
        <form className="form" onSubmit={handleSubmit}>
          <label htmlFor="youtube-url">YouTube URL</label>
          <div className="input-row">
            <input
              id="youtube-url"
              type="url"
              placeholder="https://www.youtube.com/watch?v=..."
              value={url}
              onChange={(event) => setUrl(event.target.value)}
              autoComplete="off"
              required
            />
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Sending…" : "Queue video"}
            </button>
          </div>
          <div className="hint">
            <span>Try a sample:</span>
            {SAMPLE_URLS.map((sample) => (
              <button
                key={sample}
                className="chip"
                type="button"
                onClick={() => handleSample(sample)}
              >
                {sample.replace("https://", "")}
              </button>
            ))}
          </div>
        </form>

        {error ? (
          <section className="status error">
            <h2>Submission failed</h2>
            <p>{error}</p>
          </section>
        ) : null}

        {result ? (
          <section className="status success">
            <div>
              <h2>Queued</h2>
              <p>{result.message}</p>
            </div>
            <div className="meta">
              <div>
                <span>Request ID</span>
                <strong>{result.request_id}</strong>
              </div>
              <div>
                <span>Received URL</span>
                <strong>{result.received_url}</strong>
              </div>
            </div>
          </section>
        ) : null}
      </main>

      <footer className="footer">
        <span>API target</span>
        <strong>{import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1"}</strong>
      </footer>
    </div>
  );
}
