from fastapi import APIRouter, status, HTTPException
from src.services import posts_service as posts_service
from src.pydantic_models import posts_models as posts
from src.database import psycopg


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

@router.put("/update/{post_id}", status_code=status.HTTP_200_OK, response_model=posts.PostFull)
def update(post_id: int, body: posts.PostUpdate):
    return posts_service.update_post(post_id, body)

@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: int):
    return posts_service.delete_post(post_id)

cursor = psycopg.cursor
conn = psycopg.conn
@router.get('/{username}')
def get_user(username: str):
    try:
        cursor.execute("""SELECT * from posts WHERE user = %s """, (username,))
        posts = cursor.fetchall()
        if posts is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        return posts
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"DB error: {str(e)}")  