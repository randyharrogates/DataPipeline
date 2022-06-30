import os
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer, String , Enum, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import sqlalchemy as sqlalchemy
from cleaner import finalDf
import pandas as pd
import os
import sys
import inspect
import base64

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
print(parentdir)

passwords = pd.read_csv(parentdir + '/scraping/encrypt.csv')
postgrespw = passwords['postgrespw'][0]
print(passwords.head())
print(postgrespw)
print(f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test')
DB_URI = f'postgresql://postgres:{base64.b64decode(postgrespw).decode("utf-8")}@localhost:5432/test'

engine = create_engine(DB_URI, echo=False)
conn = engine.connect()
Base = declarative_base()

class Words(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    body = Column(String)
    year = Column(String)
    sourceType = Column(String)
    

    def __repr__(self):
        return f"Words(id={self.id!r}, SourceType={self.sourceType!r})"

finalDict = finalDf.to_dict(orient='records')

metadata = sqlalchemy.schema.MetaData(bind=engine)
table = sqlalchemy.Table('words', metadata, autoload=True)

Session = sessionmaker(bind=engine)
session = Session()

conn.execute(table.insert(), finalDict)

session.commit()
session.close()





