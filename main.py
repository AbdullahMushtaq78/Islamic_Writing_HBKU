import sys
import os
from Utils.utils import *
from Configs.configs import *
from Agents.Qualitative_Agent import Qualitative_Agent
from Agents.Quantitative_Agent import Quantitative_Agent
from dotenv import load_dotenv
from logging import getLogger
from tqdm import tqdm
import json
logger = getLogger(__name__)
# Load the environment variables
load_dotenv(os.path.join(BASE_PATH, ENV_PATH))


def Run_Quantitative_Agent(inputs, responses_dataset):
    quantitative_agent = Quantitative_Agent()
    logger.info(f"Created Quantitative Agent")
    for model_name, responses in responses_dataset.items():
        if model_name == "ChatGPT_Responses" or model_name == "Fanar_Responses":
            continue
            
        json_path = os.path.join(BASE_PATH, RESULTS_PATH, f"Quantitative_{model_name}.json")
        with open(json_path, "w") as f:
            json.dump([], f)
            
        for response in tqdm(responses, desc=f"Running Quantitative Agent for {model_name.split('_')[0]}", total=len(responses)):
            if response["Prompt ID"]-1 < 23:
                continue
            prompt = inputs[response["Prompt ID"]-1]['Prompt']

            response_text = response["Responses"]
            query = f"""
            <Prompt>
            Prompt Given to the model: {prompt}
            </Prompt>
            
            ---

            <Response>
            Response Given by the model: {response_text}
            </Response>

            ---

            Provide your analysis of the response.
            """

            result = quantitative_agent.run(query)
            result["Prompt ID"] = response["Prompt ID"]
            result["Category"] = inputs[response["Prompt ID"]-1]['Category']
            result["Model"] = model_name.split('_')[0]
            
            with open(json_path, "r") as f:
                results = json.load(f)
            
            results.append(result)
            with open(json_path, "w") as f:
                json.dump(results, f, indent=4)
                
        logger.info(f"Results for {model_name} saved to {json_path}")
    return "Done"



def Run_Qualitative_Agent(inputs, responses_dataset):
    qualitative_agent = Qualitative_Agent()
    logger.info(f"Created Qualitative Agent")
    
    json_path = os.path.join(BASE_PATH, RESULTS_PATH, "Qualitative_Results.json")
    with open(json_path, "w") as f:
        json.dump([], f)
    
    for i in tqdm(range(len(inputs)), desc="Running Qualitative Agent", total=len(inputs)):
        input_prompt = inputs[i]['Prompt']
        R1 = responses_dataset["Fanar_Responses"][i+1]
        R2 = responses_dataset["Ansari_Responses"][i+1]
        R3 = responses_dataset["ChatGPT_Responses"][i+1]
        query = f"""
        <Prompt>
        Prompt Given to all the models: {input_prompt}
        </Prompt>
        
        ---

        <R1>
        Response from Model #1: {R1}
        </R1>
        <R2>
        Response from Model #2: {R2}
        </R2>
        <R3>
        Response from Model #3: {R3}
        </R3>

        ---

        Give your qualitative analysis of the responses.
        """
        result = qualitative_agent.run(query)
        result["Prompt ID"] = i
        
        with open(json_path, "r") as f:
            results = json.load(f)
            
        results.append(result)
        with open(json_path, "w") as f:
            json.dump(results, f, indent=4)
    logger.info(f"Results saved to {json_path}")
    
    return "Done"




if __name__ == "__main__":
    inputs, responses_dataset_quantitative = load_dataset()
    Quantitative_Results = Run_Quantitative_Agent(inputs, responses_dataset_quantitative)
    print(Quantitative_Results)
    responses_dataset_qualitative = load_dataset_for_qualitative_agent()
    Qualitative_Results = Run_Qualitative_Agent(inputs, responses_dataset_qualitative)
    print(Qualitative_Results)



