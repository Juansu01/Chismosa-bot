from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

user = "chismosa_dev"
passw = "chismosa_dev_pwd"
host = "localhost"
db = "chismosa_dev_db"
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_pre_ping=True)
Base = declarative_base()

class Chismes(Base):
    __tablename__ = "Chismes"
    id = Column(Integer, primary_key=True)
    content = Column(String(700))


