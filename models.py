from sqlalchemy import Integer, Column, String
from database import Base

class Blog(Base):
	__tablename__ = 'blogs'
	
	Id = Column(Integer,primary_key = True, index = True)
	title = Column(String)
	content = Column(String)
