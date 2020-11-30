import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(
    "mysql+mysqlconnector://root:s3cr37@localhost:33010/classicmodels"
)

Base = declarative_base()
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
