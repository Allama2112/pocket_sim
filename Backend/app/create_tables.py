from app.models.card import Base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Load .env file from parent folder (backend/)
dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
load_dotenv(dotenv_path)

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
	raise ValueError("DATABASE_URL is not set")

# Create a synchronous SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create all tables defined in your models
def create_tables():
	Base.metadata.create_all(engine)
	print("✅ Tables created successfully.")

if __name__ == "__main__":
	create_tables()
