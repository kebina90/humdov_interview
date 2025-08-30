from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import database
from pydantic import BaseModel, ConfigDict
from contextlib import asynccontextmanager


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    id: int
    username: str
    model_config = ConfigDict(from_attributes=True)

class PostCreate(BaseModel):
    title: str
    content: str
    tag: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    tag: str
    model_config = ConfigDict(from_attributes=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=database.engine)
    yield

app = FastAPI(title="Humdov Interview Test API", version="1.0.0", lifespan=lifespan)

# endpoit to create new user
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(database.get_db)):
    # checking if username already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# endpoint to create new post
@app.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(database.get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# endpoint for a user to like post
@app.post("/users/{user_id}/like/{post_id}")
def like_post(user_id: int, post_id: int, db: Session = Depends(database.get_db)):

    # getting user and post from database
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not db_user or not db_post:
        raise HTTPException(status_code=404, detail="User or Post not found")

    # adding post to user liked post
    if db_post not in db_user.liked_posts:
        db_user.liked_posts.append(db_post)
        db.commit()
        return {"message": f"User #{user_id} liked post #{post_id}"}
    else:
        return {"message": "Post already liked"}

# endpoint to get persolized feed from a user
@app.get("/users/{user_id}/feed", response_model=List[PostResponse])
def get_personalized_feed(user_id: int, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    all_posts = db.query(models.Post).all()

    # user tags
    user_liked_tags = [post.tag for post in db_user.liked_posts]

    if not user_liked_tags:
        return all_posts[::-1]

    # posts with tags the user likes get higher priority for scores
    scored_posts = []
    for post in all_posts:
        score = 1 if post.tag in user_liked_tags else 0
        scored_posts.append((post, score))

    # sort post by scores
    scored_posts.sort(key=lambda x: (x[1], x[0].id), reverse=True)
    personalized_feed = [post for post, score in scored_posts]
    return personalized_feed

# get all users
@app.get("/users/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

# get all posts
@app.get("/posts/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).all()
    return posts