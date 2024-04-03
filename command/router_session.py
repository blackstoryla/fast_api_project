from typing import Annotated, Union
from fastapi import Body, Depends, status
from sqlalchemy import select, insert, update, delete
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from models.database import get_async_session
from models.data_base_table import session as session_db

from models.cinema import Session, Session_Update


router_session = APIRouter(
)

@router_session.get("/") 
async def get_all_sessions(session: AsyncSession = Depends(get_async_session)):
    query = select(session_db)
    result = await session.execute(query)
    return result.mappings().all()


@router_session.get("/{id}") 
async def get_session_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(session_db).where(session_db.c.id == id)
    result = await session.execute(query)
    return result.mappings().all()

@router_session.post("/create") 
async def add_session(ses: Annotated[Session, Depends()], session: AsyncSession = Depends(get_async_session)):
    stmt = insert(session_db).values(
        id_movie = ses.id_movie,
        date = ses.date_time,
        cinema_hall = ses.cinema_hall
        )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content = [])
    
@router_session.put("/update") 
async def update_session(ses: Annotated[Session_Update, Depends()], session: AsyncSession = Depends(get_async_session)):
    def not_null_value(a, b):
        if a==None:
            return b
        return a
    
    query = select(session_db).where(session_db.c.id == ses.id)
    answer = await session.execute(query)
    result = answer.mappings().all()
    if result == []:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content = [])

    stmt = update(session_db).where(session_db.c.id == ses.id).values(
        date = not_null_value(ses.date_time, result[0].date),
        cinema_hall = not_null_value(ses.cinema_hall, result[0].cinema_hall)
        )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_201_CREATED, content = [])

@router_session.delete("/delete") 
async def delete_session(id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(session_db).where(session_db.c.id == id)
    answer = await session.execute(query)
    result = answer.mappings().all()
    if result == []:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content = [])

    stmt = delete(session_db).where(session_db.c.id == id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=status.HTTP_200_OK, content = [])