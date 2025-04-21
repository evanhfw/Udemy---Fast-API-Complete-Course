"""FastAPI Todo application with SQLAlchemy ORM."""

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from starlette import status

import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=10, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: Session = Depends(get_db)):
    return db.query(Todos).all()


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} not found.")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, db: Session = Depends(get_db)):
    todo_model = Todos(**todo_request.model_dump())
    db.add(todo_model)
    db.commit()


@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    todo_id: int, todo_request: TodoRequest, db: Session = Depends(get_db)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo ID {todo_id} not found.")

    # type: ignore
    todo_model.title = todo_request.title  # type: ignore
    todo_model.description = todo_request.description  # type: ignore
    todo_model.priority = todo_request.priority  # type: ignore
    todo_model.complete = todo_request.complete  # type: ignore
    db.add(todo_model)
    db.commit()
