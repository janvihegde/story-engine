import { useState } from 'react';
import './App.css';

function App() {
  const [step, setStep] = useState(1); // 1=Genre, 2=StartSelect, 3=InteractivePlay
  const [genre, setGenre] = useState('horror');
  const [starters, setStarters] = useState([]);
  
  // Interactive State
  const [history, setHistory] = useState([]); // Keeps track of the full story so far
  const [currentNode, setCurrentNode] = useState(null); // The node we are reading right now
  const [options, setOptions] = useState([]); // The buttons to click next
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [gameEnded, setGameEnded] = useState(false);

  // STEP 1: Find Start Nodes
  const fetchStarters = async () => {
    setLoading(true); setError(null);
    try {
      const res = await fetch(`http://localhost:8000/start-nodes?genre=${genre}`);
      const data = await res.json();
      if (data.length === 0) throw new Error("No start nodes found for this genre.");
      setStarters(data);
      setStep(2);
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  // STEP 2 & 3: Play a Step
  const playStep = async (nodeId) => {
    setLoading(true); setError(null);
    try {
      // 1. Fetch details for the chosen node
      const res = await fetch(`http://localhost:8000/story-step?genre=${genre}&node_id=${nodeId}`);
      const data = await res.json();
      
      // 2. Add this new node to our history
      const newNode = data.current_node;
      setHistory((prev) => [...prev, newNode]);
      
      // 3. Update state for the UI
      setCurrentNode(newNode);
      setOptions(data.options);
      setGameEnded(data.is_end);
      
      // 4. Move to Play Mode if not already there
      setStep(3);
      
    } catch (err) { setError(err.message); } 
    finally { setLoading(false); }
  };

  const resetGame = () => {
    setStep(1);
    setHistory([]);
    setCurrentNode(null);
    setOptions([]);
    setGameEnded(false);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>📚 Story Engine</h1>
        <p className="subtitle">Interactive Mode</p>
      </header>

      {/* ERROR MSG */}
      {error && <div className="error-box">{error}</div>}

      {/* === STEP 1: GENRE SELECTION === */}
      {step === 1 && (
        <div className="controls">
          <h3>Step 1: Pick a Genre</h3>
          <select value={genre} onChange={(e) => setGenre(e.target.value)}>
            <option value="horror">👻 Horror</option>
            <option value="thriller">🕵️ Thriller</option>
            <option value="comedy">😂 Comedy</option>
          </select>
          <button className="btn-generate" onClick={fetchStarters} disabled={loading}>
            {loading ? 'Loading...' : 'Start Adventure'}
          </button>
        </div>
      )}

      {/* === STEP 2: START NODE SELECTION === */}
      {step === 2 && (
        <div className="story-list">
          <button onClick={() => setStep(1)} className="btn-back">← Back</button>
          <h3>Step 2: Choose how it begins...</h3>
          <div className="grid-options">
            {starters.map((s) => (
              <div key={s.event_id} className="story-card option" onClick={() => playStep(s.event_id)}>
                <div className="meta">Start Option</div>
                <p className="card-text">{s.preview}</p>
                <button className="btn-select">Start Here →</button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* === STEP 3: INTERACTIVE PLAY === */}
      {step === 3 && (
        <div className="story-list">
           <button onClick={resetGame} className="btn-back">↺ Restart Game</button>
           
           {/* 1. Show History (Previous Cards) */}
           {history.slice(0, -1).map((event, index) => (
             <div key={index} className="story-card history">
               <div className="meta">Chapter {index + 1}</div>
               <p className="card-text text-gray-500">{event.text}</p>
             </div>
           ))}

           {/* 2. Show Current Active Card */}
           {currentNode && (
             <div className="story-card active-card">
               <div className="meta" style={{color: '#2563eb'}}>Currently Reading • Chapter {history.length}</div>
               <p className="card-text" style={{fontSize: '1.2rem', fontWeight: '500'}}>
                 {currentNode.text}
               </p>
             </div>
           )}

           {/* 3. Show Options (Next Moves) */}
           <div className="options-area">
              {loading && <p>Thinking...</p>}
              
              {!loading && !gameEnded && (
                <>
                  <h4 style={{textAlign:'center', margin:'20px 0', color:'#64748b'}}>What happens next?</h4>
                  <div className="grid-options">
                    {options.map((opt) => (
                      <div key={opt.event_id} className="story-card option" onClick={() => playStep(opt.event_id)}>
                        <div className="meta">Option</div>
                        <p className="card-text">{opt.preview}</p>
                        <button className="btn-select">Select →</button>
                      </div>
                    ))}
                  </div>
                </>
              )}

              {gameEnded && (
                <div style={{textAlign: 'center', padding: '40px'}}>
                   <h2 style={{color: '#2563eb'}}>The End.</h2>
                   <p>You have reached the conclusion of this path.</p>
                   <button onClick={resetGame} className="btn-generate" style={{marginTop:'20px'}}>Play Again</button>
                </div>
              )}
           </div>
        </div>
      )}
    </div>
  );
}

export default App;