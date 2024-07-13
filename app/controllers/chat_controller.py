from domain.openai import OpenaiInterface
from nofications import NotificationsInterface
from dao import ConversationsDao
from models import QuestionDto, ConversationDto, ChatResponse
from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import Optional, List
from utils import generate_random_string, generate_security_hash
import os
import hashlib

class ChatsController(object):
    
    
    def __init__(self, db:ConversationsDao, notifications: NotificationsInterface, openai_client: OpenaiInterface) -> None:
        self.db = db
        self.notifications = notifications
        self.openai_client = openai_client
        
        
    
    def _check_recent_chats_limit(self, question: QuestionDto):
        if self.db.get_recent_chats_count(datetime.now() - timedelta(hours=1)) > 30:
            self.notifications.send_update_notification(f"Someone triggerd the max conversations count with question: {question.content}")
            raise HTTPException(detail="Appologies, too many conversations have been started in the last hour, please try again later.", status_code=503)
        
    
    def _check_current_chat_limit(self, current_chat: ConversationDto):
        
        if len(current_chat.questions) > 9:
            raise HTTPException(detail="It seems you have a lot of questions, let's connect via [**linkedin** (link)](https://nl.linkedin.com/in/roel-huijskens) I can answer more there.", status_code=503)
    
    
    def _get_or_create_conversation(self, question:QuestionDto ,conversation_id: Optional[str]) -> ConversationDto:
        
        if not conversation_id:
            conversation_id, start_time = generate_random_string()
            current_chat = ConversationDto(
                questions=[question],
                start_time=start_time,
                chat_id=conversation_id
            )
            self.db.create_chat(
                current_chat
            )
            admin_hash = generate_security_hash(seed=conversation_id)
            self.notifications.send_update_notification(f"Someone started a new conversation, see: https://roel-huijskens.azurewebsites.net/chat?conversation_id={conversation_id}&hash={admin_hash}")
        else:
            current_chat = self.db.get_chat_by_id(conversation_id)
            self.db.append_chat(
                question, current_chat.chat_id
            )
            
            self._check_current_chat_limit(current_chat=current_chat)
            
            if not current_chat:
                raise HTTPException(detail="Failed to retrieve specified chat, please try refreshing your page", status_code=404)
        return current_chat
            
    
    def _format_and_store_response(self, response:str, annotations:List[str], chat_id: str) -> ChatResponse:
        
        format_response = ChatResponse(
                content=response,
                role="bot",
                chat_id=chat_id,
            )

            
        self.db.append_chat(format_response, chat_id=format_response.chat_id, annotations=annotations)
            
        return format_response
        
    
    def handle_user_question(self, question: QuestionDto, conversation_id: Optional[str]) -> ChatResponse:
        
        
        self._check_recent_chats_limit(question)
        current_chat = self._get_or_create_conversation(question, conversation_id)
        
        response, annotations = self.openai_client.submit_assistant_question(
            chat_history=current_chat.questions,
            question = question
        )
    
        if response:
            return self._format_and_store_response(
                response=response, 
                annotations=annotations, 
                chat_id=current_chat.chat_id
                )
        else:
            raise HTTPException(detail="Appologies, something went wrong while communicating with openai, please try again later", status_code=503)        
        

    def get_chat(self, conversation_id: str, hash:str) -> dict[str, str]:
    
    
        

    
        if hash == generate_security_hash(conversation_id):
            chat = self.db.get_chat_by_id(conversation_id)
            if not chat:
                raise HTTPException(detail=f"Could not find chat {conversation_id}", status_code=404)
            
            chat.questions = [question.to_dict() for question in chat.questions]
            return chat.model_dump()
        
        else:
            raise HTTPException(detail="What on earth are you doing here?? Please leave", status_code=401)