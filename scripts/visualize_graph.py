"""
Visualize the LangGraph workflow as a diagram.

Usage:
    python scripts/visualize_graph.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from agents.graph import build_graph_custom

def visualize():
	"""Generate and display the graph diagram."""
	app = build_graph_custom()
	
	# Get the graph visualization as a Mermaid diagram
	try:
		from IPython.display import Image, display
		# If running in Jupyter
		display(Image(app.get_graph().draw_mermaid_png()))
	except:
		# If running in terminal, save to file
		try:
			png_data = app.get_graph().draw_mermaid_png()
			with open("graph_diagram.png", "wb") as f:
				f.write(png_data)
			print("✅ Graph diagram saved to: graph_diagram.png")
		except Exception as e:
			print(f"⚠️  Could not generate PNG. Error: {e}")
			print("\n📊 Mermaid diagram code (paste into https://mermaid.live):\n")
			print(app.get_graph().draw_mermaid())

if __name__ == "__main__":
	visualize()

