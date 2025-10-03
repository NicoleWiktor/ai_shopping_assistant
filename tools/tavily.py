from langchain_tavily import TavilySearch

def build_tavily_search_tool(max_results: int = 8, topic: str = "general"):
	return TavilySearch(max_results=max_results, topic=topic)


def tavily_search(query: str, max_results: int = 8, topic: str = "general"):
	pass

def tavily_extract(urls: list[str], fmt: str = "markdown") -> list[str]:
	clinet = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
	contents = list[str] = []

	for url in urls:
		resp = client.extract(url)
		contents.append(resp.get("content", resp) if isinstance(resp, dict) else str(resp))
	return contents

