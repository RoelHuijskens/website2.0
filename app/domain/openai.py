



from openai import OpenAI
from openai.types.beta.thread import Thread
from openai.types.beta.threads.message import Message
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.message_content import MessageContent
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.file_citation_annotation import FileCitationAnnotation
from openai.types.beta.assistant import Assistant

from typing import Optional, Tuple, List

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
        
    def _await_response(self, run: Run, thread: Thread) -> Tuple[str, Optional[List[FileCitationAnnotation]]]:
        while True:
                logger.info("Awaiting response...")
                sleep(3)
                if run.status == 'completed': 
                    logger.info("Received Response")
                    message = self.client.beta.threads.messages.list(
                        thread_id=thread.id,
                        limit=1
                    )
                    
                    message_run = message.data.pop()
                    logger.info("Clean response text.")
                    return OpenaiInterface._clean_openai_response(message_run.content)
                logger.warning("Continue waiting for response")


    @staticmethod
    def _clean_openai_response(response: list[MessageContent]) -> Tuple[str, List[str]]:
        for content in response:
            if isinstance(content, TextContentBlock):
                if not content.text.annotations:
                    response_disclaimer = "  (*This answer is not based on any of my documents in my knowledge base, it might be true or false idk either...*)"
                else:
                    response_disclaimer = ""
                
                raw_response = content.text.value
                pattern = r'【\S+†source】'
                response = re.sub(pattern, '', raw_response)
                
                return response + response_disclaimer, [annotation.file_citation.file_id for annotation in content.text.annotations]
            raise Exception(f"Openai response did not contain a content block, instead got: {response}")


    def submit_assistant_question(self, chat_history: list[UserInput], question: UserInput) -> Tuple[str, Optional[List[str]]]:
        
        
        try:
            chat_history = [message.to_openai_message() for message in chat_history]
            question = question.content
            logger.info(f"The length of the question {len(question)}")
            if len(question) > 150:
                logger.info(f"The length of the question {len(question)}")
                return f"I'm sorry, your question was too long ({len(question)} characters). I like OpenAI but since I am not made of money I've capped the total character count for questions to 150.", None
            
            logger.error(chat_history)
            logger.error(question)
            
            logger.info(f"Retrieving assitant {self.assistant_id}")
            assistant = self._get_assistant()
            
            logger.info("Staring new thread")
            thread = self._get_thread(chat_history)
            
            logger.info("Create message")
            self._create_message(thread.id, question)
            
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
                    Keep answers concise, do not answer a question by adding unnecessary information and stay factual, dont ever mention that you are looking into provided documents, act as if you knew the answers all
                """,
                temperature=0.01
                
            ) 
            
            logger.info("Awaiting response...")
            response, annotations = self._await_response(run, thread)
            return response, annotations
        
        except Exception as e:
            logger.error(f"Something went wrong while interacting with openai: {e}")
        
    
    def get_file_info(self, file_id: str):

        return self.client.files.retrieve(file_id=file_id)