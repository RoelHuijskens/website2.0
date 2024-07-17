from pydantic import BaseModel
from enum import Enum
from openai.types.beta.thread_create_params import Message
from typing import List, Optional
from datetime import datetime


class Role(Enum):
    """Enumeration for role type of agent who provided a message"""

    USER = "user"
    BOT = "bot"


class UserInput(BaseModel):
    """User provided question"""

    content: str
    role: Role

    def to_openai_message(self) -> Message:
        """Transform input to OpenAI message.

        Returns:
            Message: Instance of Message used in openAI client package
        """
        if self.role == Role.BOT:
            role = "assistant"
        else:
            role = "user"
        return Message(content=self.content, role=role)  # type: ignore

    def to_dict(self) -> dict:
        return {"content": self.content, "role": self.role.value}


class ChatResponse(UserInput):
    """Chat response object send to front-end"""

    chat_id: str

    def to_dict(self) -> dict:
        return {"content": self.content, "role": self.role.value}


class QuestionDto(UserInput):
    """Data transfer object for moving around questions."""

    annotations: Optional[List[str]] = []

    def to_dict(self) -> dict:
        question_dict = super().to_dict()
        question_dict["annotations"] = self.annotations
        return question_dict


class ConversationDto(BaseModel):
    """Data transfer object for moving around conversations."""

    questions: list[QuestionDto]
    chat_id: str
    start_time: datetime
