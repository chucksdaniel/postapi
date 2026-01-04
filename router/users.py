from fastapi import Body, status, Response, HTTPException, FastAPI, Depends, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema
from ..utility import hash_password

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

""" Create a new user route """
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
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

@router.get("/{user_id}", response_model=schema.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {user_id} does not exist"
        )
    return user

""" Get all users """
@router.get("/") # , response_model=List[schema.UserOut]
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users