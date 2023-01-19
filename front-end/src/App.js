import React, { useState } from 'react';
import './App.css'; //import css file

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    // make a post request to the server with the repo URL
    // await response from server
    try {
      const response = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl }),
      });
      const data = await response.json();
      console.log(data);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <form className="bottom-aligned" onSubmit={handleSubmit}>
        <input 
          type="text" 
          placeholder="Enter git repository URL" 
          value={repoUrl} 
          onChange={e => setRepoUrl(e.target.value)} 
        />
        <button type="submit">Submit</button>
      </form>
      {loading ? <div className="wait-text">Analyzing...</div> : null}
    </div>
  );
}

export default App;