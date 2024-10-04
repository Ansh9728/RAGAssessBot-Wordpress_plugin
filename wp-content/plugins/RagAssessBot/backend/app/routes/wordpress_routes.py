from fastapi import APIRouter
from pydantic import BaseModel 
from fastapi import HTTPException
import json
from langchain_community.vectorstores import Chroma
from app.services.wordpress_posts import fetch_wordpress_posts
from app.services.vectordb import get_documents, get_retriver_tool
from app.services.vectordb import get_embedding_model
# from services.wordpress_posts import get_post_details
from app.services.vectordb import store_posts_in_vectordb


# Model to receive site URL
class SiteUrlDataRequest(BaseModel):
    site_url: str


router = APIRouter(
    prefix="/site",
    tags=['sites']
)
# we use any database for store better result
# stored_documents = {}
retriver_tools = []

@router.post("/")
def receive_site_url(request: SiteUrlDataRequest):
    site_url = request.site_url

    try:
        wordpress_posts = fetch_wordpress_posts(site_url)

        documents = get_documents(wordpress_posts, site_url)

        # stored_documents[site_url] = documents

        retriver = get_retriver_tool(documents)
        retriver_tools.append(retriver)

        return {"message":"Data Fetched succussfully", 'Data':wordpress_posts}


    except HTTPException as e:
        return {"message":"Failed to Fetch the Data", "details":str(e)}
    
router1 = APIRouter(
    prefix="/tools",
)

@router1.get("/")
def get_document_posts():
    try:
        tools = retriver_tools[0]

        if tools is None:
            raise HTTPException(status_code=500, detail="Tools is Not present")
        
        return {"Message": "Tools Found", "tools":tools}

    except HTTPException as e:
        raise e