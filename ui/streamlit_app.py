import streamlit as st
import os
import sys
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import build_graph_custom
from agents.state import make_initial_state

def render_app():
	st.title("Shopping Assistant")
	
	# Show graph visualization in sidebar
	with st.sidebar:
		st.subheader("Workflow Graph")
		try:
			app = build_graph_custom()
			# Generate PNG image of the graph
			graph_image = app.get_graph().draw_mermaid_png()
			st.image(graph_image)
		except Exception as e:
			st.error(f"Could not generate graph visualization: {e}")
			st.info("Install graphviz if needed: `brew install graphviz` or `apt-get install graphviz`")
	
	query = st.text_input("What are you shopping for?", value="Find me cheap wireless headphones")
	if st.button("Search"):
		app = build_graph_custom()
		state = make_initial_state(query)
		with st.spinner("Running..."):
			result = app.invoke(state)

		# Polished answer (from decide_and_summarize)
		st.subheader("Assistant answer")
		rec = result.get("recommendation", {}) or {}
		st.write(rec.get("content", "No answer"))
		st.write("DEBUG result keys:", result.keys())
		st.write("DEBUG extracts count:", len(result.get("extracts", [])))
		# Debug: search_products outputs
		st.subheader("Search results (search_products)")
		urls = result.get("urls", [])
		for u in urls:
			st.write(u)

		# Debug: tavily_extract + extract_pages outputs
		st.subheader(f"Extracted pages (tavily_extract via extract_pages) — {len(result.get('pages', []))}")
		for i, content in enumerate(result.get("pages", [])):
			with st.expander(f"Extract #{i+1} — {urls[i] if i < len(urls) else ''} ({len(content)} chars)"):
				st.text_area(f"Content {i+1}", content, height=300)


if __name__ == "__main__":
	render_app()