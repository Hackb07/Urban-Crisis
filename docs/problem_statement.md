# Problem Statement: Autonomous Real-time Urban Crisis Response & Resource Orchestrator

## Overview
Build an autonomous crisis-management agent that orchestrates emergency resources in a dynamic, evolving urban disaster scenario. The system must monitor a live stream of simulated emergency events and sensor data, prioritize goals, allocate limited resources, and adapt in real-time when conditions change.

## Core Objectives
- **Goal-Driven Execution:** Move from "responding to a prompt" to "managing a city state."
- **Real-time Adaptation:** Respond to unplanned disruptions (e.g., road closures, resource failures).
- **Resource Optimization:** Minimize response time and maximize lives saved under strict resource constraints.

## Required Agentic Workflow
1. **Continuous Monitoring:** Ingest a real-time stream of emergency alerts and infrastructure status.
2. **Dynamic Prioritization:** Maintain a global "Crisis State" and autonomously decide which events require immediate action.
3. **Resource Orchestration:** Use tools to dispatch units, calculate optimal routes, and assign tasks.
4. **Observation & Feedback:** Monitor the progress of dispatched units.
5. **Real-time Adaptation:** Re-route units or re-assign resources when a planned action fails or a new higher-priority event occurs.
6. **Outcome Verification:** Verify that critical objectives are met before closing the incident.

## Evaluation Success Criteria
- **Autonomy:** Can the agent handle a sequence of 5+ events without human intervention?
- **Adaptation:** Does the agent correctly reroute a unit when a road is marked "Blocked" mid-transit?
- **Tool Use:** Does it effectively combine GIS tools, Resource DBs, and State Managers?
