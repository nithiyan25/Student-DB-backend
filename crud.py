from sqlalchemy.orm import Session
from sqlalchemy import or_
from models import Student
from schemas import StudentCreate, StudentUpdate
from datetime import datetime

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def get_student_by_roll_number(db: Session, roll_number: str):
    return db.query(Student).filter(Student.roll_number == roll_number).first()

def get_student_by_school_email(db: Session, school_email: str):
    return db.query(Student).filter(Student.school_email == school_email).first()

def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    department: str = None,
    year: str = None,
    mentor_name: str = None,
    gender: str = None,
    search: str = None
):
    query = db.query(Student)
    
    # Apply filters
    if department:
        query = query.filter(Student.department == department)
    
    if year:
        query = query.filter(Student.year == year)
    
    if gender:
        query = query.filter(Student.gender == gender)
    
    if mentor_name:
        query = query.filter(Student.mentor_name.ilike(f"%{mentor_name}%"))
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.ilike(search_term),
                Student.roll_number.ilike(search_term),
                Student.school_email.ilike(search_term),
                Student.personal_email.ilike(search_term),
                Student.mentor_name.ilike(search_term)
            )
        )
    
    return query.offset(skip).limit(limit).all()

def create_student(db: Session, student: StudentCreate, created_by: str):
    db_student = Student(
        **student.dict(),
        created_by=created_by
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def update_student(db: Session, student_id: int, student: StudentUpdate):
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    
    update_data = student.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_student, key, value)
    
    db_student.updated_at = datetime.now()
    db.commit()
    db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = get_student(db, student_id)
    if not db_student:
        return False
    
    db.delete(db_student)
    db.commit()
    return True 