from sqlmodel import SQLModel, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

# when using sqlite
# sqlite_file_name = "database/database.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# connect_args = {"check_same_thread": False}
# engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

# load from .env => not sure whether this is really happening
# POSTGRES_USER = os.getenv("POSTGRES_USER")
# POSTGRES_HOST = os.getenv("POSTGRES_HOST")
# POSTGRES_PORT = os.getenv("POSTGRES_PORT")
# POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
# POSTGRES_DB = os.getenv("POSTGRES_DB")
# POSTGRES_URL = (
#     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
# )

# for developemnt when api is run locally
# POSTGRES_URL = "postgresql://djinni:djinni@localhost:5432/djinni"

# for developemnt when api is run in container
POSTGRES_URL = "postgresql://djinni:djinni@djinni_db:5432/djinni"

print("POSTGRES_URL", POSTGRES_URL)
engine = create_engine(POSTGRES_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
