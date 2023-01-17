"""
Defines the Chisme table to store strings as "chismes", and creates Table.
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


USER = "chismosa_dev"
PASSW = "chismosa_dev_pwd"
HOST = "localhost"
DB = "chismosa_dev_db"

engine = create_engine(
    f"mysql+mysqldb://{USER}:{PASSW}@{HOST}/{DB}",
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
