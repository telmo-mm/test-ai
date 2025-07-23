from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Rating, Movie, User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/rate", response_class=HTMLResponse)
async def rate_movie(
    request: Request,
    movie_id: int = Form(...),
    rating: float = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """Rate a movie and return updated rating component"""
    try:
        # For now, we'll use a default user (user_id = 1)
        # In a real app, you'd get this from authentication
        user_id = 1
        
        # Check if user exists, create if not
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        if not user:
            user = User(id=user_id, username="demo_user")
            db.add(user)
            await db.commit()
        
        # Check if rating already exists
        rating_result = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
        )
        existing_rating = rating_result.scalar_one_or_none()
        
        if existing_rating:
            existing_rating.rating = rating
        else:
            new_rating = Rating(user_id=user_id, movie_id=movie_id, rating=rating)
            db.add(new_rating)
        
        await db.commit()
        
        return templates.TemplateResponse(
            "partials/rating_success.html",
            {
                "request": request, 
                "rating": rating,
                "movie_id": movie_id,
                "message": "Rating updated!" if existing_rating else "Rating saved!"
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "partials/error.html",
            {"request": request, "error": "Failed to save rating. Please try again."}
        )

@router.get("/{movie_id}/rating", response_class=HTMLResponse)
async def get_movie_rating(
    request: Request,
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get current user's rating for a movie"""
    try:
        user_id = 1  # Default user for demo
        
        rating_result = await db.execute(
            select(Rating).where(Rating.user_id == user_id, Rating.movie_id == movie_id)
        )
        rating = rating_result.scalar_one_or_none()
        
        return templates.TemplateResponse(
            "partials/movie_rating.html",
            {
                "request": request,
                "movie_id": movie_id,
                "current_rating": rating.rating if rating else 0
            }
        )
        
    except Exception as e:
        return templates.TemplateResponse(
            "partials/movie_rating.html",
            {
                "request": request,
                "movie_id": movie_id,
                "current_rating": 0
            }
        )
