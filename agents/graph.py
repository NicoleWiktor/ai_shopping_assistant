from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph, END
from agents.state import State
from agents.nodes.search_products import search_products
from agents.nodes.generate_response import decide_and_summarize


def build_graph_custom():
	"""
	Builds the custom LangGraph workflow for the shopping assistant.
	
	Flow: START → search_products → decide_and_summarize → END
	"""
	g = StateGraph(State)
	g.add_node("search_products", search_products)
	g.add_node("decide_and_summarize", decide_and_summarize)
	g.set_entry_point("search_products")
	g.add_edge("search_products", "decide_and_summarize")
	g.add_edge("decide_and_summarize", END)
	return g.compile()

