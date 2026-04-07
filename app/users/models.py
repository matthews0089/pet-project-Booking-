from sqlalchemy import JSON, Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hasned_password = Column(String, nullable=False)
    
    bookings = relationship("Bookings", back_populates="user")
    
    def __str__(self):
        return f"User {self.email}"