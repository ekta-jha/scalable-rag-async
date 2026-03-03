import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def get_azure_openai_client():
    load_dotenv()  # Load environment variables from .env file

    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

    return AzureOpenAI(
        azure_endpoint=azure_endpoint, # type: ignore
        api_key=azure_key,
        azure_deployment=azure_deployment
    )