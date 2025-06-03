from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.service import get_user_by_username
from app.database import SessionLocal
from app.utils import verify_password


security = HTTPBasic()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    db: SessionLocal = Depends(get_db)
):
    user = get_user_by_username(db, username=credentials.username)
    if not user or not verify_password(
        credentials.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
