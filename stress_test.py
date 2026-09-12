import time
import threading
import logging
from simulator.city_sim import CitySimulator
from tools.city_tools import CityTools
from agent.orchestrator import UrbanCrisisAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("StressTest")

def run_simulator(sim):
    while True:
        sim.update()
        time.sleep(0.5)

def main():
    # 1. Initialize
    sim = CitySimulator()
    tools = CityTools(sim)
    agent = UrbanCrisisAgent(tools)

    # Start simulator
    sim_thread = threading.Thread(target=run_simulator, args=(sim,), daemon=True)
    sim_thread.start()

    print("\n---  STARTING ADAPTATION STRESS TEST  ---")

    # STEP 1: Create a high priority incident
    logger.info("STEP 1: Creating a critical incident at location 5")
    tools.add_emergency("Fire", location=5, priority=5)

    # Let the agent observe and dispatch
    logger.info("Agent is observing and planning...")
    agent.run_iteration()

    # Verify dispatch
    state = sim.get_state()
    active_unit = None
    for uid, res in state['resources'].items():
        if res['assigned_incident'] == 'inc_1':
            active_unit = uid
            break

    if not active_unit:
        print(" Error: Agent failed to dispatch a unit.")
        return

    logger.info(f" Success: {active_unit} dispatched to inc_1")

    # STEP 2: Mid-transit blockage
    # We wait until the unit is close to the target
    logger.info("STEP 2: Waiting for unit to start moving...")
    time.sleep(1)

    # Block a road on the path (in our simple simulator, we just block any road)
    # Since the simulator is simple, we'll block a road and then
    # force the agent to "re-observe" and "re-plan".
    logger.info("️  SIMULATING FAILURE: Blocking road r2_3...")
    tools.block_road("r2_3")

    # STEP 3: Agent Detection and Recovery
    logger.info("STEP 3: Agent is now detecting the failure and adapting...")

    # Run the agent loop again.
    # In a real scenario, the agent would see the unit isn't moving
    # or the path is blocked and would decide to dispatch a DIFFERENT unit
    # from a different direction or reroute.
    agent.run_iteration()

    print("\n--- Final Stress Test State ---")
    print(sim.get_state())
    print("\n Stress test completed. Check the logs to see the Agent's reasoning loop!")

if __name__ == "__main__":
    main()
