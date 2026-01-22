from sqlalchemy import Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.sql import func
from database import Base
import enum

class GenderEnum(str, enum.Enum):
    male = "Male"
    female = "Female"
    other = "Other"

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_number = Column(String(50), unique=True, index=True, nullable=False)
    department = Column(String(100), nullable=False, index=True)
    year = Column(String(20), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)
    school_email = Column(String(100), unique=True, index=True, nullable=False)
    personal_email = Column(String(100), nullable=False)
    parent_name = Column(String(100), nullable=False)
    parent_mobile = Column(String(15), nullable=False)
    mentor_name = Column(String(100), nullable=False, index=True)
    mentor_staff_id = Column(String(50), nullable=False)
    mentor_email = Column(String(100), nullable=False)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())