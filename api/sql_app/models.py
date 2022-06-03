from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sql_app.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(32), unique=True, index=True)
    password = Column(String(64))
    fullname = Column(String(64))
    isdeteled = Column(Boolean, default=False)
