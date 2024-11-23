from sqlalchemy import Enum, create_engine, Column,Integer,String,ForeignKey,Float,DateTime,MetaData,Boolean, event
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum


SQLALCHEMY_DATABASE_URL = "sqlite:///.rent_a_shelf.db"
engine= create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()
