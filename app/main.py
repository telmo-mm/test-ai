from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
import os
from dotenv import load_dotenv

from app.database import init_db, get_db
from app.routers import movies, ratings, recommendations

load_dotenv()

app = FastAPI(title="Movie Recommendation Engine", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(movies.router, prefix="/api/movies", tags=["movies"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["ratings"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/movies", response_class=HTMLResponse)
async def movies_page(request: Request):
    return templates.TemplateResponse("movies.html", {"request": request})

@app.get("/recommendations", response_class=HTMLResponse)
async def recommendations_page(request: Request):
    return templates.TemplateResponse("recommendations.html", {"request": request})
