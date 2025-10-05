import os
from langchain_community.tools.tavily_search import TavilySearchResults
from tavily import TavilyClient


def search_products(state: dict) -> dict:
    # Use query directly without LLM reformulation
    search_query = state.get("query", "")
    
    print(f"[DEBUG] search_products called with state keys: {state.keys()}")
    print(f"[DEBUG] Searching for: '{search_query}'")
    
    if not search_query:
        print("[ERROR] Empty search query!")
        return {"urls": [], "extracts": [], "pages": []}

    # 1) Tavily search -> urls
    tsearch = TavilySearchResults(max_results=8, tavily_api_key=os.getenv("TAVILY_API_KEY", ""))
    docs = tsearch.invoke(search_query)
    
    print(f"[DEBUG] Tavily returned {len(docs)} docs, type: {type(docs)}")
    if docs and len(docs) > 0:
        print(f"[DEBUG] First doc type: {type(docs[0])}, keys: {docs[0].keys() if isinstance(docs[0], dict) else 'N/A'}")
    
    urls = [d.get("url", d.get("source", "")) for d in docs if isinstance(d, dict) and (d.get("url") or d.get("source"))]
    print(f"[DEBUG] Extracted {len(urls)} URLs")

    # 2) Tavily extract -> raw page text
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY", ""))
    resp = client.extract(urls)
    
    extracts = []
    for item in resp.get("results", []):
        content = item.get("raw_content", "")
        if content:
            extracts.append(content)
            print(f"[DEBUG] Added extract with {len(content)} chars")

    # 3) Return ONLY the new/updated keys
    return {
        "urls": urls,
        "extracts": extracts,
        "pages": extracts,  
    }
