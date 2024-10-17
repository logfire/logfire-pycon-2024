from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse
from fastui import prebuilt_html
from pydantic_settings import BaseSettings
from openai import AsyncClient

from .db import Database
from .main import router as main_router


class Settings(BaseSettings):
    create_database: bool = True
    pg_dsn: str = 'postgres://postgres:postgres@localhost/cat_bacon_fastapi'


settings = Settings()  # type: ignore


@asynccontextmanager
async def lifespan(app_: FastAPI):
    async with Database.create(settings.pg_dsn, True, settings.create_database) as db:
        app_.state.db = db
        openai = AsyncClient()
        app_.state.openai = openai
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(main_router, prefix='/api')


@app.get('/favicon.ico')
async def favicon():
    return RedirectResponse(url='https://smokeshow.helpmanual.io/favicon.ico')


@app.get('/{path:path}')
async def html_landing() -> HTMLResponse:
    """Simple HTML page which serves the React app, comes last as it matches all paths."""
    return HTMLResponse(prebuilt_html(title='Logfire Cat Bacon'))
