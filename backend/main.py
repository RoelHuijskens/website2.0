import yaml
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core import Settings

from dotenv import load_dotenv

load_dotenv()

import uvicorn
import os
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles


import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


class Message(BaseModel):
    questionText: str


class UserInput(BaseModel):
    message: Message
    sender: str
    


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Document
from llama_index.core import PromptTemplate
from llama_index.llms.openai import OpenAI


# LLM (gpt-4)
gpt4 = OpenAI(temperature=1, model="gpt-4")

with open("./knowledge_bank/my_info.yml", 'r') as file:
    my_info = yaml.safe_load(file)

documents = []

for info in my_info['info']:
    documents.append(Document(doc_id=info['title'], text=info['text']))

print(documents)
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine(similarity_top_k=5,similarity=0.6, llm=gpt4)


prompt_template = PromptTemplate("""
    You are a bot called Roel Huijskens, the virtual counterpart of the Real Roel huijskens.
    Using the following context: {context_str} give an answer to the question: {query_str} to the best of your ability.
    If you are not sure about the answer, answer with I am not sure, would you like to ask the real Roel?
    Be polite and enthusiastic in your response, try to respond in 3 to 4 sentences at most, shorter if possible.
""")

query_engine.update_prompts({"response_synthesizer:text_qa_template":prompt_template})
print(query_engine.get_prompts().keys())
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
def chat(questions: List[UserInput]):
    # Use LlamaIndex to answer the user's question
    answer = query_engine.query(questions[-2].message.questionText)
    return UserInput(
        message=Message(questionText=str(answer)),
        sender="bot"
    )

    #
    # return {"answer": answer}

@app.post("/load_data")
def load_data():
    # Reload the vector database and load data from directory and LinkedIn page
    index.reload_data()
    return {"message": "Data loaded successfully"}

app.mount("/", StaticFiles(directory="frontend_dist",  html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
