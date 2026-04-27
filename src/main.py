import logging
from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.routes.posts import posts
from src.routes.user import user
from src.services import authservice, posts_service
from src.schemas import posts_models, users_models
from src.database.session import engine, get_db
from src.database.session import Base
from src.models import models  # noqa: F401 — ensures models are registered

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

Base.metadata.create_all(bind=engine)

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
def homepage(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)):
    return posts_service.get_all(db, limit, offset)


@app.post("/signup", response_model=users_models.UserCreated)
def create_new_user(user: users_models.UserCreate, db: Session = Depends(get_db)):
    return authservice.create_user(user, db)


@app.post("/login", response_model=users_models.Token)
def user_login(user: users_models.UserLogin, db: Session = Depends(get_db)):
    return authservice.verify_user(user, db)
