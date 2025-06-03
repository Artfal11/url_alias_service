from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app import service, models, schemas
from app.database import SessionLocal, engine
from app.auth import get_current_user


models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Alias Service",
    description="Сервис для создания коротких ссылок",
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/urls/", response_model=schemas.URL)
def create_url(
    url: schemas.URLCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return service.create_url(db=db, url=url, user_id=current_user.id)


@app.get("/urls/", response_model=list[schemas.URL])
def read_urls(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    urls = service.get_urls(
        db,
        skip=skip,
        limit=limit,
        active_only=active_only
    )
    return urls


@app.patch("/urls/{url_id}/deactivate", response_model=schemas.URL)
def deactivate_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    url = service.deactivate_url(db, url_id=url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return url


@app.get("/stats/", response_model=list[schemas.URLStats])
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return service.get_url_stats(db)


@app.get("/{alias}")
def redirect_url(
    alias: str,
    request: Request,
    db: Session = Depends(get_db)
):
    url = service.get_url_by_alias(db, alias=alias)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    if not url.is_active or url.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=410,
            detail="URL is no longer available"
        )

    service.create_visit(
        db,
        url_id=url.id,
        client_ip=request.client.host,
        user_agent=request.headers.get("user-agent", "")
    )

    return RedirectResponse(url.original_url)


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    return service.create_user(db=db, user=user)
