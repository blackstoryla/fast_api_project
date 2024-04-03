from typing import Annotated, Union
from fastapi import Body, Depends, status
from sqlalchemy import select, insert, update, delete
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from models.database import get_async_session
from models.data_base_table import movie

from models.cinema import Movie, Movie_Update

router_movie = APIRouter()

@router_movie.get("/") 
async def get_all_movie(session: AsyncSession = Depends(get_async_session)):
    query = select(movie)
    result = await session.execute(query)
    return result.mappings().all()

@router_movie.get("/{id}") 
async def get_movie_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(movie).where(movie.c.id == id)
    result = await session.execute(query)
    return result.mappings().all()

@router_movie.post("/create") 
async def add_movie(mov: Annotated[Movie, Depends()], session: AsyncSession = Depends(get_async_session)):
    stmt = insert(movie).values(
        name = mov.name,
        description = mov.description,
        time = mov.time,
        date_start = mov.date_start,
        date_end = mov.date_end
        )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content = [])
    
@router_movie.put("/update") 
async def update_movie(mov: Annotated[Movie_Update, Depends()], session: AsyncSession = Depends(get_async_session)):
    def not_null_value(a, b):
        if a==None:
            return b
        return a
    
    query = select(movie).where(movie.c.id == mov.id)
    answer = await session.execute(query)
    result = answer.mappings().all()
    if result == []:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content = [])

    stmt = update(movie).where(movie.c.id == mov.id).values(
        name = not_null_value(mov.name, result[0].name),
        description = not_null_value(mov.description, result[0].description),
        time = not_null_value(mov.time, result[0].time),
        date_start = not_null_value(mov.date_start, result[0].date_start),
        date_end = not_null_value(mov.date_end, result[0].date_end)
        )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content = [])

@router_movie.delete("/delete") 
async def delete_movie(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(movie).where(movie.c.id == id)
    answer = await session.execute(query)
    result = answer.mappings().all()
    if result == []:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content = [])

    stmt = delete(movie).where(movie.c.id == id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content = [])
    