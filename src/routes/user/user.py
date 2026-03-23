from fastapi import APIRouter, status, HTTPException
from src.services import posts_service as posts_service
from src.pydantic_models import posts_models as posts

router = APIRouter(
    prefix="/u",
    tags=['Users']
)

@router.get("/")
def get_posts():
    # 'raise' stops execution and sends the 502 error immediately
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Specify the username"
    )


@router.post("/post", status_code=status.HTTP_201_CREATED, response_model=posts.PostFull)
def post(body: posts.Post):
    return posts_service.create_post(body)

@router.put("/post_id/update", status_code=status.HTTP_201_CREATED, response_model=posts.PostFull)
def update(post_id: int, body: posts.Post):
    return posts_service.update_post(post_id, body)

@router.delete("/post_id/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: int):
    return posts_service.delete_post(post_id)