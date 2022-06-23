from routes.v1.book import book_app
from fastapi import FastAPI

from database import create_db_and_tables, engine, Book, User, Category

def main():
    create_db_and_tables()


app = FastAPI()
app.include_router(book_app, prefix="/api/v1/book")

