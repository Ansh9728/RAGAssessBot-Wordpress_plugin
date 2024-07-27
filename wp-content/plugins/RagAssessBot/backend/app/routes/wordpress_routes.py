from fastapi import APIRouter
from pydantic import BaseModel 
from fastapi import HTTPException
import json
from services.wordpress_posts import fetch_wordpress_posts_data



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
    # Process the site URL as needed
    # print('site url',site_url)
    # return {"message": site_url}

    try:
        post_data = fetch_wordpress_posts_data(site_url)
        post = json.loads(post_data)
        pretiy = json.dumps(post,indent=4)
        print(pretiy)
    except HTTPException as e:
        return {"message":"Failed to Fetch the Data", "details":str(e)}