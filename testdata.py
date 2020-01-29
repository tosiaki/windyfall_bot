from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, TIMESTAMP
from sqlalchemy import func

Base = declarative_base()

class TestData(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key = True)
    data = Column(Text)
    created_at = Column(TIMESTAMP, server_default = func.sysdate())
    updated_at = Column(TIMESTAMP, server_default = func.sysdate())
