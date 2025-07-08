import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import function_tool
import requests

@function_tool
def fetch_hadith(hadith_number: str) -> dict:
    pass