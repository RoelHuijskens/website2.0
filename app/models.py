
from pydantic import BaseModel
from enum import Enum
from  openai.types.beta.thread_create_params import Message
from typing import List, Optional
from datetime import datetime

class Role(Enum):
    USER = "user"
    BOT = "bot"




class UserInput(BaseModel):
    content: str
    role: Role


    def to_openai_message(self) -> Message:
        if self.role == Role.BOT:
            role = "assistant"
        else:
            role = "user"
        return Message(
            content=self.content,
            role = role
        )
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role.value
        }    
        
class ChatResponse(UserInput):
    chat_id: str
    
    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "role": self.role.value
        }    

class QuestionDto(UserInput):
    annotations: Optional[List[str]] = []
    
    def to_dict(self) -> dict:
        question_dict = super().to_dict()
        question_dict["annotations"] = self.annotations
        return question_dict
    
    
class ConversationDto(BaseModel):
    questions: list[QuestionDto]
    chat_id: str
    start_time: datetime
    
    