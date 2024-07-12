
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime, timedelta

import uvicorn
from typing import List, Optional
from fastapi.staticfiles import StaticFiles


from models import UserInput, ChatResponse, ConversationDto
from utils import generate_random_string

import logging
import sys


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,stream=sys.stdout )

from dependencies import get_openai_interface, OpenaiInterface, get_mongodb_client, ConversationsDao, NotificationsInterface, get_notification_inerface


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
    db: ConversationsDao = Depends(get_mongodb_client),
    notifications:NotificationsInterface = Depends(get_notification_inerface)
    ) -> ChatResponse:
    
    
    if db.get_recent_chats_count(datetime.now() - timedelta(hours=1)) > 30:
        notifications.send_update_notification(f"Someone triggerd the max conversations count with question: {question.content}")
        raise HTTPException(detail="Appologies, too many conversations have been started in the last hour, please try again later.", status_code=503)
    
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
        notifications.send_update_notification(f"Someone started a new conversation with question: {question.content}, see chat: {conversation_id}")
    else:
        current_chat = db.get_chat_by_id(conversation_id)
        db.append_chat(
            question, current_chat.chat_id
        )
        if not current_chat:
            raise HTTPException(detail="Failed to retrieve specified chat, please try refreshing your page", status_code=404)


    if len(current_chat.questions) > 9:
        raise HTTPException(detail="It seems you have a lot of questions, let's connect via [**linkedin** (link)](https://nl.linkedin.com/in/roel-huijskens) I can answer more there.", status_code=503)

    try:
        response, annotations = interface.submit_assistant_question(
            chat_history=current_chat.questions,
            question = question
        )
        if response:
            format_response = ChatResponse(
                content=response,
                role="bot",
                chat_id=current_chat.chat_id,
            )
            
            logger.info("Ze annotations")
            logger.info(annotations)
            
            db.append_chat(format_response, chat_id=format_response.chat_id, annotations=annotations)
            
            return format_response
        else:
            return UserInput(
                content="Apologies something went wrong, please try again later.",
                role="bot"
            ) 
    except Exception as e:
        logger.error(e)
        notifications.send_error_notification("Something went wrong while processing a request to openai.")
        raise HTTPException(detail="Something went wrong while submitting your request, please try again later", status_code=503)



@app.post("/file_info")
def run(file_id: str, openai_client: OpenaiInterface = Depends(get_openai_interface)):
    return openai_client.get_file_info(
        file_id=file_id
    )


app.mount("/", StaticFiles(directory="frontend_dist",  html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
