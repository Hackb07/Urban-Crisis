import os
import logging
from typing import Annotated, List, TypedDict, Dict, Any, Union, Literal
from operator import add

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

from backend.tools.city_tools import CityTools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProfessionalUrbanAgent")

load_dotenv()

# --- State Definition ---
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add]
    city_state: Dict[str, Any]
    next_agent: str # Who should act next?

# --- Tools Definition ---
def create_city_tools(city_tools: CityTools):
    @tool
    def get_city_state():
        """Returns the current state of all incidents, resources, and roads."""
        return city_tools.get_city_state()

    @tool
    def dispatch_unit(unit_id: str, incident_id: str):
        """Assigns a unit to an incident. Returns True if successful."""
        return city_tools.dispatch_unit(unit_id, incident_id)

    @tool
    def block_road(road_id: str):
        """Blocks a road to simulate disaster evolution."""
        return city_tools.block_road(road_id)

    @tool
    def add_emergency(type: str, location: int, priority: int):
        """Adds a new emergency."""
        return city_tools.add_emergency(type, location, priority)

    return [get_city_state, dispatch_unit, block_road, add_emergency]

# --- Professional Multi-Agent Orchestrator ---
class ProfessionalUrbanGraph:
    def __init__(self, city_tools: CityTools):
        self.city_tools = city_tools
        self.tools = create_city_tools(city_tools)
        self.tool_node = ToolNode(self.tools)

        # LLM for the Supervisor and Workers
        self.llm = ChatOpenAI(
            model="anthropic/claude-3.5-sonnet",
            openai_api_key=os.getenv("OPENROUTER_API_KEY"),
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0
        )

    def supervisor(self, state: AgentState):
        """
        The Manager Agent: Analyzes city state and routes tasks to
        specialized workers (Fire, Medical, Police) or the Verifier.
        """
        logger.info("Manager: Analyzing crisis and delegating...")

        system_prompt = (
            "You are the Urban Crisis Manager. Your goal is to minimize casualties and restore order. "
            "Analyze the city state and delegate tasks to specialized agents: "
            "FireAgent, MedicalAgent, PoliceAgent, or the Verifier. "
            "Once all emergencies are resolved, route to the Verifier to close the case. "
            "Response must be in JSON format: {'next': 'AgentName', 'reasoning': '...'}"
        )

        # We provide the current state as a HumanMessage
        messages = [HumanMessage(content=system_prompt), HumanMessage(content=f"City State: {state['city_state']}")]
        response = self.llm.invoke(messages)

        # In a real system, we'd use structured output. Here we simulate the routing.
        content = response.content.lower()
        if "fire" in content: next_agent = "fire_worker"
        elif "medical" in content: next_agent = "medical_worker"
        elif "police" in content: next_agent = "police_worker"
        elif "resolved" in content or "verify" in content: next_agent = "verifier"
        else: next_agent = "fire_worker" # Default fallback

        return {"next_agent": next_agent, "messages": [response]}

    def worker_node(self, state: AgentState, agent_type: str):
        """
        Specialized Worker Agent: Executes tool calls for their domain.
        """
        logger.info(f"Worker ({agent_type}): Executing domain-specific actions...")

        system_prompt = (
            f"You are the {agent_type} Specialist. Your only goal is to resolve {agent_type} emergencies. "
            "Use the provided tools to dispatch units. Be efficient. "
            "Once you have dispatched all needed units, return a summary."
        )

        llm_with_tools = self.llm.bind_tools(self.tools)
        messages = [HumanMessage(content=system_prompt), HumanMessage(content=f"State: {state['city_state']}")]
        response = llm_with_tools.invoke(messages)

        return {"messages": [response]}

    def verifier(self, state: AgentState):
        """
        Verification Agent: Audits the performance and closes the loop.
        """
        logger.info("Verifier: Auditing operation efficiency...")

        system_prompt = (
            "You are the Quality Assurance Agent. Review the actions taken. "
            "Determine if all critical incidents are resolved and if the response was optimal. "
            "If everything is resolved, output 'COMPLETE'. Otherwise, suggest what is missing."
        )

        messages = [HumanMessage(content=system_prompt), HumanMessage(content=f"Final State: {state['city_state']}")]
        response = self.llm.invoke(messages)

        return {"messages": [response]}

    def build(self):
        workflow = StateGraph(AgentState)

        # Nodes
        workflow.add_node("supervisor", self.supervisor)
        workflow.add_node("fire_worker", lambda s: self.worker_node(s, "Fire"))
        workflow.add_node("medical_worker", lambda s: self.worker_node(s, "Medical"))
        workflow.add_node("police_worker", lambda s: self.worker_node(s, "Police"))
        workflow.add_node("verifier", self.verifier)
        workflow.add_node("execute", self.tool_node)

        # Edges
        workflow.add_edge(START, "supervisor")

        # Supervisor routes to workers or verifier
        workflow.add_conditional_edges(
            "supervisor",
            lambda x: x["next_agent"],
            {
                "fire_worker": "fire_worker",
                "medical_worker": "medical_worker",
                "police_worker": "police_worker",
                "verifier": "verifier"
            }
        )

        # Workers route to execution if they called tools
        def route_after_worker(state: AgentState):
            last_msg = state["messages"][-1]
            if last_msg.tool_calls:
                return "execute"
            return "supervisor"

        workflow.add_conditional_edges("fire_worker", route_after_worker, {"execute": "execute", "supervisor": "supervisor"})
        workflow.add_conditional_edges("medical_worker", route_after_worker, {"execute": "execute", "supervisor": "supervisor"})
        workflow.add_conditional_edges("police_worker", route_after_worker, {"execute": "execute", "supervisor": "supervisor"})

        workflow.add_edge("execute", "supervisor") # Return to manager after tool use

        # Verifier closes the loop
        workflow.add_conditional_edges(
            "verifier",
            lambda x: "END" if "COMPLETE" in x["messages"][-1].content.upper() else "supervisor",
            {"END": END, "supervisor": "supervisor"}
        )

        return workflow.compile()

class UrbanCrisisAgent:
    def __init__(self, tools: CityTools):
        self.graph = ProfessionalUrbanGraph(tools).build()

    def run_iteration(self):
        initial_state = {
            "messages": [],
            "city_state": {},
            "next_agent": ""
        }
        # Run the multi-agent graph
        return self.graph.invoke(initial_state)
