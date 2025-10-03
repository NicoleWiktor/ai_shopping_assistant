from typing import TypedDict, Optional, List, Dict, Any

class State(TypedDict):
	query: str
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
		"urls": [],
		"products": [],
		"approved": None,
		"feedback": None,
		"refinement_attempts": 0,
		"extracts": [],
		"pages": [],
		"recommendation": None,
	}
