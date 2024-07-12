
from pymongo import MongoClient
from typing import Optional, List
from models import ConversationDto, UserInput
from datetime import datetime

class ConversationsDao(object):
    
    
    def __init__(self, client: MongoClient) -> None:
        
        
        self.client = client
        
        
    def append_chat(self, question: UserInput, chat_id: str, annotations: Optional[List[str]] = None):
        db = self.client['PersonalWebsite']
        collection = db['Conversations']
        
        question_dict = question.to_dict()
        
        if annotations:
            question_dict["annotations"] = annotations
        
        collection.update_one(
            {"_id":chat_id},
            {
                "$push": {
                    "questions": question_dict
                }
            }
        )
    
    def get_chat_by_id(self, chat_id: str) -> ConversationDto:
        db = self.client['PersonalWebsite']
        collection = db['Conversations']
        chat = collection.find_one({'_id': chat_id})
        chat["chat_id"] = chat['_id']
        del chat['_id']
        return ConversationDto(**chat)
    
    
    def create_chat(self, conversation: ConversationDto):
        db = self.client['PersonalWebsite']
        collection = db['Conversations']
        collection.insert_one(
            {
                "_id": conversation.chat_id,
                "start_time": conversation.start_time,
                "questions": [conversation.questions[0].to_dict()]
            }
        )
        
    def get_recent_chats_count(self, threshold: datetime) -> int:
        db = self.client['PersonalWebsite']
        collection = db['Conversations']
        print(threshold)
        return collection.count_documents({
              "start_time": {
              "$gte": threshold
  }
        })
        
