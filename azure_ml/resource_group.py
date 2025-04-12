from azureml.core import Workspace
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

ws = Workspace(
    subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
    resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
    workspace_name=os.getenv("AZURE_WORKSPACE_NAME"),
    credential=DefaultAzureCredential()  # Secure auth
)