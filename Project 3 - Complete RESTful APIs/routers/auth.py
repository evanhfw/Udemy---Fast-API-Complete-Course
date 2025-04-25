"""Authentication router module for handling user authentication and authorization."""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt

from database import SessionLocal
from models import Users

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

SECRET_KEY = "d876c290ca444cb7d15909c04f2b8396561a84e5ed13fd3e2d48e16829a284f3"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_db():
    """Database session dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    """Authenticate a user by username and password."""
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, str(user.hashed_password)):
        return False
    return user


class CreateUserRequest(BaseModel):
    """Data model for user creation requests."""

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    """OAuth2 compatible token schema."""

    access_token: str
    token_type: str


def create_access_token(username, user_id, expires_delta: timedelta):
    """Create a new JWT access token."""
    # Convert to native types if needed
    username_str = str(username) if username is not None else None
    user_id_int = int(user_id) if user_id is not None else None

    encode = {"sub": username_str, "id": user_id_int}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=401, detail="Could not validate credentials"
            )
        return {"username": username, "id": user_id}
    except JWTError as exc:
        raise HTTPException(
            status_code=401, detail="Could not validate credentials"
        ) from exc


@router.post("/")
async def create_user(
    create_user_request: CreateUserRequest, db: Session = Depends(get_db)
):
    """Create a new user."""
    create_user_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Generate and return a JWT token for authenticated users."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}
