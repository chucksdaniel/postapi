from fastapi import status, Response, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schema, oauth2
from ..utility import hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

""" Create a new user route """
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
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

# Initial login route using UserLogin schema
# @router.post("/login", response_model=schema.Token)
# def login(user_credentials: schema.UserLogin, db: Session = Depends(get_db)):
#     print(f"User login attempt: {user_credentials.email}")
#     # Check if user exists
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
#     print("User fetched from DB:", user)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid Credentials"
#         )
#     # This method failed: if not user or not user.password == hash_password(user_credentials.password)
#     print("Password verification result:", user.password == hash_password(user_credentials.password))
#     # Alternative way using verify_password function separately
#     if not verify_password(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Invalid Credentials"
#         )
    
#     access_token = oauth2.create_access_token(data={"user_id": user.id})
#     print("Access Token created:", access_token)

#     return {"access_token": access_token, "token_type": "bearer"}

""" 
Function: 
The OAuth2PasswordRequestForm dependency is used to handle form data for user login.
Revised login route using OAuth2PasswordRequestForm 
Dependency Data is passed as form data not through JSON body
"""
@router.post("/login", response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(f"User login attempt: {user_credentials.username}")
    # Check if user exists
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print("User fetched from DB:", user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    # This method failed: if not user or not user.password == hash_password(user_credentials.password)
    print("Password verification result:", user.password == hash_password(user_credentials.password))
    # Alternative way using verify_password function separately
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid Credentials"
        )
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    print("Access Token created:", access_token)

    return {"access_token": access_token, "token_type": "bearer"}