from sqlalchemy import Column , Integer , String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
     __tablename__ = 'users'
     id = Column(Integer , primary_key=True)
     username = Column(String(150) , nullable=False)
     email = Column(String(150) , nullable=False, unique=True)
     role = Column(String(150))
     password = Column(String(150) , nullable=False)
     
# class Product(Base):
#      __tablename__ = 'products'
#      id = Column(Integer , primary_key=True)
#      productname =Column(String(150) , nullable=False)
#      productCategory = Column(String(150) , nullable=False)
     