from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def decide_and_summarize(state: dict) -> dict:
    import os
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage

    llm = ChatOpenAI(model=os.getenv("LLM_MODEL", "gpt-4o-mini"), api_key=os.getenv("OPENAI_API_KEY", ""))
    extracts = state.get("extracts") or state.get("pages") or []

    sys = SystemMessage(content=(
        "You are a shopping assistant. From the provided web extracts, identify 3-5 relevant products. "
        "For each, include product_name, product_price if present, and a 1-2 sentence product_review_summary. "
        "Return a friendly, polished markdown answer and include links when you can infer them from the text."
    ))
    
    # Limit to first 3 extracts and truncate each to 10,000 chars to avoid context limit
    limited_extracts = [e[:10000] for e in extracts[:3]]
    user = HumanMessage(content="\n\n---\n\n".join(limited_extracts) if limited_extracts else "No content.")
    resp = llm.invoke([sys, user])

    return {
        "recommendation": {"content": resp.content if hasattr(resp, "content") else str(resp)}
    }