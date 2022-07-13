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



# select all books from session
def select_all_books():
    with Session(engine) as session:
        # books = session.query(Book).all()
        books = session.exec(select(Book)).all()
        print(books)
        # return books

# write a function to select all books of user1 and print them
def select_all_books_of_user1():
    with Session(engine) as session:
        statement = select(User).where(User.name == "John Doe")
        result = session.exec(statement)
        user = result.one()
        print('user1 book', user.books)

# function to delete a model from the database
# NOT WORKING
def delete_model(model):
    with Session(engine) as session:
        session.exec(statement=delete(model))
        session.commit()

# delete all models by looping over delete_model()
# NOT WORKING
def delete_all_models():
    for model in ALL_MODELS:
        delete_model(model=model)


# select all titles of books where category Duration is short
def select_all_titles_of_books_with_category_short():
    with Session(engine) as session:
        # select all books 
        statement = select(Book)
        result = session.exec(statement)
        books = result.all()
        shorts = [b for b in books if any(c.value == "short" for c in b.categories)]
        print([b.title for b in shorts])


# return all books by a given user name
def select_all_books_by_user_name(name):
    with Session(engine) as session:
        statement = select(User).where(User.name == name)
        result = session.exec(statement)
        user = result.one()
        print('user books', user.books)
        # print the titles
        print([b.title for b in user.books])

# for a given list of books, return all books where a given category has a given value
# unsure how to do multipl where clauses on a many to many expression
def select_all_books_with_category_value(category_name, value):
    with Session(engine) as session:
        # statement = select(BookCategoryLink).where(BookCategoryLink.category.name == category_name).where(BookCategoryLink.category.value == value)
        # result = session.exec(statement)
        # books = result.all()
        # print([b.title for b in books])
        pass

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
        # reset_db(session=Session(engine))
        delete_model(model=Book)
    finally:
        pass
        # create_db_and_tables()
