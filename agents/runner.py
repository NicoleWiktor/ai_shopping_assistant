from agents.graph import build_graph

def run_shopping_assistant(query: str = "Find me cheap wireless headphones"):
	app = build_graph_custom()
	state = make_initial_state(query)
	result = app.invoke(state)
	print("URLs:", result.get("urls", []))
	print("Pages:", len(result.get("pages", [])))
	return result