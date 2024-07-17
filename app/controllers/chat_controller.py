from app.domain.openai import OpenaiInterface
from app.logging.nofications import (
    NotificationsInterface,
    update_thread_executor,
)
from app.db.dao import ConversationsDao
from app.models import QuestionDto, ConversationDto, ChatResponse, Role
from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Optional, List
from app.utils import generate_random_string, generate_security_hash
from app.logging.app_logging import logger
import threading


class ChatsController(object):
    def __init__(
        self,
        db: ConversationsDao,
        notifications: NotificationsInterface,
        openai_client: OpenaiInterface,
    ) -> None:
        self.db = db
        self.notifications = notifications
        self.openai_client = openai_client

    def _start_notification_thread(self, message: str) -> None:
        """Start a new thread for sending an update using the mail interface

        Args:
            message (str): Notification message body
        """
        threading.Thread(
            target=update_thread_executor, args=(self.notifications, message)
        ).start()

    def _check_recent_chats_limit(
        self,
        question: QuestionDto,
    ) -> None:
        """Verify conversation count within timeframe is below threshold

        Args:
            question (QuestionDto): User question object being processed

        Raises:
            HTTPException: If total conversation threshold is used.
        """
        if (
            self.db.get_recent_chats_count(datetime.now() - timedelta(hours=1))
            > 25
        ):
            logger.warning(
                "Total requeest count per hour has exceeded max of 25"
            )
            self._start_notification_thread(
                f"Max conversations count triggered: {question.content}"
            )
            raise HTTPException(
                detail="""Appologies, too many conversations have been
                started in the last hour, please try again later.""",
                status_code=503,
            )

    def _check_current_chat_limit(self, current_chat: ConversationDto) -> None:
        """Verify whether current chat has reached the max question limit.

        Args:
            current_chat (ConversationDto): Current chat being processed.

        Raises:
            HTTPException: If question limit is reached for conversation.
        """
        if len(current_chat.questions) > 9:
            logger.warning(
                f"Chat {current_chat.chat_id} exceeded total max questions."
            )
            raise HTTPException(
                detail="""It seems you have a lot of questions,
                let's connect via [**linkedin** (link)](https://nl.linkedin.com/in/roel-huijskens)
                I can answer more there.""",  # noqa E501
                status_code=503,
            )

    def _get_or_create_conversation(
        self, question: QuestionDto, conversation_id: Optional[str]
    ) -> ConversationDto:
        """Retrieve or create a new conversation object in database.

        Args:
            question (QuestionDto): User provided question object
            conversation_id (Optional[str]): Client provided conversation id

        Raises:
            HTTPException: if provided conversation_id does not exist

        Returns:
            ConversationDto: Created or retrieved conversation object.
        """
        if not conversation_id:
            conversation_id, start_time = generate_random_string()
            current_chat = ConversationDto(
                questions=[question],
                start_time=start_time,
                chat_id=conversation_id,
            )
            self.db.create_chat(current_chat)
            admin_hash = generate_security_hash(seed=conversation_id)
            self._start_notification_thread(
                f"Someone started a new conversation, see: https://roel-huijskens.azurewebsites.net/chat?conversation_id={conversation_id}&hash={admin_hash}"  # noqa E501
            )
        else:
            current_chat = self.db.get_chat_by_id(conversation_id)
            if not current_chat:
                raise HTTPException(
                    detail=(
                        "Failed to retrieve specified chat, try refreshing your page"  # noqa E501
                    ),
                    status_code=404,
                )
            self.db.append_chat(question, current_chat.chat_id)
        return current_chat

    def _format_and_store_response(
        self, response: str, annotations: List[str], chat_id: str
    ) -> ChatResponse:
        """Format and store response from the OpenAI assistants API

        Args:
            response (str): Response text from OpenAI assistant
            annotations (List[str]): List of file paths to knowledge docs
            chat_id (str): Current chat id

        Returns:
            ChatResponse: Chat response object
        """
        format_response = ChatResponse(
            content=response,
            role=Role.BOT,
            chat_id=chat_id,
        )

        self.db.append_chat(
            format_response,
            chat_id=format_response.chat_id,
            annotations=annotations,
        )

        return format_response

    def handle_user_question(
        self, question: QuestionDto, conversation_id: Optional[str]
    ) -> ChatResponse:
        """User question handler flow, process/store user question.

        Args:
            question (QuestionDto): User provided question object
            conversation_id (Optional[str]): Current conversation id

        Raises:
            HTTPException: If openai interface did not provide a response.

        Returns:
            ChatResponse: Chat response object
        """
        self._check_recent_chats_limit(question)
        current_chat = self._get_or_create_conversation(
            question, conversation_id
        )
        self._check_current_chat_limit(current_chat=current_chat)

        response, annotations = self.openai_client.submit_assistant_question(
            chat_history=current_chat.questions, question=question
        )

        if response:
            return self._format_and_store_response(
                response=response,
                annotations=annotations,
                chat_id=current_chat.chat_id,
            )
        else:
            raise HTTPException(
                detail=(
                    "Appologies, something went wrong while communicating with openai, please try again later"  # noqa E501
                ),
                status_code=503,
            )

    def _get_security_hash(self, conversation_id: str) -> str:
        """Get security hash based on client provided conversation id

        Args:
            conversation_id (str): Client provided conversation id

        Returns:
            str: Generated security hash
        """
        return generate_security_hash(conversation_id)

    def get_chat(self, conversation_id: str, hash: str) -> dict[str, str]:
        """Retrieve conversation from database

        Args:
            conversation_id (str): Id of conversation to be retrieved
            hash (str): Client provided security hash.

        Raises:
            HTTPException: If provided conversation id does not exist.
            HTTPException: If provided security hash is invalid.

        Returns:
            dict[str, str]: Dictionary with all questions in conversation.
        """
        if hash == self._get_security_hash(conversation_id):
            chat = self.db.get_chat_by_id(conversation_id)
            if not chat:
                raise HTTPException(
                    detail=f"Could not find chat {conversation_id}",
                    status_code=404,
                )
            return chat.model_dump()

        else:
            logger.warning("Unauthorized accessw attempt to chats endpoint.")
            raise HTTPException(
                detail="What on earth are you doing here?? Please leave..",
                status_code=401,
            )
