


from openai.types.beta.assistant import Assistant
from openai import OpenAI
from models import UserInput




class OpenaiInterface:


    def __init__(self, client:OpenAI, assistant_id: str):
        self.client: OpenAI = client
        self.assistant_id = assistant_id
    
    def _get_assistant(self):

        return self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id
        )


    def _get_thread(self):
        return self.client.beta.threads.create(
            messages=self.messag_history
        )

    def submit_assistant_question(chat_history: list[UserInput]):
        raise ValueError(chat_history)


