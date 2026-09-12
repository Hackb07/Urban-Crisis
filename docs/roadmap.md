# Implementation Roadmap

## Phase 1: Foundation (The Simulator)
- [ ] Build a `simulator.py` that:
    - Generates random incidents.
    - Tracks unit positions.
    - Manages road blockages.
    - Exposes a simple REST API or JSON file for the agent to read.

## Phase 2: The Tool Layer
- [ ] Implement Python functions for:
    - `get_city_state()`
    - `dispatch_unit()`
    - `get_optimal_route()` (using a simple graph algorithm like Dijkstra).

## Phase 3: The Agent Loop
- [ ] Integrate with an LLM (Claude).
- [ ] Implement the `Observe-Plan-Act` loop.
- [ ] Create the "Memory" system to track ongoing missions.

## Phase 4: Adaptation & Edge Cases
- [ ] Implement the logic to detect "Plan Failures" (e.g., unit not moving).
- [ ] Add the "Real-time" trigger: when a `RoadBlocked` event hits, the agent is forced to reconsider all active paths.

## Phase 5: Demo & Polish
- [ ] Create a simple frontend/CLI dashboard to visualize the city map and agent logs.
- [ ] Record the demo video showing the `Goal` $\rightarrow$ `Decision` $\rightarrow$ `Action` $\rightarrow$ `Adaptation` flow.
