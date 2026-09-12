# Presentation Outline: Urban Crisis Response Agent
**Project Goal:** To demonstrate a professional Agentic AI system capable of real-time orchestration and adaptation in a dynamic urban disaster environment.

---

## Slide 1: Title Slide
- **Title:** Urban Crisis Response Agent
- **Subtitle:** Autonomous Resource Orchestration using LangGraph & Claude 3.5 Sonnet (via OpenRouter)
- **Visual Suggestion:** A futuristic image of a smart city with connected emergency services.
- **Key Points:** Team Name, Member Names, Tech Zephyr 4.0 | IIT Bhubaneswar.

---

## Slide 2: The Problem Statement
- **Heading:** The Challenge: Urban Chaos in Real-time
- **Content:**
    - Emergency response in disasters is not a "single-turn" problem.
    - **The Complexity:** Constant stream of new alerts, changing road conditions, and limited resources.
    - **The Gap:** Traditional systems are static. We need a system that can **Observe, Plan, and Adapt** autonomously.
- **Visual Suggestion:** A "Chaos vs. Order" split screen (Static list of alerts vs. a coordinated response).

---

## Slide 3: Why Agentic AI?
- **Heading:** Moving Beyond the Chatbot
- **Content:**
    - **Not a Wrapper:** This is not a simple LLM wrapper or a RAG system.
    - **True Autonomy:** The system pursues a goal (Minimize casualties/Restore power) by interacting with environment tools.
    - **Decision-Making:** It doesn't just suggest; it **executes** (Dispatches units, updates priorities).
    - **Statefulness:** It maintains a global "Crisis State" to reason over time.
- **Visual Suggestion:** A comparison table: "Simple LLM" (Input $\rightarrow$ Output) vs. "Agentic AI" (Goal $\rightarrow$ Loop $\rightarrow$ Outcome).

---

## Slide 4: High-Level Architecture
- **Heading:** The System Ecosystem
- **Content:**
    - **The Brain:** Claude 3.5 Sonnet (Reasoning engine).
    - **The Nervous System:** LangGraph (State-machine orchestration).
    - **The World:** Custom Urban City Simulator (Ground truth).
    - **The Interface:** Specialized Tool Suite (API for dispatch, routing, and monitoring).
- **Visual Suggestion:** A block diagram showing the flow: Simulator $\rightarrow$ Tools $\rightarrow$ LangGraph $\rightarrow$ Claude.

---

## Slide 5: The "Winning" Logic: LangGraph Workflow
- **Heading:** The Cyclic Orchestration Loop
- **Content:**
    - **Observe:** Ingests real-time telemetry (Incidents, unit positions).
    - **Plan:** Claude reasons about priorities and selects the best tool.
    - **Execute:** ToolNode interacts with the simulator to dispatch units.
    - **Evaluate:** A conditional edge that determines: "Is the goal met?" $\rightarrow$ If No $\rightarrow$ Loop back to Observe.
- **Visual Suggestion:** A circular flowchart showing the cycle: `START` $\rightarrow$ `Observe` $\rightarrow$ `Plan` $\rightarrow$ `Execute` $\rightarrow$ `Evaluate` $\rightarrow$ (back to Observe).

---

## Slide 6: Tool Integration & Execution
- **Heading:** Bridging AI and Action
- **Content:**
    - **`get_city_state`**: Provides the "eyes" for the agent.
    - **`dispatch_unit`**: The "hands" that move resources.
    - **`block_road`**: Used to simulate real-world failures.
    - **`add_emergency`**: Simulates the unpredictability of disasters.
- **Visual Suggestion:** Screenshots of the JSON state or the tool logs from the terminal.

---

## Slide 7: The Secret Sauce: Real-time Adaptation
- **Heading:** Handling the Unexpected (Adaptation)
- **Content:**
    - **Scenario:** A unit is dispatched $\rightarrow$ Road becomes blocked $\rightarrow$ Unit stops.
    - **Agentic Response:**
        1. **Detection:** The `Observe` node sees the unit is not moving.
        2. **Reasoning:** Claude identifies the road blockage.
        3. **Recovery:** The agent autonomously triggers a **reroute** or assigns a different unit.
- **Visual Suggestion:** A "Before" and "After" path on a map (Plan A $\rightarrow$ Blockage $\rightarrow$ Plan B).

---

## Slide 8: Results & Live Demo
- **Heading:** Proof of Concept
- **Content:**
    - **Goal:** Resolve all critical emergencies.
    - **Outcome:** 100% resolution of high-priority incidents.
    - **Efficiency:** Optimized resource allocation based on priority.
- **Visual Suggestion:** Embed the Demo Video here. Highlight the "Decision $\rightarrow$ Action $\rightarrow$ Adaptation" sequence.

---

## Slide 9: Conclusion & Future Scope
- **Heading:** Scaling the Vision
- **Content:**
    - **Current:** Simulated 1D/2D environment.
    - **Future:** Integration with real GIS data (OpenStreetMap) and actual IoT sensor feeds.
    - **Scalability:** Multi-agent coordination (e.g., one agent for Fire, one for Medical, one for Power).
- **Visual Suggestion:** A vision map showing the project expanding from "Simulation" to "Real World."
