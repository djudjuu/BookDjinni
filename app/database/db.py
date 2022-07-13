from sqlmodel import SQLModel, create_engine
# import os
# from dotenv import load_dotenv


sqlite_file_name = "database/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_URL = (
#     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )
postgres_url = "postgresql://djinni:djinni@localhost:5432/djinni"

connect_args = {"check_same_thread": False}

# engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)
engine = create_engine(postgres_url, echo=True)

# engine = create_engine(sqlite_url, echo=True)
# engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
