from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import Text,Optional
from datetime import datetime
from uuid import uuid4
app = FastAPI()

posts = []

#POST MODEL
class Post(BaseModel):
    id:Optional[str]
    title:str
    author:str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False
@app.get('/')
def read_root():
    return {"welcome": "welcome to my app"}

@app.get('/posts')
def get_post():
    return posts

@app.post('/posts')
def create_post(post:Post):
    post.id = str(uuid4())
    posts.append(post.dict())
    return posts

@app.get('/posts/{post_id}')
def get_post_by_id(post_id:str):
    for post in posts:
        if (post["id"] == post_id):
            return post
    raise HTTPException(status_code=404,detail="Post Not Found")

@app.delete('/delete/post/{post_id}')
def delete_post(post_id:str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": 'Post deleted '}

    raise HTTPException(status_code=404,detail="Post Not Found")

@app.put('/posts/{post_id}')
def update_post(post_id:str, updatePost:Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updatePost.title
            posts[index]["content"] = updatePost.content
            posts[index]["author"] = updatePost.author

            return {"message": 'Post updated ',"post": posts[index]}
    raise HTTPException(status_code=404,detail="Post Not Found")
