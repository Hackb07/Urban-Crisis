import os
import time
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from simulator.city_sim import CitySimulator
from tools.city_tools import CityTools
from agent.orchestrator import UrbanCrisisAgent

# Initialize FastAPI app
app = FastAPI(title="Urban Crisis Response API")

# Enable CORS for Frontend (Render) to communicate with Backend (Railway)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your Render URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state for the simulator and agent
# In a production app, you might use a database or Redis,
# but for the hackathon, a global singleton is sufficient.
sim = CitySimulator()
tools = CityTools(sim)
agent = UrbanCrisisAgent(tools)

# Start simulator in a background thread
def run_simulator():
    while True:
        sim.update()
        time.sleep(0.5)

sim_thread = threading.Thread(target=run_simulator, daemon=True)
sim_thread.start()

# --- Models ---
class EmergencyRequest(BaseModel):
    type: str
    location: int
    priority: int

class InfrastructureRequest(BaseModel):
    road_id: str
    action: str # "block" or "unblock"

# --- Endpoints ---

@app.get("/state")
async def get_state():
    """Returns the current city state"""
    return sim.get_state()

@app.post("/emergency")
async def add_emergency(req: EmergencyRequest):
    """Adds a new emergency incident"""
    inc_id = tools.add_emergency(req.type, req.location, req.priority)
    return {"status": "success", "incident_id": inc_id}

@app.post("/infrastructure")
async def update_infrastructure(req: InfrastructureRequest):
    """Blocks or unblocks a road"""
    if req.action == "block":
        success = tools.block_road(req.road_id)
    elif req.action == "unblock":
        success = tools.unblock_road(req.road_id)
    else:
        raise HTTPException(status_code=400, detail="Invalid action. Use 'block' or 'unblock'.")

    return {"status": "success" if success else "failed"}

@app.post("/run_agent")
async def run_agent():
    """Triggers one iteration of the LangGraph agent loop"""
    try:
        result = agent.run_iteration()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/advance_sim")
async def advance_sim():
    """Manually advances the city simulator by one tick"""
    sim.update()
    return {"status": "success", "tick": sim.tick_count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
