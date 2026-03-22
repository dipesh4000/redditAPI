from fastapi import APIRouter, status, HTTPException

router = APIRouter(
    prefix="/u",
    tags=['Users']
)

@router.get("/",status_code=status.HTTP_200_OK)
def get_posts():
    return HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Specify the username")