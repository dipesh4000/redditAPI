import logging
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from src.routes.posts import posts
from src.routes.user import user
from src.services import authservice, posts_service
from src.schemas import posts_models, users_models

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Reddit API", description="A simple API for Reddit", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(user.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/", response_model=list[posts_models.PostFull])
def homepage(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    return posts_service.get_all(limit, offset)


@app.post("/signup", response_model=users_models.UserCreated)
def create_new_user(user: users_models.UserCreate):
    return authservice.create_user(user)


@app.post("/login", response_model=users_models.Token)
def user_login(user: users_models.UserLogin):
    return authservice.verify_user(user)
