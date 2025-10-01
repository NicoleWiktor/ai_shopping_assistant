from langchain_tavily import TavilySearch

def build_tavily_search_tool(max_results: int = 8, topic: str = "general"):
	return TavilySearch(max_results=max_results, topic=topic)


