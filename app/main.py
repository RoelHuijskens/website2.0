
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware





import uvicorn
from typing import List
from fastapi.staticfiles import StaticFiles


from models import UserQuestion, UserInput

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))



from dependencies import get_openai_interface, OpenaiInterface


app = FastAPI()

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(questions: List[UserInput], interface: OpenaiInterface  = Depends(get_openai_interface)) -> UserInput:
    try:
        interface.submit_assistant_question(
            chat_history=questions
        )
    except Exception as e:
        logging.info("Oh oh")
        logging.error(f"Failed to sent request to open ai with: {e}")



app.mount("/", StaticFiles(directory="frontend_dist",  html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
