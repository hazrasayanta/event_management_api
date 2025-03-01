from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext

# Database Configuration
DATABASE_URL = "sqlite:///./events.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    """Dependency to get the database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database and create a test user."""
    from app.models import User  # Import models inside the function to avoid circular import

    # Create tables
    Base.metadata.create_all(bind=engine)  

    db = SessionLocal()
    test_user = db.query(User).filter(User.username == "testuser").first()

    if not test_user:
        hashed_password = pwd_context.hash("testpassword")  
        new_user = User(username="testuser", email="testuser@example.com", password=hashed_password)
        db.add(new_user)
        db.commit()
        print("✅ Test user created: testuser / testpassword")
    else:
        print("ℹ️ Test user already exists.")

    db.close()
