from fastapi import APIRouter
import requests
from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/chat")
def chat(requests: ChatRequest):
    user_query = requests.query
    response = f"Your query was: {user_query}. Backend is working fine!"

    return {
        "success":True,
        "data":{
            "response":response,
        }
    }