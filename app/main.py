from routes.v1.book import book_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables, engine, Book, User, Category
import os

# allow origins from localhost:3000
from dotenv import load_dotenv

load_dotenv()

# load from .env -> not working in container
# FRONTEND_URL = os.getenv("FRONTEND_URL")
# local dev
# FRONTEND_URL  = ["http://localhost:3000"]
# hack for now
FRONTEND_URL  = ["*"]

origins = [
    FRONTEND_URL
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def main():
    create_db_and_tables()


app.include_router(book_app, prefix="/api/v1")

