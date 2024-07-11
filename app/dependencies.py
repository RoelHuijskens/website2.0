from openai import OpenAI
from domain.openai import OpenaiInterface
import os
from pymongo import MongoClient
from dao import ConversationsDao


openai_client = OpenAI()
assistant_id = os.getenv("OPENAI_ASS_ID")



async def get_openai_interface() -> OpenaiInterface:
    return OpenaiInterface(
        client=openai_client,
        assistant_id=assistant_id
    )
    
    

async def get_mongodb_client():
    # MongoDB connection string
    
    USER_NAME = os.getenv("DB_USER_NAME")
    PW = os.getenv("DB_PASSWORD")
    
    if not USER_NAME or not PW:
        raise Exception("Forgto to set DB_USER_NAME or DB_PASSWORD")
    connection_string = f"mongodb+srv://{USER_NAME}:{PW}@conversations-info.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
    
    # Create a MongoDB client
    client = MongoClient(connection_string)
    
    dao =  ConversationsDao(client)
    
    yield dao
    
    print("Closing the connection")
    dao.client.close()
    
    
    