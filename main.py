from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import PlainTextResponse
import secrets
from typing import List, Optional
from fastapi import FastAPI, requests
from starlette import status
from starlette.responses import Response
from pydantic import BaseModel

app=FastAPI()
security = HTTPBasic()
posts_db = []

class Posts(BaseModel):
    author: str
    title: str
    content:str
    creation_datetime:str


@app.get('/ping')
def read_ping():
    return "Pong"

@app.get('/home')
def welcome_home():
    with open ("home.html","r",encoding="utf-8") as file:
        html_content=file.read()
        return Response(content=html_content,status_code=200)
"""
    <html>
        
        <body>
            <h1>Welcome home!</h1>
        </body>
    </html>
    """
@app.get('/{full_path=path}')
def  catch_all(full_path:str):
    with open("not_found.html","r",encoding="utf-8") as file:
        html_content=file.read()
        return Response(content=html_content,status_code=404)
        """
    <html>
        
        <body>
            <h1>404 NOT FOUND</h1>
        </body>
    </html>
    """




@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(posts: List[Posts]):
    posts_db.extend(posts)
    return posts_db

@app.get("/posts")
async def get_posts():
    return posts_db

@app.put("/posts")
async def update_or_add_post(post: Posts):
    for i, p in enumerate(posts_db):
        if p.title == post.title:
            posts_db[i] = post
            return posts_db
    posts_db.append(post)
    return posts_db


@app.get("/ping", response_class=PlainTextResponse)
def ping():
    return "pong"

@app.get("/ping/auth", response_class=PlainTextResponse)
def ping_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "123456")

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Accès refusé : identifiants invalides",
            headers={"WWW-Authenticate": "Basic"},
        )

    return "pong"
