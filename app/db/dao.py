from pymongo import MongoClient
from typing import Optional, List
from app.models import ConversationDto, UserInput
from datetime import datetime


class ConversationsDao(object):
    def __init__(self, client: MongoClient) -> None:
        self.client = client

    def append_chat(
        self,
        question: UserInput,
        chat_id: str,
        annotations: Optional[List[str]] = None,
    ):
        """Add new message to existing conversation

        Args:
            question (UserInput): User or bot provided message
            chat_id (str): Existing Chat Id
            annotations (Optional[List[str]], optional): List of file paths.
        """
        db = self.client["PersonalWebsite"]
        collection = db["Conversations"]

        question_dict = question.to_dict()

        if annotations:
            question_dict["annotations"] = annotations

        collection.update_one(
            {"_id": chat_id}, {"$push": {"questions": question_dict}}
        )

    def get_chat_by_id(self, chat_id: str) -> ConversationDto:
        """Get an existing chat by ID

        Args:
            chat_id (str): Id of an exisitng chat.

        Returns:
            ConversationDto: Retrieved conversation object.
        """
        db = self.client["PersonalWebsite"]
        collection = db["Conversations"]
        chat = collection.find_one({"_id": chat_id})
        # TODO change id key in query
        chat["chat_id"] = chat["_id"]  # type: ignore
        del chat["_id"]  # type: ignore
        return ConversationDto(**chat)  # type: ignore

    def create_chat(self, conversation: ConversationDto):
        """Create a new chat

        Args:
            conversation (ConversationDto): New conversation object
        """
        db = self.client["PersonalWebsite"]
        collection = db["Conversations"]
        collection.insert_one(
            {
                "_id": conversation.chat_id,
                "start_time": conversation.start_time,
                "questions": [conversation.questions[0].to_dict()],
            }
        )

    def get_recent_chats_count(self, threshold: datetime) -> int:
        """Get count of recently started chats within defined timeframe

        Args:
            threshold (datetime): Timestamp indicating start of timeframe.

        Returns:
            int: Count conversations started in the specified timeframe.
        """
        db = self.client["PersonalWebsite"]
        collection = db["Conversations"]
        return collection.count_documents({"start_time": {"$gte": threshold}})
