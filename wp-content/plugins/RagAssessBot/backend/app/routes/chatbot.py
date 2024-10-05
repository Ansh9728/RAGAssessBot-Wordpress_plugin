from fastapi import APIRouter
import requests
from pydantic import BaseModel
from ..services.chat_response_gen import chatbot


class ChatRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/chat")
def chat(requests: ChatRequest):
    user_query = requests.query
    response = f"Your query was: {user_query}. Backend is working fine!"
    # response = run_conversation(user_query)
    # response = chatbot(user_query)

    return {
        "success":True,
        "data":{
            "response":response,
        }
    }