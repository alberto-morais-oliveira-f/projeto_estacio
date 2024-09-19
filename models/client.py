from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(VARCHAR(256), nullable=False)
    email = Column(VARCHAR(256), unique=True, nullable=False)
    phone = Column(VARCHAR(14))
