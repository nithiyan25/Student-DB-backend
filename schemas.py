from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from typing import Optional

class StudentBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    roll_number: str = Field(..., min_length=1, max_length=50)
    department: str = Field(..., min_length=1, max_length=100)
    year: str = Field(..., min_length=1, max_length=20)
    dob: date
    gender: str = Field(..., min_length=1, max_length=20)
    phone_number: str = Field(..., min_length=10, max_length=15)
    school_email: EmailStr
    personal_email: EmailStr
    parent_name: str = Field(..., min_length=1, max_length=100)
    parent_mobile: str = Field(..., min_length=10, max_length=15)
    mentor_name: str = Field(..., min_length=1, max_length=100)
    mentor_staff_id: str = Field(..., min_length=1, max_length=50)
    mentor_email: EmailStr

class StudentCreate(StudentBase):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    roll_number: Optional[str] = Field(None, min_length=1, max_length=50)
    department: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[str] = Field(None, min_length=1, max_length=20)
    dob: Optional[date] = None
    gender: Optional[str] = Field(None, min_length=1, max_length=20)
    phone_number: Optional[str] = Field(None, min_length=10, max_length=15)
    school_email: Optional[EmailStr] = None
    personal_email: Optional[EmailStr] = None
    parent_name: Optional[str] = Field(None, min_length=1, max_length=100)
    parent_mobile: Optional[str] = Field(None, min_length=10, max_length=15)
    mentor_name: Optional[str] = Field(None, min_length=1, max_length=100)
    mentor_staff_id: Optional[str] = Field(None, min_length=1, max_length=50)
    mentor_email: Optional[EmailStr] = None

class Student(StudentBase):
    id: int
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True