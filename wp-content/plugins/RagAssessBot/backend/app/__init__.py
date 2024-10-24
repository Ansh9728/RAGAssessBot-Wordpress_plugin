from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import chatbot
from .routes import posts
from .routes import wordpress_routes

app =FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chatbot.router)
app.include_router(posts.router)
app.include_router(wordpress_routes.router)
# app.include_router(wordpress_routes.router1)


@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Bot Application"}

print("FastAPI app initialized")