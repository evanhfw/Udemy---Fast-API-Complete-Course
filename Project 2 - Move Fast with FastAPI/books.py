"""FastAPI application for managing a collection of books."""

from typing import Optional, List

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


class BookRequest(BaseModel):
    """Pydantic model for book request validation and serialization."""

    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "codingwithevan",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2025,
            }
        }
    }


class Book(BaseModel):
    """Book model representing a book entity in the application."""

    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int


app = FastAPI()

BOOKS: List[Book] = [
    Book(
        id=1,
        title="Computer Science Pro",
        author="codingwithroby",
        description="A very nice book!",
        rating=5,
        published_date=2030,
    ),
    Book(
        id=2,
        title="Be Fast with FastAPI",
        author="codingwithroby",
        description="A great book!",
        rating=5,
        published_date=2030,
    ),
    Book(
        id=3,
        title="Master Endpoints",
        author="codingwithroby",
        description="A awesome book!",
        rating=5,
        published_date=2029,
    ),
    Book(
        id=4,
        title="HP1",
        author="Author 1",
        description="Book Description",
        rating=2,
        published_date=2028,
    ),
    Book(
        id=5,
        title="HP2",
        author="Author 2",
        description="Book Description",
        rating=3,
        published_date=2027,
    ),
    Book(
        id=6,
        title="HP3",
        author="Author 3",
        description="Book Description",
        rating=1,
        published_date=2026,
    ),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    """Get all books."""
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=-1)):
    """Get a single book by ID."""
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail=f"book_id {str(book_id)} not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    """Get books filtered by rating."""
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    """Create a new book."""
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    """Generate a new ID for a book and return the book."""
    book.id = BOOKS[-1].id + 1 if len(BOOKS) > 0 else 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    """Update an existing book."""
    book_changed = False
    for i, existing_book in enumerate(BOOKS):
        if existing_book.id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True
            break  # Exit loop once the book is found and updated
    if not book_changed:
        raise HTTPException(status_code=404, detail=f"book_id {str(book.id)} not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=-1)):
    """Delete a book by ID."""
    book_deleted = False
    for i, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail=f"book_id {str(book_id)} not found")


@app.get("/books/fetch-by-published-date/", status_code=status.HTTP_200_OK)
async def fetch_by_published_date(published_date: int = Query(gt=1990, lt=2031)):
    """Get books filtered by published date."""
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return
