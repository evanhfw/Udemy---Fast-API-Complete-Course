"""REST API for managing a book collection with CRUD operations."""

from typing import List, Dict

from fastapi import FastAPI, Body

BOOKS: List[Dict[str, str]] = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "science"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "math"},
    {"title": "Title Five", "author": "Author Five", "category": "math"},
    {"title": "Title Six", "author": "Author Two", "category": "math"},
]

app = FastAPI()


@app.get("/books/fetch/")
async def fetch_all_books_by_author_query(book_author: str):
    """Fetch books by author using query parameter."""
    books_to_return = []
    for book in BOOKS:
        if book.get("author", "").casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/fetch/{book_author}")
async def fetch_all_books_by_author_path(book_author: str):
    """Fetch books by author using path parameter."""
    books_to_return = []
    for book in BOOKS:
        if book.get("author", "").casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books")
async def read_all_books():
    """Get all books."""
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    """Get a book by title."""
    for book in BOOKS:
        if book.get("title", "").casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    """Get books by category using query parameter."""
    books_to_return = []

    for book in BOOKS:
        if book.get("category", "").casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    """Get books by author and category."""
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author", "").casefold() == book_author.casefold()
            and book.get("category", "").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    """Add a new book to the collection."""
    BOOKS.append(new_book)


@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    """Update an existing book by title."""
    for i, book in enumerate(BOOKS):
        if book.get("title", "").casefold() == updated_book.get("title", "").casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    """Delete a book by title."""
    for i, book in enumerate(BOOKS):
        if book.get("title", "").casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
