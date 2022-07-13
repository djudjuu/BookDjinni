from sqlmodel import Session, delete, select
from database.models import User, Book, Category, ALL_MODELS, BookCategoryLink
from database.db import engine, create_db_and_tables


def create_books_and_users():
    with Session(engine) as session:
        # add some users using generic emails and passworddjudjuus
        user1 = User(name="John Doe", email="j@mail.com", password="password")
        user2 = User(name="Jane Doe", email="Jane@mail.com", password="password")
        # create 3 categories
        long = Category(name="Duration", value="long")
        short = Category(name="Duration", value="short")
        scifi = Category(name="Genre", value="SciFi")
        adventure = Category(name="Genre", value="Adventure")
        # create 3 books
        book1 = Book(title="The Alchemist", author="Paulo Coelho", isbn="123456789", recommender=user1, categories=[short, adventure], data={'rating': 5, 'review': "This book is great!", "description": "A book about a book about a book"})
        book2 = Book(title="Endymion", author="Paulo Coelho", isbn="123456789", recommender=user1, categories=[long,scifi])
        book3 = Book(title="I, Robot", author="Paulo Coelho", isbn="123456789", recommender=user2, categories=[short, scifi])
        # add books to db
        session.add(book1)
        session.add(book2)
        session.add(book3)
        session.commit()

        print('categories of book1', book1.categories)

def reset_db(session: Session, tables=[]):
    # if tables is empty, delete all models
    if not tables:
        session.execute('TRUNCATE book, "user", category, bookcategorylink CASCADE;')
    else:
        for table in tables:
            if table == "user":
                session.execute('TRUNCATE table "user" CASCADE;') # + ", ".join(tables))
            else: 
                # print what table is being deleted
                statement = f"TRUNCATE table {table} CASCADE;"
                # print('doing', statement)
                session.execute(statement=statement)
    session.commit()




if __name__ == "__main__":
    try:
        reset_db(session=Session(engine))
        # pass
    finally:
        # create_db_and_tables()
        create_books_and_users()
        #     # select_all_books_of_user1()
        #     # select_all_books()
        # select_all_titles_of_books_with_category_short()
        # select_all_books_by_user_name("John Doe")
        # select_all_books_with_category_value("Duration", "short")

