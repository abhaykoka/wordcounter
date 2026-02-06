import { useState, useEffect } from 'react';

const API_URL = import.meta.env.PROD ? '/api/count' : 'http://127.0.0.1:8000/count';

function App() {
  const [text, setText] = useState('');
  const [count, setCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    // Apply theme to body
    document.body.className = theme;
  }, [theme]);

  // Debounced counting or manual? 
  // Requirement says "upload your text... and it will count".
  // Real-time is better for UX. Ill do it on effect change with debounce.
  useEffect(() => {
    const timer = setTimeout(() => {
      countWords(text);
    }, 300); // 300ms debounce

    return () => clearTimeout(timer);
  }, [text]);

  const countWords = async (inputText) => {
    if (!inputText.trim()) {
      setCount(0);
      return;
    }

    setIsLoading(true);
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setCount(data.count);
    } catch (error) {
      console.error('Error counting words:', error);
      // Fallback local count if API fails? No, requirement says backend.
    } finally {
      setIsLoading(false);
    }
  };

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <div className="glass-panel">
      <header className="header">
        <h1>WordCount_</h1>
        <button onClick={toggleTheme} className="theme-toggle" aria-label="Toggle theme">
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>
      </header>

      <main className="editor-container">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste your essay here to begin..."
          autoFocus
        />
      </main>

      <footer className="stats-bar">
        <div className="stat-item">
          <span className="stat-value">{count}</span>
          <span className="stat-label">Words</span>
        </div>

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            Processing...
          </div>
        )}
      </footer>
    </div>
  );
}

export default App;
