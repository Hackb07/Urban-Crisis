import os
import time
import logging
from typing import Annotated, List, TypedDict, Dict, Any, Union
from operator import add

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode

from tools.city_tools import CityTools

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("UrbanAgent")

load_dotenv()

# 1. State Definition
class AgentState(TypedDict):
    # The list of messages in the conversation
    messages: Annotated[List[BaseMessage], add]
    # Current snapshot of the city state
    city_state: Dict[str, Any]
    # Track active missions to identify failures
    active_missions: Dict[str, Any]

# 2. Tool Definitions (LangChain format)
# We wrap the existing CityTools to make them compatible with LangGraph
def create_langchain_tools(city_tools: CityTools):
    @tool
    def get_city_state():
        """Returns the current state of all incidents, resources, and roads in the city."""
        return city_tools.get_city_state()

    @tool
    def dispatch_unit(unit_id: str, incident_id: str):
        """Assigns a resource unit to an incident. Returns True if successful."""
        return city_tools.dispatch_unit(unit_id, incident_id)

    @tool
    def block_road(road_id: str):
        """Simulates a road blockage for testing adaptation."""
        return city_tools.block_road(road_id)

    @tool
    def add_emergency(type: str, location: int, priority: int):
        """Adds a new emergency incident to the city."""
        return city_tools.add_emergency(type, location, priority)

    return [get_city_state, dispatch_unit, block_road, add_emergency]

# 3. Node Definitions
class UrbanGraph:
    def __init__(self, city_tools: CityTools):
        self.city_tools = city_tools
        self.tools = create_langchain_tools(city_tools)
        self.tool_node = ToolNode(self.tools)

        # Initialize the LLM with tool binding
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0
        ).bind_tools(self.tools)

    def observe(self, state: AgentState):
        """Node to update the current city state"""
        logger.info("Node: Observe - Updating city state...")
        current_state = self.city_tools.get_city_state()
        return {
            "city_state": current_state,
            "messages": [HumanMessage(content=f"Current City State: {current_state}")]
        }

    def plan(self, state: AgentState):
        """Node where Claude decides what to do"""
        logger.info("Node: Plan - Reasoning with Claude...")
        response = self.llm.invoke(state["messages"])
        return {"messages": [response]}

    def evaluate(self, state: AgentState):
        """Node to determine if we need to loop back or finish"""
        last_message = state["messages"][-1]

        if last_message.tool_calls:
            return "execute"

        # If no tool calls, check if all incidents are resolved
        incidents = state["city_state"]["incidents"]
        if any(inc["status"] == "open" for inc in incidents.values()):
            logger.info("Evaluation: Incidents still open. Looping back to observe.")
            return "observe"

        logger.info("Evaluation: All incidents resolved. Ending loop.")
        return END

    def build(self):
        # Define the graph
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("observe", self.observe)
        workflow.add_node("plan", self.plan)
        workflow.add_node("execute", self.tool_node)

        # Define edges
        workflow.add_edge(START, "observe")
        workflow.add_edge("observe", "plan")
        workflow.add_edge("execute", "observe") # Loop back to check result

        # Conditional edge from plan to either execute or evaluate
        workflow.add_conditional_edges(
            "plan",
            self.evaluate,
            {
                "execute": "execute",
                "observe": "observe",
                END: END
            }
        )

        return workflow.compile()

class UrbanCrisisAgent:
    def __init__(self, tools: CityTools):
        self.graph = UrbanGraph(tools).build()

    def run_iteration(self):
        """Runs one full cycle of the agentic loop"""
        initial_state = {
            "messages": [],
            "city_state": {},
            "active_missions": {}
        }

        # Run the graph until it reaches END
        final_state = self.graph.invoke(initial_state)
        return final_state
