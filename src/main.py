from fastapi import FastAPI
from src.routes.posts import posts
from src.routes.user import user
from src.services import authservice as auth

app = FastAPI(title="Reddit API", 
              description="A simple API for Reddit",
              version="1.0.0")

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
def homepage():
    return {"message": "Welcome to Reddit!", "quote": "The heart of the Internet", "status": "success"}

@app.get("/signup")
def create_new_user():  # Removed async/await to fix runtime error
    return auth.create_new()

@app.get("/login")
def user_login():  # Removed async/await to fix runtime error
    return auth.verify_user()