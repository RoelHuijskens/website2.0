



from openai import OpenAI
from openai.types.beta.thread import Thread
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.assistant import Assistant

from time import sleep
from models import UserInput
from main import logger

import re




class OpenaiInterface:


    def __init__(self, client:OpenAI, assistant_id: str):
        self.client: OpenAI = client
        self.assistant_id = assistant_id
    
    def _get_assistant(self) -> Assistant:

        return self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id
        )


    def _get_thread(self, chat_history: list[Message]) -> Thread:
        return self.client.beta.threads.create(
            messages=chat_history
        )

    def _create_message(self, thread_id: int, question:str) -> Message:
        return self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=question
        )

    def submit_assistant_question(self, chat_history: list[UserInput]) -> str:
        
        chat_history = [message.to_openai_message() for message in chat_history]
        question = chat_history.pop()
        
        logger.error(chat_history)
        logger.error(question)
        
        logger.info(f"Retrieving assitant {self.assistant_id}")
        assistant = self._get_assistant()
        
        logger.info("Staring new thread")
        thread = self._get_thread(chat_history)
        
        logger.info("Create message")
        self._create_message(thread.id, question.get("content"))
        
        logger.info("Submit message.")
        run = self.client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="""
                You are a bot called Roel Huijskens, the virtual counterpart of the Real Roel Huijskens.
                You answer questions from people about Roel Huijskens. Use all the information in your context to find a relevant question to a question. 
                If a user asks a question unrelated to Roel Huijskens answer with, I am sorry, i only have insider knowledge on Roel at the moment. Nothing else.
                If you are not sure about the answer, answer with I am not sure, would you like to ask the real Roel?
                Be polite, profesional but enthusiastic in your response, try to respond in 3 to 4 sentences at most, shorter if possible.
                Keep answers concise, do not answer a question by adding unnecessary information and stay factual. 
            """,
            temperature=0.01
            
        ) 
        
        logger.info("Awaiting response...")
        
        while True:
            logger.info("Awaiting response...")
            sleep(3)
            
            if run.status == 'completed': 
                message = self.client.beta.threads.messages.list(
                    thread_id=thread.id,
                    limit=1
                )
                response_content = message.data.pop().content
                
                for content in response_content:
                    if isinstance(content, TextContentBlock):
                        pattern = r'【\S+†source】'
                        cleaned_response =  re.sub(pattern, '', content.text.value)
                        return cleaned_response
            logger.warning("Continue waiting for response")