from typing import List
from fastapi import Body, status, Response, HTTPException, FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import models, schema
from .database import engine, get_db
from .utility import hash_password

# from psycopg2.extras import RealDictCursor


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

"""Function that find a post by Id in an array"""
@app.get("/")
async def read_root():
    return {"Message": " Hello World! Welcome to the Learning platform!"}

@app.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # This prints the query object the real query is executed when we call .all()
    print(db.query(models.Post))
    return posts

# This can be used to get the latest post but also can be achieved using sorting
@app.get("/posts/latest", response_model=schema.Post)
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return {"Latest Post": latest_post}

# Method 1 to handle 404 error using status code
@app.get("/posts/{post_id}", response_model=schema.Post)
def read_post(
    post_id: int, response: Response, 
    q: str | None = None, db: Session = Depends(get_db)
):
    print(f"Post ID: {post_id} and type of data {type(post_id)}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id: {post_id} was not found"}
    return post

# Method 2 to handle 404 error using HTTPExceptione
@app.get("/posts/{post_id}", response_model=schema.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    print(f"Post ID: {post_id} and type of data {type(post_id)}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {post_id} was not found"
        )
    return {"post": post}

# Using Pydantic schema to validate request body
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(new_post: schema.PostCreate, db: Session = Depends(get_db)):
    print(f"pydantic: {new_post}")
    # post = models.Post(
    #     title=new_post.title,
    #     content=new_post.content,
    #     published=new_post.published
    # ) # Not efficient when there are many fields

    # Unpacking the dictionary ease to use when there are many fields
    post = models.Post(**new_post.dict())  # Unpacking the dictionary
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Update a post
@app.put("/posts/{post_id}", response_model=schema.Post)
def update_post(post_id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)):
    print(f"type(post_id) in the update func : {type(post_id)}")
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_query)
    post = post_query.first() # Execute the query to get the post
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {post_id} does not exist"
        )
    """
    What is being done here is that we are updating 
    the post with the data from updated_post
    Put method works however it replaces all the fields 
    whlie Patch only updates the specified fields
    """
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {"data": updated_post}

# Delete a post
@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    print(type(post_id))
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_query)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {post_id} does not exist"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(
    status_code=200,
    content={"message": f"Post with id {post_id} has been deleted"}
    )

""" Create a new user route """
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(new_user: schema.UserCreate, db: Session = Depends(get_db)):
    print(f"pydantic: {new_user}")

    # Hash the password - user.password
    hashed_password = hash_password(new_user.password)
    new_user.password = hash_password(new_user.password)

    user = models.User(**new_user.dict())  # Unpacking the dictionary
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@app.get("/users/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist"
        )
    return user

""" Get all users """
@app.get("/users") # , response_model=List[schema.UserOut]
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users