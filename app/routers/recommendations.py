from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import Rating, Movie, User
from app.services.tmdb import tmdb_service

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def get_recommendations(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """Get personalized movie recommendations"""
    try:
        user_id = 1  # Default user for demo
        
        # Get user's highest rated movies
        user_ratings = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.rating >= 4.0)
            .order_by(Rating.rating.desc())
            .limit(3)
        )
        top_rated_movies = user_ratings.scalars().all()
        
        recommendations = []
        
        if top_rated_movies:
            # Get TMDB recommendations based on user's favorite movies
            for rating in top_rated_movies:
                try:
                    tmdb_recs = await tmdb_service.get_movie_recommendations(rating.movie_id)
                    for movie in tmdb_recs.get('results', [])[:4]:  # Get 4 from each
                        if len(recommendations) < 12:  # Limit total recommendations
                            recommendations.append({
                                'id': movie['id'],
                                'title': movie['title'],
                                'overview': movie.get('overview', '')[:200] + '...' if movie.get('overview', '') else 'No overview available',
                                'poster_url': tmdb_service.get_poster_url(movie.get('poster_path')),
                                'release_date': movie.get('release_date', 'Unknown'),
                                'vote_average': round(movie.get('vote_average', 0), 1)
                            })
                except:
                    continue
        
        # If no personalized recommendations, show popular movies
        if not recommendations:
            popular_movies = await tmdb_service.get_popular_movies()
            for movie in popular_movies.get('results', [])[:12]:
                recommendations.append({
                    'id': movie['id'],
                    'title': movie['title'],
                    'overview': movie.get('overview', '')[:200] + '...' if movie.get('overview', '') else 'No overview available',
                    'poster_url': tmdb_service.get_poster_url(movie.get('poster_path')),
                    'release_date': movie.get('release_date', 'Unknown'),
                    'vote_average': round(movie.get('vote_average', 0), 1)
                })
        
        # Remove duplicates
        seen_ids = set()
        unique_recommendations = []
        for movie in recommendations:
            if movie['id'] not in seen_ids:
                seen_ids.add(movie['id'])
                unique_recommendations.append(movie)
        
        return templates.TemplateResponse(
            "partials/recommendations.html",
            {
                "request": request,
                "movies": unique_recommendations[:12],
                "has_ratings": len(top_rated_movies) > 0
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Failed to load recommendations."}
        )
