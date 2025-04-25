"""User routes for the Todo application. Handles user management and authentication functionality."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status
from models import Users
from database import SessionLocal
from pydantic import BaseModel

from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PasswordUpdateRequest(BaseModel):
    """Schema for password update requests."""

    password: str = Query(..., min_length=5, max_length=24)
    new_password: str = Query(..., min_length=5, max_length=24)


@router.get("/get_user", status_code=status.HTTP_200_OK)
async def get_user(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get current user information from the database."""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed"
        )

    user_model = db.query(Users).filter(Users.username == user.get("username")).first()
    if user_model is not None:
        return user_model
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_request: PasswordUpdateRequest,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change the current user's password after verifying the current password."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    user_model = db.query(Users).filter(Users.username == user.get("username")).first()

    if user_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not bcrypt_context.verify(
        password_request.password, str(user_model.hashed_password)
    ):
        raise HTTPException(status_code=401, detail="Authentication failed")

    setattr(
        user_model,
        "hashed_password",
        bcrypt_context.hash(password_request.new_password),
    )
    db.add(user_model)
    db.commit()
