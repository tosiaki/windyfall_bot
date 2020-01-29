import sqlalchemy
from sqlalchemy import Column, Integer, Text, DateTime

Base = sqlalchemy.ext.declarative.declarative_base()

class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key = True)
    data = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
