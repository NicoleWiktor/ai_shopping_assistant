import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import build_graph

def render_app():
	st.title("Shopping Assistant")
	query = st.text_input("What are you shopping for?", value="Find me cheap wireless headphones")
	if st.button("Search"):
		agent = build_graph()
		final = None
		with st.spinner("Searching..."):
			for step in agent.stream({"messages": query}, stream_mode="values"):
				final = step["messages"][-1]
		st.write(final.content if final else "No result")


if __name__ == "__main__":
	render_app()