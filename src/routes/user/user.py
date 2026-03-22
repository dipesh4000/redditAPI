from fastapi import APIRouter, status, HTTPException
from src.services import user_service as user_service
from src.pydantic_models import users_models as user
from src.pydantic_models import posts_models as posts

router = APIRouter(
    prefix="/u",
    tags=['Users']
)

@router.get("/")
def get_posts():
    # 'raise' stops execution and sends the 502 error immediately
    raise HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Specify the username"
    )
@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=posts.postfull)
def post(body: user.post):
    return user_service.user_post(body)