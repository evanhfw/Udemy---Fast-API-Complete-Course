"""Admin routes for the Todo application. Provides admin-specific functionality to manage todos."""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/todo", status_code=status.HTTP_200_OK)
async def get_todos(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all todos from the database. Admin access only."""
    if current_user is None or current_user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return db.query(Todos).all()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int = Path(..., description="The ID of the todo to delete"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if current_user is None or current_user.get("role") != "admin":
        raise HTTPException(status_code=401, detail="Unauthorized")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        db.delete(todo_model)
        db.commit()
