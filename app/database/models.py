from typing import Optional, List, Dict
from sqlmodel import Field, SQLModel, create_engine, Session, select, Relationship, delete, JSON, Column


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

class CategoryBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    value: str

class Category(CategoryBase, table=True):
    books: List["Book"] = Relationship(back_populates="categories", link_model=BookCategoryLink)
    # book_links: List[BookCategoryLink] = Relationship(back_populates="categories")

    # instantiate a CategoryReadWithBookIds from this object
    # @classmethod()
    # def to_category_read_with_book_ids(cls, c):
    #     # write docstring
    #     return CategoryReadWithBookIds(
    #         id=c.id,
    #         name=c.name,
    #         value=c.value,
    #         books=c.book_ids_only()
    #     )

    # def book_ids_only(self):
    #     return [book.id for book in self.books]
 
class CategoryRead(CategoryBase):
    id: int

class CategoryCreate(CategoryBase):
    pass
   
class BookBase(SQLModel):
    title: str
    author: str
    isbn: Optional[str] = None
    recommended_by: Optional[int] = Field(default=None, foreign_key="user.id")
    data: Dict = Field(default={}, sa_column=Column(JSON))
    
class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recommender: Optional[User] = Relationship(back_populates="books")
    categories: List[Category] = Relationship(back_populates="books", link_model=BookCategoryLink)
    # category_links: List[BookCategoryLink] = Relationship(back_populates="books")
    # add data column as jsonb for storing data
    # data: Optional[dict] = Field(default=None)
    # data: JSON = Field(default=None)

    class Config:
        arbitrary_types_allowed = True

class BookRead(BookBase):
    id: int

class BookCreate(BookBase):
    pass

# class BookUpdate with all fields optional defaulting to None
class BookUpdate(SQLModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    categories: Optional[List[int]] = None
    data: Optional[Dict] = None

class BookReadWithCategories(BookRead):
    categories: List[CategoryRead] = []

class CategoryReadWithBookIds(CategoryBase):
    books: List[int] = []

class CategoryReadWithBooks(CategoryBase):
    books: List[BookRead]


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
