from database import Base
from sqlalchemy import Column, Integer , String
from sqlalchemy.orm import relationship

class RoleModel (Base):
    __tablename__ = "role"

    id = Column(Integer,primary_key=True)
    role_name = Column(String(50),unique=True,nullable=False)

    users = relationship("UserModel",back_populates="role")