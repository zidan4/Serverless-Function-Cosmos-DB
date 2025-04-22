import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os
import json

# Cosmos DB setup via environment variables
URL = os.environ["COSMOS_URL"]
KEY = os.environ["COSMOS_KEY"]
DATABASE = "UserDB"
CONTAINER = "Profiles"

client = CosmosClient(URL, credential=KEY)
db = client.get_database_client(DATABASE)
container = db.get_container_client(CONTAINER)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger processed a request.')

    try:
        data = req.get_json()
        name = data.get("name", "unknown")
        container.create_item({"id": name, "name": name})
        return func.HttpResponse(json.dumps({"message": f"Added {name}"}), status_code=200)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse("Error", status_code=500)
