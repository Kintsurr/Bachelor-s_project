from azureml.core import Workspace
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

def get_workspace():
    credential = DefaultAzureCredential()
    ws = Workspace(
        subscription_id=os.getenv("AZURE_SUBSCRIPTION_ID"),
        resource_group=os.getenv("AZURE_RESOURCE_GROUP"),
        workspace_name=os.getenv("AZURE_WORKSPACE_NAME"),
        credential=credential
    )
    return ws


# Test authentication
if __name__ == "__main__":
    ws = get_workspace()
    print(f"Connected to: {ws.name}")