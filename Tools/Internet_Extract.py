from tavily import TavilyClient
import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import function_tool





@function_tool
def extract_from_url(urls: list[str]) -> dict:
    """
    Extract text content from given URLs using Tavily's extraction API.
    
    Args:
        urls (list): The URLs to extract content from
        
    Returns:
        dict: A dictionary containing:
            - results (list): List of dictionaries with:
                - url (str): The URL that was extracted
                - raw_content (str): The extracted text content
                - images (list): List of image URLs found
            - failed_results (list): List of URLs that failed extraction
            - response_time (float): Time taken for the extraction
    """
    print(f"Extracting content from URLs: {urls}")
    status = load_dotenv(os.path.join(BASE_PATH, ENV_PATH))
    if not status:
        raise Exception(f"Failed to load environment variables from {os.path.join(BASE_PATH, ENV_PATH)}")
    
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    
    try:
        response = tavily_client.extract(urls, include_images=False, extract_images=SEARCH_DEPTH, format="markdown")
        return response
    except Exception as e:
        print(f"Error extracting content from URL: {e}")
        return None
