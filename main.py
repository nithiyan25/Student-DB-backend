from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
import os
from typing import List, Optional
import json

from database import engine, get_db, init_db
from models import Base
import schemas
import crud

# Initialize Database
print("🔄 Initializing database...")
init_db()

# Initialize Firebase Admin
if not firebase_admin._apps:
    firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
    if firebase_credentials:
        try:
            cred_dict = json.loads(firebase_credentials)
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized successfully!")
        except Exception as e:
            print(f"⚠️  Firebase initialization failed: {e}")
            print("⚠️  Running without authentication - NOT RECOMMENDED FOR PRODUCTION")
    else:
        print("⚠️  No Firebase credentials found")

app = FastAPI(
    title="Student Management System API",
    description="API for managing student records with role-based access control",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    os.getenv("FRONTEND_URL", ""),
]
origins = [origin for origin in origins if origin]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Verify Firebase token
async def verify_firebase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Firebase ID token and extract user info with role"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        token = credentials.credentials
        
        # Verify the Firebase ID token
        decoded_token = firebase_auth.verify_id_token(token)
        
        # Extract role from custom claims (set via Firebase Admin SDK)
        role = decoded_token.get("role", "student")
        
        return {
            "uid": decoded_token.get("uid"),
            "email": decoded_token.get("email"),
            "role": role
        }
    except firebase_auth.ExpiredIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired. Please login again."
        )
    except firebase_auth.RevokedIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked. Please login again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}"
        )

# Dependency to check admin role
async def require_admin(current_user: dict = Depends(verify_firebase_token)):
    """Ensure user has admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Health check
@app.get("/", tags=["Health"])
def read_root():
    return {
        "message": "Student Management System API",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health", tags=["Health"])
def health_check():
    try:
        db = next(get_db())
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "healthy",
            "database": "connected",
            "firebase": "connected" if firebase_admin._apps else "not configured"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

# Students endpoints
@app.post("/students/", response_model=schemas.Student, tags=["Students"])
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)  # Only admins can create
):
    """Create a new student record (Admin only)"""
    
    # Check if roll number already exists
    if crud.get_student_by_roll_number(db, roll_number=student.roll_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Roll number already registered"
        )
    
    # Check if school email already exists
    if crud.get_student_by_school_email(db, school_email=student.school_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="School email already registered"
        )
    
    return crud.create_student(
        db=db, 
        student=student, 
        created_by=current_user.get("email")
    )

@app.get("/students/", response_model=List[schemas.Student], tags=["Students"])
def read_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    department: Optional[str] = Query(None),
    year: Optional[str] = Query(None),
    mentor_name: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_firebase_token)  # All authenticated users can view
):
    """Get all students with optional filters"""
    students = crud.get_students(
        db,
        skip=skip,
        limit=limit,
        department=department,
        year=year,
        mentor_name=mentor_name,
        gender=gender,
        search=search
    )
    return students

@app.get("/students/{student_id}", response_model=schemas.Student, tags=["Students"])
def read_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_firebase_token)
):
    """Get a specific student by ID"""
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return db_student

@app.put("/students/{student_id}", response_model=schemas.Student, tags=["Students"])
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)  # Only admins can update
):
    """Update a student record (Admin only)"""
    db_student = crud.update_student(db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return db_student

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_admin)  # Only admins can delete
):
    """Delete a student record (Admin only)"""
    success = crud.delete_student(db, student_id=student_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return {"message": "Student deleted successfully", "id": student_id}

@app.get("/stats", tags=["Statistics"])
def get_statistics(
    db: Session = Depends(get_db),
    current_user: dict = Depends(verify_firebase_token)
):
    """Get student statistics"""
    from sqlalchemy import func
    from models import Student
    
    total_students = db.query(func.count(Student.id)).scalar()
    students_by_dept = db.query(
        Student.department,
        func.count(Student.id)
    ).group_by(Student.department).all()
    
    students_by_year = db.query(
        Student.year,
        func.count(Student.id)
    ).group_by(Student.year).all()
    
    return {
        "total_students": total_students,
        "by_department": dict(students_by_dept),
        "by_year": dict(students_by_year)
    }

# User info endpoint
@app.get("/me", tags=["Auth"])
def get_current_user(current_user: dict = Depends(verify_firebase_token)):
    """Get current user information"""
    return current_user

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)