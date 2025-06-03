import secrets
import string
from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import get_password_hash


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def generate_alias(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def create_url(db: Session, url: schemas.URLCreate, user_id: int):
    alias = url.custom_alias if url.custom_alias else generate_alias()

    while db.query(models.URL).filter(models.URL.alias == alias).first():
        alias = generate_alias()

    db_url = models.URL(
        original_url=str(url.original_url),
        alias=alias,
        user_id=user_id
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_url_by_alias(db: Session, alias: str):
    return db.query(models.URL).filter(models.URL.alias == alias).first()


def get_urls(db: Session, skip: int = 0, limit: int = 100, active_only: bool = True):
    query = db.query(models.URL)
    if active_only:
        query = query.filter(models.URL.is_active)
    return query.offset(skip).limit(limit).all()


def deactivate_url(db: Session, url_id: int):
    db_url = db.query(models.URL).filter(models.URL.id == url_id).first()
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url


def create_visit(db: Session, url_id: int, client_ip: str, user_agent: str):
    db_visit = models.Visit(
        url_id=url_id,
        client_ip=client_ip,
        user_agent=user_agent
    )
    db.add(db_visit)
    db.commit()
    db.refresh(db_visit)
    return db_visit


def get_url_stats(db: Session):
    return db.query(
        models.URL.alias,
        models.URL.original_url,
        models.URL.is_active,
        models.URL.created_at,
        models.URL.expires_at,
        func.count(models.Visit.id).label("visits_count")
    ).outerjoin(
        models.Visit,
        models.URL.id == models.Visit.url_id
    ).group_by(
        models.URL.id
    ).order_by(
        func.count(models.Visit.id).desc()
    ).all()
