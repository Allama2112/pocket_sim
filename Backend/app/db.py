from sqlalchemy import create_engine, MetaData
from app.models.card import Base

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)
metadata = MetaData()

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
	Base.metadata.create_all(engine)