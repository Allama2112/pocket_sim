from databases import Database
from sqlalchemy import create_engine, MetaData
from app.models.card import Base

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()


def create_db_and_tables():
	Base.metadata.create_all(engine)