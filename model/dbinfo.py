from sqlalchemy import Column, Integer

from model.base import Base


class DBInfo(Base):
    __tablename__ = 'dbinfo'

    key = Column(Integer, primary_key=True)
    value = Column(Integer)
