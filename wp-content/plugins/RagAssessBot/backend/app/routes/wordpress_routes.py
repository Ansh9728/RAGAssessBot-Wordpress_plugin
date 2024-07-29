from fastapi import APIRouter
from pydantic import BaseModel 
from fastapi import HTTPException
import json
from services.wordpress_posts import fetch_wordpress_posts_data
from services.wordpress_posts import extract_post_details
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
        post_data = fetch_wordpress_posts_data(site_url)

        posts = extract_post_details(post_data)

        result = store_posts_in_vectordb(posts)
        print("esult ",result)

        return {"message":"Data Fetched succussfully", 'Data':result}


    except HTTPException as e:
        return {"message":"Failed to Fetch the Data", "details":str(e)}