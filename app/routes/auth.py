from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models import User, Attendee  # Import both user types
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(db: Session, email: str):
    """Fetch user (Organizer or Attendee) by email."""
    user = db.query(User).filter(User.email == email).first()
    if user:
        return user
    return db.query(Attendee).filter(Attendee.email == email).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        user = get_user_by_email(db, email)
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


# Use Pydantic for structured input
class RegisterUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str  # Accepts "organizer" or "attendee"

    class Config:
        use_enum_values = True


@router.post("/register")
def register_user(user: RegisterUserRequest, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)

    if user.role == "organizer":
        new_user = User(
            username=f"{user.first_name} {user.last_name}",  # Create username dynamically
            email=user.email,
            password=hashed_password,
        )
    elif user.role == "attendee":
        new_user = Attendee(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hashed_password,  # Store hashed password
            phone_number="",
            check_in_status=False,
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid role. Choose 'organizer' or 'attendee'.")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User registered successfully as {user.role}"}


@router.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):  # password check
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    role = "organizer" if isinstance(user, User) else "attendee"
    access_token = create_access_token(data={"sub": user.email, "role": role})
    
    return {"access_token": access_token, "token_type": "bearer", "role": role}


@router.get("/me")
def get_logged_in_user(current_user = Depends(get_current_user)):
    role = "organizer" if isinstance(current_user, User) else "attendee"
    return {"id": current_user.id, "email": current_user.email, "role": role}
