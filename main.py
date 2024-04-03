# -*- coding: cp1251 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from command.router_movie import router_movie
from command.router_session import router_session

app = FastAPI(
    title = "Cinema"
)

app.include_router(
    router_movie, 
    tags = ["Movie"],
    prefix = "/movie"
    )

app.include_router(
    router_session,
    tags = ["Session"],
    prefix = "/session"
    )

@app.get('/', response_class= HTMLResponse)
async def f_index():
    return "FIO:Shulga Olga Vladimirovna"

