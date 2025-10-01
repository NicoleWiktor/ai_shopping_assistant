from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from tools.tavily import build_tavily_search_tool
import os
from dotenv import load_dotenv

def build_graph():
	load_dotenv()
	api_key = os.getenv("OPENAI_API_KEY", "")
	max_results = int(os.getenv("MAX_SEARCH_RESULTS", "8"))
	llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)
	tavily_search_tool = build_tavily_search_tool(max_results=max_results)
	agent = create_react_agent(llm, tools=[tavily_search_tool])
	return agent



