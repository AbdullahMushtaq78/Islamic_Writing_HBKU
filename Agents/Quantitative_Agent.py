import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
from Configs.configs import *
from agents import Agent, Runner, ModelSettings, AgentOutputSchema
from Tools.Internet_Extract import extract_from_url
from Tools.Internet_Search import internet_search
from pydantic import BaseModel
from Tools.Ayah_Search import fetch_quran_ayah

class Accuracy_Verification_Log(BaseModel):
    content_snippet: str
    matched_source_type: str
    matched_source_reference: str
    matched_source_text: str
    source_url: str
    verification_comment: str
    verification_result: str
class Quantitative_Agent_Output(BaseModel):
    structure_score: float
    structure_feedback: str
    theme_score: float
    theme_feedback: str
    clarity_score: float
    clarity_feedback: str
    originality_score: float
    originality_feedback: str
    islamic_accuracy_score: float
    islamic_accuracy_feedback: str
    citation_score: float
    citation_feedback: str
    overall_score: float
    accuracy_verification_log: list[Accuracy_Verification_Log] = [
      Accuracy_Verification_Log(
        content_snippet="",
        matched_source_type="",
        matched_source_reference="",
        matched_source_text="",
        source_url="",
        verification_comment="",
        verification_result=""
      )
    ]

class Quantitative_Agent:
    def __init__(self):
        with open(os.path.join(BASE_PATH, PROMPTS_PATH, QUANTITATIVE_AGENT_PROMPT), "r", encoding="utf-8") as f:
            self.system_prompt = f.read()
        self.agent = Agent(
            name="Quantitative_Agent",
            instructions=self.system_prompt,
            model=QUANTITATIVE_MODEL,
            model_settings=ModelSettings(
                temperature=TEMPERATURE,
                #parallel_tool_calls=PARALLEL_TOOLS_CALLS,
            ),
            tools = [extract_from_url, internet_search, fetch_quran_ayah],
            output_type=AgentOutputSchema(
                Quantitative_Agent_Output,
                strict_json_schema=False,
            ),
        )

    def run(self, query:str)->dict:
        result = Runner.run_sync(self.agent, query, max_turns=MAX_TOOLS_CALLS)
        return result.final_output.dict()
    
    