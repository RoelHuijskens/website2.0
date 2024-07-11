
from pydantic import BaseModel
from enum import Enum
from  openai.types.beta.thread_create_params import Message
from typing import List
from datetime import datetime

class Role(Enum):
    USER = "user"
    BOT = "bot"


class UserQuestion(BaseModel):
    questionText: str


class UserInput(BaseModel):
    content: UserQuestion
    role: Role


    def to_openai_message(self) -> Message:
        if self.role == Role.BOT:
            role = "assistant"
        else:
            role = "user"
        return Message(
            content=self.content.questionText,
            role = role
        )
    
    def to_dict(self) -> dict:
        return {
            "content": self.content.model_dump(),
            "role": self.role.value
        }    
        
class ChatResponse(UserInput):
    chat_id: str
    
    def to_dict(self) -> dict:
        return {
            "content": self.content.model_dump(),
            "role": self.role.value
        }    
    
class ConversationDto(BaseModel):
    questions: list[UserInput]
    chat_id: str
    start_time: datetime
    
    