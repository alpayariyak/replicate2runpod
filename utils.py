from dotenv import load_dotenv
import os

def load_tokens():
    load_dotenv()
    runpod_token = os.getenv('RUNPOD_TOKEN')
    hf_token = os.getenv('HF_TOKEN')
    return runpod_token, hf_token

