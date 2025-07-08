from tavily import TavilyClient
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import function_tool


@function_tool
def internet_search(query: str) -> dict:
    """Search the internet using Tavily and return structured results.

    This tool is designed to search the internet using Tavily and return structured results.

    Parameters
    ----------
    query : str
        The natural-language search query.

    Returns
    -------
    dict
        A dictionary matching Tavily's response schema, for example:

            {
              "query": "Who is Leo Messi?",
              "answer": "Lionel Messi ...",
              "images": [],
              "results": [
                  {"title": "...", "url": "...", "content": "...", "score": 0.81}
              ],
              "auto_parameters": {"topic": "general", "search_depth": "basic"},
              "response_time": "1.67"
            }

    Raises
    ------
    RuntimeError
        If environment variables cannot be loaded.
    """
    print(f"Searching the internet with query: {query}")
    status = load_dotenv(os.path.join(BASE_PATH, ENV_PATH))
    if not status:
        raise Exception(f"Failed to load environment variables from {os.path.join(BASE_PATH, ENV_PATH)}")
    
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=query,
        max_results=MAX_SEARCH_RESULTS,
        search_depth=SEARCH_DEPTH,
        include_images=False,
        include_videos=False,
        include_audio=False,
        include_files=False,
    )
    return response





