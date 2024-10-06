# from fastapi import APIRouter
# from pydantic import BaseModel 
# from fastapi import HTTPException
# from langchain_community.vectorstores import Chroma
# from app.services.wordpress_posts import fetch_wordpress_posts
# from app.services.vectordb import get_documents, get_retriver_tool
# from app.services.vectordb import get_embedding_model
# # from services.wordpress_posts import get_post_details
# # from app.services.vectordb import store_posts_in_vectordb
# import requests

# # Model to receive site URL
# class SiteUrlDataRequest(BaseModel):
#     site_url: str


# router = APIRouter(
#     prefix="/site",
#     tags=['sites']
# )

# def store_in_wordpress_database(site_url, title, content):
#     url = f"{site_url}/wp-json/store_chunk_docs/v1/store-document"

#     payload = {
#         'title': title,
#         'content': content,
#         'source_url': site_url,
#     }
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()



# @router.post("/")
# def receive_site_url(request: SiteUrlDataRequest):
#     site_url = request.site_url

#     try:
#         wordpress_posts = fetch_wordpress_posts(site_url)

#         documents = get_documents(wordpress_posts, site_url)

#         for document in documents:
#             title = document.metadata['title']
#             content = document.page_content
#             store_in_wordpress_database(site_url=site_url, title=title, content=content)

#         return {"message":"Data Fetched succussfully", 'Data':wordpress_posts}


#     except HTTPException as e:
#         return {"message":"Failed to Fetch the Data", "details":str(e)}


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from app.services.wordpress_posts import fetch_wordpress_posts
from app.services.vectordb import get_documents
from langchain_core.documents.base import Document

# Model to receive site URL
class SiteUrlDataRequest(BaseModel):
    site_url: str

router = APIRouter(
    prefix="/site",
    tags=['sites']
)

def store_in_wordpress_database(site_url, title, content):
    url = f"{site_url}/wp-json/store_chunk_docs/v1/store-document"

    payload = {
        'title': title,
        'content': content,
        'source_url': site_url,
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        print("Stored document:", response.json())
        return response.json()
    except requests.exceptions.HTTPError as err:
        print("HTTP error occurred:", err)
    except Exception as err:
        print("An error occurred:", err)

@router.post("/")
def receive_site_url(request: SiteUrlDataRequest):
    site_url = request.site_url

    print("site url", site_url)

    try:
        wordpress_posts = fetch_wordpress_posts(site_url)
        documents = get_documents(wordpress_posts, site_url)

        # Store each document in the WordPress database
        for document in documents:
            title = document.metadata['title']
            content = document.page_content
            store_in_wordpress_database(site_url=site_url, title=title, content=content)

        return {"message": "Data fetched and stored successfully", 'Data': wordpress_posts}

    except HTTPException as e:
        return {"message": "Failed to fetch data", "details": str(e)}


def fetch_documents_from_wordpress(site_url):
    try:
        docs = []
        url = f"{site_url}/wp-json/store_chunk_docs/v1/get-documents"
        # response = requests.get(url, params={'source_url': site_url})
        response = requests.get(url)
    
        if response.status_code==200:
            print(response.json())
            json_response = response.json()

            doc = Document(
                page_content=json_response['content'],
                metadata={
                    "source":site_url,
                    "title": json_response.get('title')
                }
            )
            docs.append(doc)  
        return docs
    
    except HTTPException as e:
        raise(f"Exception occur at fetch_document {e}")
