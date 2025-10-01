from agents.graph import build_graph

def run_shopping_assistant():
	agent = build_graph()
	user_input = "Find me cheap wireless headphones"
	final = None
	for step in agent.stream({"messages": user_input}, stream_mode="values"):
		final = step["messages"][-1]
	print(final.content)