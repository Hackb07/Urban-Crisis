# How to Run the Urban Crisis Response Agent

This application demonstrates an autonomous agent managing a real-time city crisis simulation.

## Prerequisites
- Python 3.10+ installed.

## Running the Application
From the root directory of the project, run the following command in your terminal:

```bash
export PYTHONPATH=$PYTHONPATH:. && python app/main.py
```

*(On Windows CMD, use `set PYTHONPATH=. && python app/main.py`)*

## What to Expect
1. The application starts a **City Simulator** in the background.
2. It triggers two emergency events: a **High Priority Fire** and a **Medical Emergency**.
3. The **UrbanCrisisAgent** will:
    - **Observe** the city state.
    - **Reason** about which resources are available and which incidents are most urgent.
    - **Dispatch** the appropriate units (Fire truck for Fire, Ambulance for Medical).
    - **Track** the units as they move towards the targets.
4. After several ticks, you will see the **Final City State**, showing if the incidents were resolved.
