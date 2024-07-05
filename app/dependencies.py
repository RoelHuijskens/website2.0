from openai import OpenAI
from domain.openai import OpenaiInterface
import os


openai_client = OpenAI()
assistant_id = os.getenv("OPENAI_ASS_ID")



async def get_openai_interface() -> OpenaiInterface:
    return OpenaiInterface(
        client=openai_client,
        assistant_id=assistant_id
    )