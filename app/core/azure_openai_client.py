import os
from dotenv import load_dotenv
from openai import AzureOpenAI

def get_azure_openai_client():
    load_dotenv()  # Load environment variables from .env file

    azure_endpoint = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_CHAT_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_CHAT_API_VERSION")

    return AzureOpenAI(
        api_version=api_version,
        azure_endpoint=azure_endpoint, # type: ignore
        api_key=azure_key,
    )