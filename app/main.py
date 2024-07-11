
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware


import uvicorn
from typing import List, Optional
from fastapi.staticfiles import StaticFiles


from models import UserQuestion, UserInput, ChatResponse, ConversationDto
from utils import generate_random_string

import logging
import sys

#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger(__name__).addHandler(logging.StreamHandler(stream=sys.stdout))
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,stream=sys.stdout )

from dependencies import get_openai_interface, OpenaiInterface, get_mongodb_client, ConversationsDao


app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://roel-huijskens.azurewebsites.net/"
    "http://roel-huijskens.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    

@app.post("/chat")
def chat(
    question: UserInput, 
    conversation_id: Optional[str] = None, 
    interface: OpenaiInterface  = Depends(get_openai_interface), 
    db: ConversationsDao = Depends(get_mongodb_client)
    ) -> ChatResponse:
    
    if not conversation_id:
        conversation_id, start_time = generate_random_string()
        current_chat = ConversationDto(
            questions=[question],
            start_time=start_time,
            chat_id=conversation_id
        )
        db.create_chat(
            current_chat
        )
    else:
        current_chat = db.get_chat_by_id(conversation_id)
        db.append_chat(
            question, current_chat.chat_id
        )
        if not current_chat:
            raise HTTPException("Failed to retrieve specified chat, please try refreshing your page")


    try:
        response = interface.submit_assistant_question(
            chat_history=current_chat.questions,
            question = question
        )
        if response:
            format_response = ChatResponse(
                content=UserQuestion(
                    questionText=response
                ),
                role="bot",
                chat_id=current_chat.chat_id
            )
            db.append_chat(format_response, chat_id=format_response.chat_id)
            return format_response
        else:
            return UserInput(
                content=UserQuestion(
                    questionText="Apologies something went wrong, please try again later."
                ),
                role="bot"
            ) 
    except Exception as e:
        logger.error(f"Failed to sent request to open ai with: {e}")



app.mount("/", StaticFiles(directory="frontend_dist",  html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
