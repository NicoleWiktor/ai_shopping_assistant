import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient
from pydantic import BaseModel


class SearchQuery(BaseModel):
    """Pydantic model for structured LLM output: a refined search query."""
    search_query: str


def search_products(state: dict) -> dict:
    # 1) LLM writes concise search query
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY", ""))
    search_instructions = SystemMessage(
        content="Rewrite the user's shopping request as a concise web search query for products and reviews."
    )
    messages = [HumanMessage(content=state.get("query", ""))]
    structured = llm.with_structured_output(SearchQuery)
    refined = structured.invoke([search_instructions] + messages).search_query

    # 2) Tavily search -> urls
    tsearch = TavilySearchResults(max_results=8, tavily_api_key=os.getenv("TAVILY_API_KEY", ""))
    docs = tsearch.invoke(refined)
    urls = [d.get("url", d.get("source", "")) for d in docs if d.get("url") or d.get("source")]

    # 3) Tavily extract -> raw page text
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
    resp = client.extract(urls)
    
    # Debug: print what Tavily Extract returns
    print(f"[DEBUG] Tavily Extract response keys: {resp.keys() if isinstance(resp, dict) else type(resp)}")
    if isinstance(resp, dict) and "results" in resp and len(resp["results"]) > 0:
        first_result = resp["results"][0]
        print(f"[DEBUG] First result keys: {first_result.keys()}")
        print(f"[DEBUG] First result URL: {first_result.get('url', 'N/A')}")
        print(f"[DEBUG] First result raw_content length: {len(first_result.get('raw_content', ''))}")
        print(f"[DEBUG] First result raw_content preview: {first_result.get('raw_content', '')[:200]}")
    
    extracts = []
    for item in resp.get("results", []):
        content = item.get("raw_content", "")
        if content:
            extracts.append(content)
            print(f"[DEBUG] Added extract with {len(content)} chars")

    # 4) Return ONLY the new/updated keys
    return {
        "urls": urls,
        "extracts": extracts,
        "pages": extracts,  
    }