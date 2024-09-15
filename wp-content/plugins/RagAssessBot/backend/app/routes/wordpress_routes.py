from fastapi import APIRouter
from pydantic import BaseModel 
from fastapi import HTTPException
import json
from services.wordpress_posts import fetch_wordpress_posts
from services.vectordb import get_documents
# from services.wordpress_posts import get_post_details
from services.vectordb import store_posts_in_vectordb


# Model to receive site URL
class SiteUrlDataRequest(BaseModel):
    site_url: str


router = APIRouter(
    prefix="/site",
    tags=['sites']
)


@router.post("/")
def receive_site_url(request: SiteUrlDataRequest):
    site_url = request.site_url

    try:
        wordpress_posts = fetch_wordpress_posts(site_url)
        # print(wordpress_posts)

        documents = get_documents(wordpress_posts, site_url)

        vector_index_loc = store_posts_in_vectordb(documents)

        return {"message":"Data Fetched succussfully", 'Data':wordpress_posts}


    except HTTPException as e:
        return {"message":"Failed to Fetch the Data", "details":str(e)}