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

@router.put("/update/{post_id}", status_code=status.HTTP_200_OK, response_model=posts.PostFull)
def update(post_id: int, body: posts.PostUpdate):
    return posts_service.update_post(post_id, body)

@router.delete("/delete/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(post_id: int):
    return posts_service.delete_post(post_id)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), ):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user     