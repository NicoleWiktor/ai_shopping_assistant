from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agents.state import State
from agents.nodes.search_products import search_products
from agents.nodes.generate_response import decide_and_summarize
from agents.nodes.refine import refine_and_search
from agents.nodes.routing import check_approval


def build_graph_custom():
	"""
	Builds the custom LangGraph workflow for the shopping assistant with HITL.
	"""
	g = StateGraph(State)
	g.add_node("search_products", search_products)
	g.add_node("decide_and_summarize", decide_and_summarize)
	g.add_node("refine_and_search", refine_and_search)
	
	g.set_entry_point("search_products")
	g.add_edge("search_products", "decide_and_summarize")
	
	g.add_conditional_edges(
		"decide_and_summarize",
		check_approval,
		{"refine_and_search": "refine_and_search", END: END}
	)
	g.add_edge("refine_and_search", "search_products")
	
	# Create memory and compile - FIXED ORDER
	memory = MemorySaver()
	compiled = g.compile(checkpointer=memory, interrupt_after=['decide_and_summarize'])
	return compiled