from fastapi import APIRouter
import requests
from pydantic import BaseModel
from ..services.chat_response_gen import chatbot
from ..services.chat_response_gen import get_retriver_tool, define_graph
from .wordpress_routes import fetch_documents_from_wordpress


class ChatRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/chat")
def chat(requests: ChatRequest):

    docs = fetch_documents_from_wordpress("http://localhost/RagAssessBot/wp-json/store_chunk_docs/v1/get-documents")
    if docs:
        print("Docs from chatpbdfiogsdf",docs)
        tools = get_retriver_tool(docs)
        graph = define_graph(tools)
       
        user_query = requests.query
        # response = f"Your query was: {user_query}. Backend is working fine!"
        # response = run_conversation(user_query)
        response = chatbot(user_query, graph=graph)

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
                # "response":response,
            }
        }