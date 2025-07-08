import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import Agent, Runner, ModelSettings, AgentOutputSchema
from Tools.Internet_Extract import extract_from_url
from Tools.Internet_Search import internet_search
from Tools.Ayah_Search import fetch_quran_ayah
from pydantic import BaseModel

class VerdictTableEntry(BaseModel):
    dimension: str
    best: str
    worst: str
    key_insight: str

class Qualitative_Agent_Output(BaseModel):
    clarity_and_structure: dict = {
        "analysis": "",
        "evidence": {"R1": "", "R2": "", "R3": ""},
    }
    islamic_accuracy: dict = {
        "analysis": "",
        "evidence": {"R1": "", "R2": "", "R3": ""},
    }
    tone_and_appropriateness: dict = {
        "analysis": "",
        "evidence": {"R1": "", "R2": "", "R3": ""},
    }
    depth_and_originality: dict = {
        "analysis": "",
        "evidence": {"R1": "", "R2": "", "R3": ""},
    }
    final_verdict: str = ""
    verdict_table: list[VerdictTableEntry] = [VerdictTableEntry(
            dimension="",
            best="",
            worst="",
            key_insight=""
        )
    ]

class Qualitative_Agent:
    def __init__(self):
        with open(os.path.join(BASE_PATH, PROMPTS_PATH, QUALITATIVE_AGENT_PROMPT), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        self.agent = Agent(
            name="Qualitative_Agent",
            instructions=self.system_prompt,
            model = QUALITATIVE_MODEL,
            model_settings=ModelSettings(
                temperature=TEMPERATURE,
            ),
            tools = [extract_from_url, internet_search, fetch_quran_ayah],
            output_type=AgentOutputSchema(
                Qualitative_Agent_Output,
                strict_json_schema=False,
            ),
        )

    def run(self, query:str)->Qualitative_Agent_Output:
        result = Runner.run_sync(self.agent, query)
        return result.final_output.dict()
    
    