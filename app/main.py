from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

import os
import uvicorn
from typing import Optional
from fastapi.staticfiles import StaticFiles


from app.models import UserInput, ChatResponse, QuestionDto
from app.dependencies import ChatsController, get_chat_controller

from app.logging.app_logging import logger


app = FastAPI()

FastAPIInstrumentor.instrument_app(app)


origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://roel-huijskens.azurewebsites.net/" "http://roel-huijskens.com/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dir = "app/frontend_dist"


@app.post("/chat")
def chat(
    question: UserInput,
    conversation_id: Optional[str] = None,
    chat_controller: ChatsController = Depends(get_chat_controller),
) -> ChatResponse:
    try:
        return chat_controller.handle_user_question(
            question=QuestionDto(content=question.content, role=question.role),
            conversation_id=conversation_id,
        )

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(e)
        chat_controller.notifications.send_error_notification(
            "Something went wrong while processing a request to openai."
        )
        raise HTTPException(
            detail=(
                "Something went wrong while processing your request, please try again later"  # noqa E501
            ),
            status_code=503,
        )


@app.get("/chat")
def chat_get(
    conversation_id: str,
    hash: str,
    chat_controller: ChatsController = Depends(get_chat_controller),
):
    return chat_controller.get_chat(conversation_id=conversation_id, hash=hash)


if os.path.isdir(frontend_dir):
    app.mount(
        "/", StaticFiles(directory=frontend_dir, html=True), name="static"
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
