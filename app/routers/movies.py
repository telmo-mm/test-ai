from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.database import get_db
from app.models import Movie
from app.services.tmdb import tmdb_service
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/search", response_class=HTMLResponse)
async def search_movies(
    request: Request,
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """Search for movies via TMDB API and return HTML results"""
    try:
        results = await tmdb_service.search_movies(q, page)
        movies = results.get('results', [])
        
        # Format movies for template
        formatted_movies = []
        for movie in movies[:12]:  # Limit to 12 results
            formatted_movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie.get('overview', '')[:200] + '...' if movie.get('overview', '') else 'No overview available',
                'poster_url': tmdb_service.get_poster_url(movie.get('poster_path')),
                'release_date': movie.get('release_date', 'Unknown'),
                'vote_average': round(movie.get('vote_average', 0), 1)
            })
        
        return templates.TemplateResponse(
            "partials/movie_results.html",
            {
                "request": request, 
                "movies": formatted_movies,
                "query": q,
                "total_results": results.get('total_results', 0)
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Failed to search movies. Please try again."}
        )

@router.get("/popular", response_class=HTMLResponse)
async def get_popular_movies(
    request: Request,
    page: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db)
):
    """Get popular movies"""
    try:
        results = await tmdb_service.get_popular_movies(page)
        movies = results.get('results', [])
        
        formatted_movies = []
        for movie in movies[:12]:
            formatted_movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'overview': movie.get('overview', '')[:200] + '...' if movie.get('overview', '') else 'No overview available',
                'poster_url': tmdb_service.get_poster_url(movie.get('poster_path')),
                'release_date': movie.get('release_date', 'Unknown'),
                'vote_average': round(movie.get('vote_average', 0), 1)
            })
        
        return templates.TemplateResponse(
            "partials/movie_results.html",
            {
                "request": request, 
                "movies": formatted_movies,
                "query": "Popular Movies"
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Failed to load popular movies."}
        )

@router.get("/{movie_id}/details", response_class=HTMLResponse)
async def get_movie_details(
    request: Request,
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed movie information"""
    try:
        movie_data = await tmdb_service.get_movie_details(movie_id)
        
        movie = {
            'id': movie_data['id'],
            'title': movie_data['title'],
            'overview': movie_data.get('overview', 'No overview available'),
            'poster_url': tmdb_service.get_poster_url(movie_data.get('poster_path')),
            'backdrop_url': tmdb_service.get_backdrop_url(movie_data.get('backdrop_path')),
            'release_date': movie_data.get('release_date', 'Unknown'),
            'vote_average': round(movie_data.get('vote_average', 0), 1),
            'runtime': movie_data.get('runtime', 0),
            'genres': [genre['name'] for genre in movie_data.get('genres', [])]
        }
        
        return templates.TemplateResponse(
            "partials/movie_details.html",
            {"request": request, "movie": movie}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Failed to load movie details."}
        )
