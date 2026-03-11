from pydantic import BaseModel
from typing import Optional

class MovieBase(BaseModel):
    title: str
    overview: str
    year: int

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    overview: Optional[str] = None
    year: Optional[int] = None