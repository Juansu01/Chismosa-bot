from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
import youtube_dl


user = "chismosa_dev"
passw = "chismosa_dev_pwd"
host = "localhost"
db = "chismosa_dev_db"
engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, passw, host, db), pool_size=20, max_overflow=0, pool_pre_ping=True)
Base = declarative_base()


class Chismes(Base):
    __tablename__ = "Chismes"
    id = Column(Integer, primary_key=True)
    content = Column(String(700))


async def search_song(client, amount, song, get_url=False):
   info = await client.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))

   if len(info["entries"]) == 0: return None
   return [entry["webpage_url"] for entry in info["entries"]] if get_url else info
