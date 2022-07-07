# fastapi routes for books
from fastapi import APIRouter, Depends, HTTPException, Body
from database import Book, User, engine, Category
from database.models import (
    BookRead, BookCreate, BookReadWithCategories, CategoryReadWithBooks, Category, CategoryRead, CategoryReadWithBooks,
    CategoryReadWithBookIds, BookUpdate

)
from sqlmodel import Session, select
from typing import List



book_app = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@book_app.get("/")
def read_root():
    return {"Hello": "World"}

# read route to get all books
@book_app.get("/books", response_model=List[BookReadWithCategories])
def read_books(session = Depends(get_session)):
    # get all books from session
    books = session.exec(select(Book)).all()
    return books

# read route to get a book by id
@book_app.get("/books/{book_id}", response_model=BookReadWithCategories)
def read_book(book_id: int, session = Depends(get_session)):
    # get book by id from session
    book = session.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# update route to update a book by id
@book_app.put("/books/{book_id}", response_model=BookReadWithCategories)
def update_book(book_id: int, book_update: BookUpdate, session = Depends(get_session)):
    # get book by id from session
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # update book
    book_data = book_update.dict(exclude_unset=True)
    for key, value in book_data.items():
        setattr(db_book, key, value)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# update route to update the categories of a book
@book_app.put("/books/{book_id}/categories", response_model=BookReadWithCategories)
def update_book_categories(book_id: int, categories: List[int] = Body(..., embed=True), session = Depends(get_session)):
    # get book by id from session
    db_book = session.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    # update book
    db_book.categories = []
    for category_id in categories:
        category = session.query(Category).filter(Category.id == category_id).first()
        if category is None:
            raise HTTPException(status_code=404, detail="Category not found")
        db_book.categories.append(category)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# post a new book
@book_app.post("/books", response_model=BookReadWithCategories)
def create_book(book: BookCreate, session = Depends(get_session)):
    if not book.recommended_by:
        book.recommended_by = 1
    db_book = Book.from_orm(book)
    # TODO check if a similar book already exists, check title and author
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# get endpoint to get all unique authors
@book_app.get("/authors", response_model=List[str])
def read_authors(session = Depends(get_session)):
    authors = session.exec(select(Book.author)).all()
    return list(set(authors))

# route to get all categories with response model CategoryReadWithBooks
@book_app.get("/categories", response_model=List[CategoryReadWithBooks])
def read_categories(session = Depends(get_session)):
    # get all categories from session
    categories = session.exec(select(Category)).all()
    # return [Category.CategoryReadWithBookIds(c) for c in categories]
    return categories

# read route to get a user by id
@book_app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# read route to get all books of a user
@book_app.get("/users/{user_id}/books", response_model=List[BookReadWithCategories])
def read_user_books(user_id: int, session = Depends(get_session)):
    # pass
    user = session.get(User, user_id)
    print('us', user.books)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.books

