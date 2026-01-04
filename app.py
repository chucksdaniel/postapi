from typing import List
from fastapi import Body, status, Response, HTTPException, FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import models, schema
from .database import engine, get_db
from .utility import hash_password
from .router import posts, users, auth

# from psycopg2.extras import RealDictCursor

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

"""Function that find a post by Id in an array"""
@app.get("/")
async def read_root():
    return {"Message": " Hello World! Welcome to the Learning platform!"}

