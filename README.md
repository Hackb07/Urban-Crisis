# ️ Urban Crisis Response Agent
**Autonomous Real-time Urban Crisis Response & Resource Orchestrator**

A professional agentic system designed for the **Agentic AI Hackathon (Tech Zephyr 4.0 | IIT Bhubaneswar)**. This project demonstrates how an autonomous agent can manage a complex, evolving urban disaster scenario by interacting with a real-time simulator using a cyclic state-machine architecture.

##  About the Project

The **Urban Crisis Response Agent** is not a chatbot; it is an autonomous operator. Its primary objective is to monitor a live stream of emergency events, prioritize them based on criticality, and orchestrate limited resources (Fire, Medical, Police) to resolve crises as efficiently as possible.

### Core Objectives
- **Goal-Driven Execution:** Managing city-wide state rather than answering one-off prompts.
- **Real-time Adaptation:** Autonomously detecting and responding to disruptions, such as road closures or resource failures.
- **Resource Optimization:** Maximizing lives saved and minimizing response time under strict constraints.

###  Agentic Architecture
The system is powered by **LangGraph** and **Claude 3.5 Sonnet**, implementing a professional cyclic loop:
`START` $\rightarrow$ `Observe` $\rightarrow$ `Plan` $\rightarrow$ `Execute` $\rightarrow$ `Evaluate` $\rightarrow$ `Observe` (Loop)

- **Observe**: Ingests the latest city state (telemetry).
- **Plan**: Claude reasons about priorities and selects the best tools.
- **Execute**: ToolNode interacts with the City Simulator.
- **Evaluate**: Determines if the goal is met or if a replan is necessary.

---

## ️ Getting Started

### Prerequisites
- Python 3.10+
- `uv` installed (`pip install uv`)
- An Anthropic API Key

### Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Hackb07/Urban-Crisis.git
   cd Urban-Crisis
   ```
2. Set up your API key in the `.env` file:
   ```text
   ANTHROPIC_API_KEY=your_api_key_here
   ```

### Running the Application

#### Option 1: Visual Dashboard (Recommended for Demos)
The project includes a Streamlit dashboard for real-time visualization of the city, resource movement, and agent reasoning.
```bash
uv run streamlit run app/dashboard.py
```

#### Option 2: CLI Version (Fast test)
```bash
uv run python app/main.py
```

#### Option 3: Adaptation Stress Test
To prove the agent's ability to handle failures (Road Blockages), run the stress test:
```bash
uv run python stress_test.py
```

---

##  Project Documentation

Detailed specifications and guides are available in the `docs/` folder:

- [**Problem Statement**](docs/problem_statement.md): Detailed overview of the challenge, objectives, and success criteria.
- [**System Design**](docs/design.md): High-level architecture, LangGraph workflow, and tool definitions.
- [**Implementation Roadmap**](docs/roadmap.md): The phased approach taken to build the simulator, tools, and agent.
- [**Presentation Outline**](docs/presentation_outline.md): Blueprint for the final competition presentation.

---

##  Key Features
-  **Real-time Simulation**: A background city simulator with dynamic incidents.
-  **Autonomous Reasoning**: Claude 3.5 Sonnet for high-level decision making.
-  **Dynamic Adaptation**: Ability to reroute units when environmental conditions change.
-  **Visual Orchestration**: A professional dashboard for monitoring agent behavior.

##  License
This project is developed for the Tech Zephyr 4.0 Agentic AI Hackathon.
