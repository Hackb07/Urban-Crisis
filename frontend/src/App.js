import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  AlertTriangle,
  Truck,
  Heart,
  Shield,
  Settings,
  FileText,
  Play,
  FastForward,
  Trash2,
  Map as MapIcon
} from 'lucide-react';
import './App.css';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [state, setState] = useState({ incidents: {}, resources: {}, roads: {}, tick: 0 });
  const [logs, setLogs] = useState([]);
  const [emergencyType, setEmergencyType] = useState('Fire');
  const [emergencyLoc, setEmergencyLoc] = useState(5);
  const [emergencyPri, setEmergencyPri] = useState(3);
  const [roadId, setRoadId] = useState('r0_1');
  const [infraAction, setInfraAction] = useState('block');

  const fetchState = async () => {
    try {
      const res = await axios.get(`${API_BASE}/state`);
      setState(res.data);
    } catch (err) {
      console.error("Failed to fetch state", err);
    }
  };

  useEffect(() => {
    fetchState();
    const interval = setInterval(fetchState, 2000);
    return () => clearInterval(interval);
  }, []);

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [`[${time}] ${msg}`, ...prev].slice(0, 50));
  };

  const handleAddEmergency = async () => {
    try {
      const res = await axios.post(`${API_BASE}/emergency`, {
        type: emergencyType,
        location: emergencyLoc,
        priority: emergencyPri
      });
      addLog(`Created ${emergencyType} emergency ${res.data.incident_id} at ${emergencyLoc}`);
      fetchState();
    } catch (err) {
      addLog("Error adding emergency");
    }
  };

  const handleInfra = async () => {
    try {
      await axios.post(`${API_BASE}/infrastructure`, {
        road_id: roadId,
        action: infraAction
      });
      addLog(`Road ${roadId} ${infraAction}ed`);
      fetchState();
    } catch (err) {
      addLog("Error updating infrastructure");
    }
  };

  const runAgent = async () => {
    try {
      await axios.post(`${API_BASE}/run_agent`);
      addLog("Agent completed one iteration of the LangGraph loop");
      fetchState();
    } catch (err) {
      addLog("Agent execution failed");
    }
  };

  const advanceSim = async () => {
    try {
      await axios.post(`${API_BASE}/advance_sim`);
      addLog("Simulator advanced by 1 tick");
      fetchState();
    } catch (err) {
      addLog("Simulator advance failed");
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-left">
          <MapIcon size={32} />
          <h1>Urban Crisis Response Dashboard</h1>
        </div>
        <div className="header-stats">
          <div className="stat-item">Open Incidents: {Object.values(state.incidents).filter(i => i.status === 'open').length}</div>
          <div className="stat-item">Active Units: {Object.values(state.resources).filter(r => r.status === 'busy').length}</div>
          <div className="stat-item">Tick: {state.tick}</div>
        </div>
      </header>

      <main className="main-content">
        <aside className="sidebar">
          <section className="control-group">
            <div className="group-header"><Settings size={20} /> Controls</div>
            <div className="form-field">
              <label>Emergency Type</label>
              <select value={emergencyType} onChange={e => setEmergencyType(e.target.value)}>
                <option value="Fire">Fire</option>
                <option value="Medical">Medical</option>
                <option value="Police">Police</option>
              </select>
            </div>
            <div className="form-field">
              <label>Location (0-9)</label>
              <input type="number" min="0" max="9" value={emergencyLoc} onChange={e => setEmergencyLoc(parseInt(e.target.value))} />
            </div>
            <div className="form-field">
              <label>Priority (1-5)</label>
              <input type="number" min="1" max="5" value={emergencyPri} onChange={e => setEmergencyPri(parseInt(e.target.value))} />
            </div>
            <button className="btn-primary" onClick={handleAddEmergency}>Add Emergency</button>
          </section>

          <section className="control-group">
            <div className="group-header"><AlertTriangle size={20} /> Infrastructure</div>
            <div className="form-field">
              <label>Road ID</label>
              <input type="text" value={roadId} onChange={e => setRoadId(e.target.value)} />
            </div>
            <div className="form-field">
              <label>Action</label>
              <select value={infraAction} onChange={e => setInfraAction(e.target.value)}>
                <option value="block">Block Road</option>
                <option value="unblock">Unblock Road</option>
              </select>
            </div>
            <button className="btn-secondary" onClick={handleInfra}>Apply Change</button>
          </section>

          <section className="control-group">
            <div className="group-header"><Play size={20} /> Agent Actions</div>
            <button className="btn-agent" onClick={runAgent}>Run Agent Iteration</button>
            <button className="btn-sim" onClick={advanceSim}>Advance Simulator</button>
          </section>
        </aside>

        <section className="map-section">
          <div className="city-grid">
            {Array.from({ length: 10 }).map((_, i) => {
              const unitsHere = Object.values(state.resources).filter(r => r.location === i).map(r => r.id);
              const incsHere = Object.values(state.incidents).filter(inc => inc.location === i && inc.status === 'open').map(inc => inc.id);
              return (
                <div key={i} className={`location-cell ${incsHere.length > 0 ? 'emergency' : ''}`}>
                  <div className="loc-label">Loc {i}</div>
                  <div className="loc-content">
                    {unitsHere.map(u => (
                      <span key={u} className="unit-badge">
                        {Object.values(state.resources).find(r => r.id === u).type === 'Fire' && <Truck size={14} />}
                        {Object.values(state.resources).find(r => r.id === u).type === 'Medical' && <Heart size={14} />}
                        {Object.values(state.resources).find(r => r.id === u).type === 'Police' && <Shield size={14} />}
                        {u}
                      </span>
                    ))}
                    {incsHere.map(inc => (
                      <span key={inc} className="inc-badge"><AlertTriangle size={14} /> {inc}</span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
          <div className="logs-container">
            <div className="logs-header"><FileText size={20} /> Agent Reasoning Logs</div>
            <div className="logs-list">
              {logs.map((log, idx) => <div key={idx} className="log-item">{log}</div>)}
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
