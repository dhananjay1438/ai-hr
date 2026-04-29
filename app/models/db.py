from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass

class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    raw_jd = Column(Text, nullable=False)
    status = Column(String, default="PENDING") # PENDING, RUNNING, DONE, FAILED
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Report(Base):
    __tablename__ = "reports"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    data = Column(JSON, nullable=False) # Store CandidateBrief list as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())
