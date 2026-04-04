from fastapi import FastAPI
from src.routes.posts import posts
from src.routes.user import user
from src.services import authservice as authservice
from src.services import posts_service as posts_service

app = FastAPI(title="Reddit API", 
              description="A simple API for Reddit",
              version="1.0.0")

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
def homepage():
    return posts_service.get_all()

@app.get("/signup")
def create_new_user():  # Removed async/await to fix runtime error
    return authservice.create_user()

@app.get("/login")
def user_login():  # Removed async/await to fix runtime error
    return authservice.verify_user()