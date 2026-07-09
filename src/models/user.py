from sqlalchemy import Column, Integer, String, Table, ForeignKey
from src.config.database import Base
from sqlalchemy.orm import relationship

roles_users = Table(
    "roles_users",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(String(1), default="Y", nullable=False)
    roles = relationship("RoleModel", secondary=roles_users, backref="users")

class RoleModel(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    name = Column(String, nullable=True, index=True, unique=True)