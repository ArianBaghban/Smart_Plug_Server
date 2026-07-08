from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.user import User
from app.schemas.user import UserSchema

from app.core.security import hash_password, verify_password
from app.core.jwt import create_token


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(
    user: UserSchema,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_user:
        return {
            "message": "Username already exists"
        }


    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "username": new_user.username
    }



@router.post("/login")
async def login(
    user: UserSchema,
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()


    if not db_user:
        return {
            "message": "Invalid username or password"
        }


    if not verify_password(
        user.password,
        db_user.password
    ):
        return {
            "message": "Invalid username or password"
        }


    token = create_token({
        "username": db_user.username
    })


    return {
        "access_token": token,
        "token_type": "bearer"
    }