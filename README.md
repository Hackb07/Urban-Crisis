# How to Run the Urban Crisis Response Agent

This application demonstrates an autonomous agent managing a real-time city crisis simulation.

## Prerequisites
- Python 3.10+ installed.
- `uv` installed (`pip install uv`).

## Running the Application

### Option 1: CLI Version (Fast test)
```bash
uv run python app/main.py
```

### Option 2: Visual Dashboard (Recommended for Demos)
The project includes a Streamlit dashboard for real-time visualization of the city, resource movement, and agent reasoning.

```bash
uv run streamlit run app/dashboard.py
```

## What to Expect
1. The application starts a **City Simulator** in the background.
2. It triggers emergency events (Fire, Medical, Police).
3. The **UrbanCrisisAgent** (powered by LangGraph & Claude 3.5 Sonnet) will:
    - **Observe** the city state.
    - **Reason** about which resources are available and which incidents are most urgent.
    - **Dispatch** the appropriate units.
    - **Adapt** and reroute if roads are blocked.
4. You can use the dashboard to manually trigger chaos (block roads, add emergencies) and watch the agent react in real-time.
