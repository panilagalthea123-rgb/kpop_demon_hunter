from sqlalchemy import Column, Integer, String
from database import Base

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String) # Huntrix, Saja Boys, etc.
    voice_actor = Column(String)
    singing_voice = Column(String)
    description = Column(String)