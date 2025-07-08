import sys
import os
from Utils.utils import *
from Configs.configs import *
from Agents.Qualitative_Agent import Qualitative_Agent
from Agents.Quantitative_Agent import Quantitative_Agent
from dotenv import load_dotenv
from logging import getLogger
from tqdm import tqdm
from agents import Agent as OpenAIAgent, Runner

logger = getLogger(__name__)
# Load the environment variables
load_dotenv(os.path.join(BASE_PATH, ENV_PATH))


def Run_Quantitative_Agent(inputs, responses_dataset):
    quantitative_agent = Quantitative_Agent()
    logger.info(f"Created Quantitative Agent")
    for model_name, responses in responses_dataset.items(): 
        results = []
        for response in tqdm(responses, desc=f"Running Quantitative Agent for {model_name.split('_')[0]}", total=len(responses)):

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
            results.append(result)
        
        import json
        with open(os.path.join(BASE_PATH, RESULTS_PATH, f"Quantitative_{model_name}.json"), "w") as f:
            json.dump(results, f, indent=4)
        logger.info(f"Results for {model_name} saved to {os.path.join(BASE_PATH, RESULTS_PATH, f'Quantitative_{model_name}.json')}")
    return "Done"



def Run_Qualitative_Agent(inputs, responses_dataset):
    qualitative_agent = Qualitative_Agent()
    logger.info(f"Created Qualitative Agent")
    results = []
    for i in range(len(inputs)):
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
        results.append(result)
    
    import json
    with open(os.path.join(BASE_PATH, RESULTS_PATH, "Qualitative_Results.json"), "w") as f:
        json.dump(results, f, indent=4)
    logger.info(f"Results saved to {os.path.join(BASE_PATH, RESULTS_PATH, 'Qualitative_Results.json')}")
    
    return "Done"




if __name__ == "__main__":
    inputs, responses_dataset_quantitative = load_dataset()
    Quantitative_Results = Run_Quantitative_Agent(inputs, responses_dataset_quantitative)
    print(Quantitative_Results)
    responses_dataset_qualitative = load_dataset_for_qualitative_agent()
    Qualitative_Results = Run_Qualitative_Agent(inputs, responses_dataset_qualitative)
    print(Qualitative_Results)

    # urdu_agent = OpenAIAgent(
    #     name="urdu speaking agent",
    #     instructions="You are a urdu speaking agent.",
    #     model="gpt-4o-mini",
    # )
    # result = Runner.run_sync(urdu_agent, "Hello, how are you?")
    # print(result.final_output)









