from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE = 'sqlite'
DB_NAME = 'db.sqlite3'

Base = declarative_base()
DATABASE_PATH = '{}:///{}'.format(DATABASE, DB_NAME)
ECHO_LOG = True

engine = create_engine(DATABASE_PATH, echo=ECHO_LOG)

Session = sessionmaker(bind=engine)
session = Session()
