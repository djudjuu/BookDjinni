from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship, delete


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str
    books: List["Book"] = Relationship(back_populates="recommender")


class BookCategoryLink(SQLModel, table=True):
    book_id: Optional[int] = Field(default=None, foreign_key="book.id", primary_key=True)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id", primary_key=True)

    # book: "Book" = Relationship(back_populates="category_links")
    # categories: "Category" = Relationship(back_populates="book_links")


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: str

    books: List["Book"] = Relationship(back_populates="categories", link_model=BookCategoryLink)
    # book_links: List[BookCategoryLink] = Relationship(back_populates="categories")
    


class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    isbn: Optional[str] = None

    recommended_by: Optional[int] = Field(default=None, foreign_key="user.id")
    recommender: Optional[User] = Relationship(back_populates="books")

    categories: List[Category] = Relationship(back_populates="books", link_model=BookCategoryLink)
    # category_links: List[BookCategoryLink] = Relationship(back_populates="books")

class Rating(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: int
    user_id: int
    rating: int
    comment: str


class RatingSystem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: int
    emoji: str


class Owns(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    book_id: Optional[int]= Field(default=None, foreign_key="book.id")
    type: str

ALL_MODELS = [User, Book, Rating, RatingSystem, Owns, Category, BookCategoryLink]
