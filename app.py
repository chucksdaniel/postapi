from fastapi import  FastAPI

from . import models
from .database import engine
from .router import posts, users, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

"""Function that find a post by Id in an array"""
@app.get("/")
async def read_root():
    return {"Message": " Hello World! Welcome to the Learning platform!"}

