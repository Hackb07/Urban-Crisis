import time
import threading
import os
import sys

# Ensure root directory is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulator.city_sim import CitySimulator
from tools.city_tools import CityTools
from agent.orchestrator import UrbanCrisisAgent

def run_simulator(sim):
    """Background thread to keep the city moving"""
    while True:
        sim.update()
        time.sleep(0.5)

def main():
    # 1. Initialize Simulator
    sim = CitySimulator()

    # 2. Initialize Tools
    tools = CityTools(sim)

    # 3. Initialize Professional LangGraph Agent
    agent = UrbanCrisisAgent(tools)

    # Start simulator in background
    sim_thread = threading.Thread(target=run_simulator, args=(sim,), daemon=True)
    sim_thread.start()

    print("Professional Urban Crisis Response Agent Started")
    print("Using LangGraph + Claude 3.5 Sonnet")
    print("-------------------------------------------------")

    # Simulate a sequence of events
    tools.add_emergency("Fire", location=3, priority=5)
    tools.add_emergency("Medical", location=7, priority=4)

    # Instead of a simple loop, we run the agent's graph
    try:
        agent.run_iteration()
    except Exception as e:
        print(f"\n  Error running agent: {e}")
        print("\nNote: Make sure you have added your ANTHROPIC_API_KEY to the .env file!")

    print("\n--- Final City State ---")
    print(sim.get_state())

if __name__ == "__main__":
    main()
