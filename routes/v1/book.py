# fastapi routes for books
from fastapi import APIRouter, Depends, HTTPException
from database import Book, User, engine
from sqlmodel import Session, select

book_app = APIRouter()

def get_session():
    with Session(engine) as session:
        yield session

@book_app.get("/")
def read_root():
    return {"Hello": "World"}

# read route to get all books
@book_app.get("/books")
def read_books(skip: int = 0, limit: int = 1000, session = Depends(get_session)):
    # get all books from session
    books = session.exec(select(Book)).all()
    return books

# read route to get a user by id
@book_app.get("/users/{user_id}")
def read_user(user_id: int):
    pass
    # user = User.get(User.id == user_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # return user

# read route to get all books of a user
@book_app.get("/users/{user_id}/books")
def read_user_books(user_id: int, skip: int = 0, limit: int = 1000):
    pass
    # user = User.get(User.id == user_id)
    # if not user:
    #     raise HTTPException(status_code=404, detail="User not found")
    # return user.books.offset(skip).limit(limit).all()

