"""
Defines the Chisme table to store strings as "chismes", and creates Table.
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(
    f"mysql+mysqldb://{DB_USER }:{DB_PASSWORD}@{HOST}/{DB_NAME}",
    pool_size=20,
    max_overflow=0,
    pool_pre_ping=True
)
Base = declarative_base()


class Chismes(Base):
    """
    Chismes table declarative class.
    """
    __tablename__ = "Chismes"
    id = Column(Integer, primary_key=True)
    content = Column(String(700))
