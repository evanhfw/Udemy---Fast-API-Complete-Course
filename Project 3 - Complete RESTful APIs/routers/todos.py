"""FastAPI Todo routerlication with SQLAlchemy ORM."""

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from starlette import status
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter()


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    """Schema for todo creation and update requests."""

    title: str = Field(min_length=3)
    description: str = Field(min_length=10, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = Field(default=False)


@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Retrieve all todos for the authenticated user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return db.query(Todos).filter(Todos.owner_id == user.get("id")).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(
    todo_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Retrieve a specific todo by ID for the authenticated user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} not found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_request: TodoRequest = Body(...),
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new todo for the authenticated user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_request: TodoRequest = Body(...),
    todo_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Update an existing todo by ID for the authenticated user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} not found.")

    # type: ignore
    todo_model.title = todo_request.title  # type: ignore
    todo_model.description = todo_request.description  # type: ignore
    todo_model.priority = todo_request.priority  # type: ignore
    todo_model.complete = todo_request.complete  # type: ignore
    db.add(todo_model)
    db.commit()


@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """Delete a todo by ID for the authenticated user."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed")
    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} not found.")
    db.delete(todo_model)
    db.commit()
