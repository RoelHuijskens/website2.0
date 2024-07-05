
from pydantic import BaseModel
from enum import Enum
from  openai.types.beta.thread_create_params import Message


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
        