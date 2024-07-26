from fastapi import APIRouter
from pydantic import BaseModel 



# Model to receive site URL
class SiteUrlRequest(BaseModel):
    site_url: str


router = APIRouter(
    prefix="/site",
    tags=['sites']
)


@router.get("/")
def receive_site_url(request: SiteUrlRequest):
    site_url = request.site_url
    # Process the site URL as needed
    print('site url',site_url)
    return {"message": site_url}