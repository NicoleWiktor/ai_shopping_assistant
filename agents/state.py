from typing import TypedDict, Optional, List, Dict, Any

class State(TypedDict):
	query: str
	original_query: str  # Store the initial user query, never changes
	urls: List[str]
	products: List[Dict[str, Any]]  # [{product_name, product_price, product_review_summary, url}]
	approved: Optional[bool]
	feedback: Optional[str]
	refinement_attempts: int
	extracts: List[str]  # Raw content from Tavily Extract
	pages: List[str]  # Alias for extracts (backward compat)
	recommendation: Optional[Dict[str, Any]]  # {content: str} from decide_and_summarize
	
def make_initial_state(query: str) -> "State":
	return {
		"query": query,
		"original_query": query,  # Save the original
		"urls": [],
		"products": [],
		"approved": None,
		"feedback": None,
		"refinement_attempts": 0,
		"extracts": [],
		"pages": [],
		"recommendation": None,
	}
