from sqlalchemy import Enum, create_engine, Column,Integer,String,ForeignKey,Float,DateTime,MetaData,Boolean
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import enum


SQLALCHEMY_DATABASE_URL = "sqlite:///.rent_a_shelf.db"
engine= create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()
