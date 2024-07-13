
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from controllers.chat_controller import ChatsController


import uvicorn
from typing import List, Optional
from fastapi.staticfiles import StaticFiles


from models import UserInput, ChatResponse, QuestionDto
from dependencies import get_openai_interface, OpenaiInterface, get_mongodb_client, ConversationsDao, NotificationsInterface, get_notification_inerface

from app_logging import logger


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
    openai_client: OpenaiInterface  = Depends(get_openai_interface), 
    db: ConversationsDao = Depends(get_mongodb_client),
    notifications:NotificationsInterface = Depends(get_notification_inerface)
    ) -> ChatResponse:
    
    
    controller = ChatsController(
        db=db,
        notifications=notifications,
        openai_client=openai_client
    )

    try:
        return controller.handle_user_question(
            question = QuestionDto(
                content=question.content,
                role=question.role
                ),
            conversation_id=conversation_id
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(e)
        notifications.send_error_notification("Something went wrong while processing a request to openai.")
        raise HTTPException(detail="Something went wrong while processing your request, please try again later", status_code=503)


@app.get("/chat")
def chat_get(
    conversation_id: str,
    hash: str,
    openai_client: OpenaiInterface  = Depends(get_openai_interface), 
    db: ConversationsDao = Depends(get_mongodb_client),
    notifications:NotificationsInterface = Depends(get_notification_inerface)
):
    
    controller = ChatsController(
        db=db,
        notifications=notifications,
        openai_client=openai_client
    )


    return controller.get_chat(
            conversation_id=conversation_id,
            hash=hash
        )
    
    



app.mount("/", StaticFiles(directory="frontend_dist",  html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
