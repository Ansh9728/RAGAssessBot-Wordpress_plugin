from fastapi import APIRouter
import requests
from pydantic import BaseModel
from langchain_core.documents import Document
from ..services.chat_response_gen import chatbot_response_generation
from ..services.vectordb import get_retriver
from .wordpress_routes import fetch_documents_from_wordpress


class ChatRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/chat")
def chat(requests: ChatRequest):
    # url hard code we have to fix
    docs = fetch_documents_from_wordpress("http://localhost/RagAssessBot/wp-json/store_chunk_docs/v1/get-documents?source_url=http://localhost/RagAssessBot") # Hard code this part

    if docs:
        # print("Docs from Wordspress_site",docs)
        retriever = get_retriver(docs)
        
        user_query = requests.query

        response = chatbot_response_generation(question=user_query, retriever=retriever)
        print("res", response)

        return {
            "success":True,
            "data":{
                "response":response,
            }
        }
    
    return {
            "error":False,
            "data":{
                "error":"No documents found"
            }
        }