from typing import TypedDict, Optional, List, Dict, Any

class State(TypedDict):
	query: str
	urls: List[str]
	products: List[Dict[str, Any]]  # [{product_name, product_price, product_review_summary, url}]
	approved: Optional[bool]
	feedback: Optional[str]
	refinement_attempts: int


