import os
from dotenv import load_dotenv

def load_settings():
    load_dotenv()
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY", ""),
        "MAX_RESULTS": int(os.getenv("MAX_SEARCH_RESULTS", "8")),
    }