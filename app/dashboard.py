import streamlit as st
import pandas as pd
import time
from simulator.city_sim import CitySimulator
from tools.city_tools import CityTools
from agent.orchestrator import UrbanCrisisAgent

# Page Config
st.set_page_config(page_title="Urban Crisis Response Agent", layout="wide")

# Initialize Session State
if 'sim' not in st.session_state:
    st.session_state.sim = CitySimulator()
    st.session_state.tools = CityTools(st.session_state.sim)
    st.session_state.agent = UrbanCrisisAgent(st.session_state.tools)
    st.session_state.logs = []

def log_message(msg):
    st.session_state.logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

# --- Sidebar: Controls ---
st.sidebar.title(" Control Panel")

st.sidebar.subheader(" Trigger Emergencies")
with st.sidebar.form("emergency_form"):
    e_type = st.selectbox("Incident Type", ["Fire", "Medical", "Police"])
    e_loc = st.slider("Location", 0, 9, 5)
    e_pri = st.slider("Priority", 1, 5, 3)
    if st.form_submit_button("Add Emergency"):
        inc_id = st.session_state.tools.add_emergency(e_type, e_loc, e_pri)
        log_message(f"Created {e_type} emergency {inc_id} at loc {e_loc} (Pri: {e_pri})")

st.sidebar.subheader(" Infrastructure")
with st.sidebar.form("infra_form"):
    road_id = st.text_input("Road ID (e.g., r0_1)", "r0_1")
    action = st.selectbox("Action", ["Block Road", "Unblock Road"])
    if st.form_submit_button("Apply Change"):
        if action == "Block Road":
            st.session_state.tools.block_road(road_id)
            log_message(f"Road {road_id} BLOCKED")
        else:
            st.session_state.tools.unblock_road(road_id)
            log_message(f"Road {road_id} OPENED")

st.sidebar.markdown("---")
if st.sidebar.button(" Clear Logs"):
    st.session_state.logs = []

# --- Main UI ---
st.title(" Urban Crisis Response Dashboard")
st.markdown("Autonomous Resource Orchestration powered by **LangGraph & Claude 3.5 Sonnet**")

# Top row: Stats
state = st.session_state.sim.get_state()
col1, col2, col3 = st.columns(3)
col1.metric("Open Incidents", len([i for i in state['incidents'].values() if i['status'] == 'open']))
col2.metric("Active Units", len([r for r in state['resources'].values() if r['status'] == 'busy']))
col3.metric("City Tick", state['tick'])

# Middle row: The Map (Visual representation of the 1D city)
st.subheader(" City Map")
map_cols = st.columns(10)
for i in range(10):
    with map_cols[i]:
        # Find units at this location
        units_here = [r['id'] for r in state['resources'].values() if r['location'] == i]
        # Find incidents at this location
        incs_here = [i['id'] for i in state['incidents'].values() if i['location'] == i and i['status'] == 'open']

        # Color coding
        bg_color = "white"
        if incs_here: bg_color = "#ffcccc" # Reddish for emergency

        st.markdown(
            f"""<div style="background-color:{bg_color}; border:1px solid #ddd; padding:10px; text-align:center; border-radius:5px; min-height:100px;">
                <b>Loc {i}</b><br>
                <small>Units: {', '.join(units_here) if units_here else 'None'}</small><br>
                <small>Incs: {', '.join(incs_here) if incs_here else 'None'}</small>
            </div>""",
            unsafe_allow_html=True
        )

# Bottom row: Agent Controls & Logs
st.markdown("---")
c1, c2 = st.columns([1, 2])

with c1:
    st.subheader(" Agent Action")
    if st.button(" Run Agent Iteration", use_container_width=True):
        with st.spinner("Claude is reasoning..."):
            # Run the agent iteration
            result = st.session_state.agent.run_iteration()
            log_message("Agent completed one iteration of the LangGraph loop.")
            st.rerun()

    if st.button(" Advance Simulator (1 Tick)", use_container_width=True):
        st.session_state.sim.update()
        log_message("Simulator advanced by 1 tick.")
        st.rerun()

with c2:
    st.subheader(" Agent Reasoning Logs")
    log_container = st.container(height=300)
    with log_container:
        for log in reversed(st.session_state.logs):
            st.text(log)

# Data Tables (Expanders)
with st.expander(" Resource Details"):
    st.table(pd.DataFrame.from_dict(state['resources'], orient='index'))

with st.expander(" Incident Details"):
    st.table(pd.DataFrame.from_dict(state['incidents'], orient='index'))
