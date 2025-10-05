from langgraph.graph import END


def route_after_extraction(state):
	pass


def check_approval(state: dict) -> str:
	"""Decides: END if approved, refine_and_search if not."""
	approved = state.get("approved")
	refinement_attempts = state.get("refinement_attempts", 0)
	
	# Safety: max 3 refinements
	if refinement_attempts >= 3:
		return END
	
	# If no approval decision yet, end
	if approved is None:
		return END
	
	# If approved, we're done
	if approved:
		return END
	
	# If not approved, refine and search again
	return "refine_and_search"