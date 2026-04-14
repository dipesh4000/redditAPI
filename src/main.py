from fastapi import FastAPI
from src.routes.posts import posts
from src.routes.user import user
from src.services import authservice, posts_service
from src.pydantic_models import users_models


app = FastAPI(title="Reddit API", 
              description="A simple API for Reddit",
              version="1.0.0")

app.include_router(posts.router)
app.include_router(user.router)

@app.get("/")
def homepage():
    return posts_service.get_all()

@app.post("/signup", response_model=users_models.UserCreated)
def create_new_user(user: users_models.UserCreate):
    print(user)  # Removed async/await to fix runtime error
    return authservice.create_user(user)

@app.post("/login", response_model=users_models.Token)
def user_login(user: users_models.UserLogin):  # Removed async/await to fix runtime error
    return authservice.verify_user(user)