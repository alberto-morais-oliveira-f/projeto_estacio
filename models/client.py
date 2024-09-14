from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR, index=True)
    email = Column(VARCHAR, unique=True, index=True)
