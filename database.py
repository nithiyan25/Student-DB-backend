from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import pymysql
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()
# Database configuration from environment variable
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "student_db")

# Encode password to handle special characters
encoded_password = quote_plus(DB_PASSWORD)

# Database URL without database name (for creating database)
DATABASE_URL_WITHOUT_DB = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}"

# Full database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# For cloud databases (Render, Aiven, etc.)
CLOUD_DATABASE_URL = os.getenv("DATABASE_URL")

if CLOUD_DATABASE_URL:
    # Use cloud database URL if provided
    if CLOUD_DATABASE_URL.startswith("postgres://"):
        CLOUD_DATABASE_URL = CLOUD_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = CLOUD_DATABASE_URL
else:
    # Create database if it doesn't exist (local MySQL only)
    try:
        # Connect without specifying database
        temp_engine = create_engine(DATABASE_URL_WITHOUT_DB, echo=False)
        
        with temp_engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SHOW DATABASES LIKE '{DB_NAME}'"))
            database_exists = result.fetchone() is not None
            
            if not database_exists:
                # Create database
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                conn.commit()
                print(f"✅ Database '{DB_NAME}' created successfully!")
            else:
                print(f"✅ Database '{DB_NAME}' already exists.")
        
        temp_engine.dispose()
    except Exception as e:
        print(f"⚠️  Warning: Could not create database automatically: {e}")
        print(f"Please create database manually or use cloud database URL")

# Create engine with the database
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize database tables
def init_db():
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")