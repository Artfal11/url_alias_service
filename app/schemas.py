from pydantic import BaseModel, HttpUrl
from datetime import datetime


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class URLBase(BaseModel):
    original_url: HttpUrl


class URLCreate(URLBase):
    custom_alias: str | None = None


class URL(URLBase):
    id: int
    alias: str
    created_at: datetime
    expires_at: datetime
    is_active: bool
    user_id: int

    class Config:
        orm_mode = True


class URLStats(URLBase):
    alias: str
    created_at: datetime
    expires_at: datetime
    is_active: bool
    visits_count: int

    class Config:
        orm_mode = True
