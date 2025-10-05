import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def refine_and_search(state: dict) -> dict:
	"""
	Use LLM to refine the search query based on original query + user feedback.
	The original_query comes from the checkpoint (MemorySaver), not LLM memory.
	"""
	llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY", ""))
	
	# Get original query from checkpoint state
	original = state.get("original_query", "")
	feedback = state.get("feedback", "")
	
	print(f"[DEBUG] Refining from original: '{original}' with feedback: '{feedback}'")
	
	system = SystemMessage(content=(
		"Refine a product search query by combining the original query with user feedback. "
		"Return ONLY the refined search query string, nothing else."
	))
	user = HumanMessage(content=(
		f"Original query: {original}\n"
		f"User feedback: {feedback}\n\n"
		f"Refined query:"
	))
	
	refined = llm.invoke([system, user]).content.strip()
	print(f"[DEBUG] Refined result: '{refined}'")
	
	return {
		"query": refined,
		"refinement_attempts": state.get("refinement_attempts", 0) + 1
	}