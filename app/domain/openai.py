from openai import OpenAI
from openai.types.beta.thread import Thread
from openai.types.beta.threads.message import Message
from openai.types.beta.thread_create_params import Message as CreateMessage
from openai.types.beta.threads.text_content_block import TextContentBlock
from openai.types.beta.threads.message_content import MessageContent
from openai.types.beta.threads.run import Run
from openai.types.beta.threads.file_citation_annotation import (
    FileCitationAnnotation,
)
from openai.types.beta.assistant import Assistant

from typing import Optional, Tuple, List

from datetime import datetime, timedelta
from time import sleep
from app.models import QuestionDto
from app.logging.app_logging import logger

import re


class OpenaiInterface:
    def __init__(self, client: OpenAI, assistant_id: str):
        self.client: OpenAI = client
        self.assistant_id = assistant_id

    def _get_assistant(self) -> Assistant:
        """Get existing assistant from openai.

        Returns:
            Assistant: Assistant object.
        """
        return self.client.beta.assistants.retrieve(
            assistant_id=self.assistant_id
        )

    def _get_thread(self, chat_history: list[CreateMessage]) -> Thread:
        """Create a new thread in the assitants playground

        Args:
            chat_history (list[Message]): List of message objects in chat.

        Returns:
            Thread: A new thread object from openai.
        """
        return self.client.beta.threads.create(messages=chat_history)

    def _create_message(self, thread_id: str, question: str) -> Message:
        """Add user question to existing thread in assistants playground

        Args:
            thread_id (int): ID of existing thread on OpenAI
            question (str): User provided question

        Returns:
            Message: OpenaiMessage Object
        """
        return self.client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=question
        )

    def _await_response(
        self, run: Run, thread: Thread, timeout_sec: Optional[int] = None
    ) -> Tuple[str, List[str]]:
        """Poll when run is completed and parse response.

        Args:
            run (Run): OpenAI Run object
            thread (Thread): Created Openai Thread Object
            timeout_sec (Optional[int], optional): Polling timeout.

        Raises:
            Exception: When response takes longer then timeout period.

        Returns:
            Tuple[str, List[str]]: Tuple containing formatted
                string response from assistants api and file paths to
                knowledge documents associated with this answer.
        """
        if not timeout_sec:
            timeout_sec = 30
        timeout = datetime.now() + timedelta(seconds=timeout_sec)

        while datetime.now() < timeout:
            logger.info("Awaiting response...")
            sleep(3)
            if run.status == "completed":
                logger.info("Received Response")
                message = self.client.beta.threads.messages.list(
                    thread_id=thread.id, limit=1
                )

                message_run = message.data.pop()
                return self._clean_openai_response(message_run.content)
            logger.warning("Continue waiting for response")
            # TODO make this a custom exception.
        raise Exception(
            "The response took too long to arrive, please try again later."
        )

    @staticmethod
    def _clean_openai_response(
        response: list[MessageContent],
    ) -> Tuple[str, List[str]]:
        """Clean OpenAI response message removing sources and parse objects.

        Args:
            response (list[MessageContent]): Messages from OpenAI run.

        Raises:
            Exception: raise exception if no TextContentBlock was returned.

        Returns:
            Tuple[str, List[str]]: Tuple containing the question response in
                text and a list of file paths relating to knowlegde documents.
        """
        for content in response:
            if isinstance(content, TextContentBlock):
                if not content.text.annotations:
                    response_disclaimer = """  (*This answer is not based on any of my documents in my knowledge base and might be wrong...
                        you could try asking a more specific question*)"""  # noqa E501
                else:
                    response_disclaimer = ""

                raw_response = content.text.value
                pattern = r"【\S+†.*】"
                print(raw_response)
                response_str = re.sub(pattern, "", raw_response)

                return response_str + response_disclaimer, [
                    annotation.file_citation.file_id
                    for annotation in content.text.annotations
                    if isinstance(annotation, FileCitationAnnotation)
                ]
        logger.error(
            f"Openai response did not contain a content block got: {content}"
        )
        raise Exception(
            f"Openai response did not contain a content block got: {content}"
        )

    def submit_assistant_question(
        self, chat_history: list[QuestionDto], question: QuestionDto
    ) -> Tuple[str, List[str]]:
        """Submit user question to OpenAI assistant and await response.

        Args:
            chat_history (list[UserInput]): User and assistant messages.
            question (UserInput): User provided question.

        Returns:
            Tuple[str, Optional[List[str]]]: Tuple containing the question
                response in text and a list of file paths relating to
                knowlegde documents.

        """

        try:
            chat_history_openai = [
                message.to_openai_message() for message in chat_history
            ]
            question_str = question.content

            if len(question_str) > 150:
                return (
                    f"""I'm sorry, your question was too long ({len(question_str)} characters).
                    I like OpenAI but I am not made of money, so I've capped the total character count for questions to 150.""",  # noqa E501
                    [],
                )

            logger.info(f"Retrieving assistant {self.assistant_id}")
            assistant = self._get_assistant()

            logger.info("Staring new thread")
            thread = self._get_thread(chat_history_openai)

            logger.info("Create message")
            self._create_message(thread.id, question_str)

            logger.info("Submit message.")

            run = self.client.beta.threads.runs.create_and_poll(
                thread_id=thread.id,
                assistant_id=assistant.id,
                instructions="""
                    You are a bot called Roel Huijskens, the virtual counterpart of the Real Roel Huijskens.
                    Only answer questions about Roel Huijskens (which is you). Don't divert to unrelated topics.
                    Always use the retrieval tool when generating an answer. If you get no results back from this tool. Inform that you are not sure.
                    Be polite, profesional but enthusiastic in your response, try to respond in 3 to 4 sentences at most, shorter if possible.
                    Keep answers concise, do not answer a question by adding unnecessary information and stay factual.
                """,  # noqa E501
                temperature=0.01,
            )

            logger.info("Awaiting response...")
            response, annotations = self._await_response(run, thread)
            return response, annotations

        except Exception as e:
            logger.error(
                f"Something went wrong while interacting with openai: {e}"
            )
            raise e

    # Todo: Implement this method for getting file names in annotations.
    # def get_file_info(self, file_id: str):

    #     return self.client.files.retrieve(file_id=file_id)
