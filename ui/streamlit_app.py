import streamlit as st
import os
import sys
import uuid
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.graph import build_graph_custom
from agents.state import make_initial_state

def render_app():
	st.title("Shopping Assistant")
	
	# ALWAYS build graph fresh (don't cache it)
	app = build_graph_custom()
	
	# Show graph visualization in sidebar
	with st.sidebar:
		st.subheader("Workflow Graph")
		try:
			graph_image = app.get_graph().draw_mermaid_png()
			st.image(graph_image)
		except Exception as e:
			st.error(f"Could not generate graph visualization: {e}")
	
	# Initialize session state
	if "thread_id" not in st.session_state:
		st.session_state.thread_id = str(uuid.uuid4())
	if "result" not in st.session_state:
		st.session_state.result = None
	
	config = {"configurable": {"thread_id": st.session_state.thread_id}}
	
	query = st.text_input("What are you shopping for?", value="Find me cheap wireless headphones")
	
	if st.button("Search"):
		state = make_initial_state(query)
		# Reset thread_id for new search
		st.session_state.thread_id = str(uuid.uuid4())
		config = {"configurable": {"thread_id": st.session_state.thread_id}}
		
		with st.spinner("Running..."):
			result = app.invoke(state, config)
			st.session_state.result = result
	
	# Display results if they exist
	if st.session_state.result:
		result = st.session_state.result
		
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
		
		# HITL feedback
		st.divider()
		col1, col2 = st.columns(2)
		
		with col1:
			if st.button("✅ Approve"):
				app.update_state(config, {"approved": True})
				final = app.invoke(None, config)
				st.success("Search approved!")
		
		with col2:
			feedback = st.text_input("Or provide feedback:")
			if st.button("🔄 Refine") and feedback:
				# Ensure we keep the original_query across the interrupt by injecting it explicitly
				orig_q = result.get("original_query", result.get("query", ""))
				app.update_state(
					config,
					{"approved": False, "feedback": feedback, "original_query": orig_q},
					as_node="decide_and_summarize",
				)
				with st.spinner("Refining..."):
					new_result = app.invoke(None, config)
					st.session_state.result = new_result
				st.rerun()


if __name__ == "__main__":
	render_app()