from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from shared.schemas.user import UserCreate, UserRead
from shared.utils import jwt
import hashlib

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hashlib.sha256(user.password.encode()).hexdigest()
    new_user = User(username=user.username, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.username == user.username).first()
    if not u or u.hashed_password != hashlib.sha256(user.password.encode()).hexdigest():
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.create_access_token({"sub": u.username})
    return {"access_token": token}
