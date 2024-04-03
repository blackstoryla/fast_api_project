from pydantic import BaseModel, Field
from typing import Union, Annotated
from datetime import date


class Movie(BaseModel):
    name: str
    description: str
    time: int
    date_start: date
    date_end: date

class Session(BaseModel):
    id_movie: int
    date_time: date
    cinema_hall: int

class Movie_Update(BaseModel):
    id: int
    name: str|None = None
    description: str|None = None
    time: int|None = None
    date_start: date|None = None
    date_end: date|None = None

class Session_Update(BaseModel):
    id: int
    date_time: date|None = None
    cinema_hall: int|None = None
