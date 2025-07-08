import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
import pandas as pd
from Configs.configs import *


def load_dataset():
    inputs = {}
    responses_dict = {}
    dataset_files = os.listdir(DATASET_PATH)
    for file in dataset_files:
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(DATASET_PATH, file))
            df_dict = df.to_dict('records')
            if file.split(".")[0] == "Titles":
                inputs = df_dict
            else:
                responses_dict[file.split(".")[0]] = df_dict
            
    return inputs, responses_dict


def load_dataset_for_qualitative_agent():
    responses_dict = {}
    dataset_files = os.listdir(DATASET_PATH)
    for file in dataset_files:
        if file.endswith(".csv") and file.split(".")[0] != "Titles":
            df = pd.read_csv(os.path.join(DATASET_PATH, file))
            model_responses = {}
            for _, row in df.iterrows():
                model_responses[row["Prompt ID"]] = row["Responses"]
            responses_dict[file.split(".")[0]] = model_responses
    return responses_dict
