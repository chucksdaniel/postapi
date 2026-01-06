from typing import List
from fastapi import Body, status, Response, HTTPException, FastAPI, Depends, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # This prints the query object the real query is executed when we call .all()
    print(db.query(models.Post))
    return posts

""" Function that Gets current user's posts only """
@router.get("/my/posts", response_model=List[schema.Post])
def get_my_posts(
    db: Session = Depends(get_db), 
    current_user: int = Depends(get_current_user)
    ):
    """
    Docstring for get_my_posts
    
    :param db: Description
    :type db: Session
    :param current_user: Description
    :type current_user: int
    """
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # This prints the query object the real query is executed when we call .all()
    print(db.query(models.Post))
    return posts

# This can be used to get the latest post but also can be achieved using sorting
@router.get("/latest", response_model=schema.Post)
def get_latest_post(db: Session = Depends(get_db)):
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return {"Latest Post": latest_post}

# Method 1 to handle 404 error using status code
@router.get("/{post_id}", response_model=schema.Post)
def read_post(
    post_id: int, response: Response, 
    q: str | None = None, db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    print(f"Post ID: {post_id} and type of data {type(post_id)}")
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": f"Post with id: {post_id} was not found"}
    return post

# Method 2 to handle 404 error using HTTPExceptione
@router.get("/{post_id}", response_model=schema.Post)
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
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(
    new_post: schema.PostCreate, db: Session = Depends(get_db), 
    current_user: int = Depends(get_current_user)
  ):
    print(f"pydantic: {new_post}")
    # post = models.Post(
    #     title=new_post.title,
    #     content=new_post.content,
    #     published=new_post.published
    # ) # Not efficient when there are many fields

    # Unpacking the dictionary ease to use when there are many fields
    print(f"Current User: {current_user}")
    post = models.Post(owner_id=current_user.id, **new_post.dict())  # Unpacking the dictionary
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Update a post
@router.put("/{post_id}", response_model=schema.Post)
def update_post(
    post_id: int, updated_post: schema.PostCreate, 
    db: Session = Depends(get_db), current_user: int = Depends(get_current_user)
):
    print(f"type(post_id) in the update func : {type(post_id)}")
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_query)
    post = post_query.first() # Execute the query to get the post
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {post_id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    """
    What is being done here is that we are updating 
    the post with the data from updated_post
    Put method works however it replaces all the fields 
    whlie Patch only updates the specified fields
    """
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

# Delete a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, db: Session = Depends(get_db), 
    current_user: int = Depends(get_current_user)
    ):
    print(type(post_id))
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    print(post_query)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id: {post_id} does not exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(
    status_code=200,
    content={"message": f"Post with id {post_id} has been deleted"}
    )