import httpx
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

class TMDBService:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3")
        self.image_base_url = "https://image.tmdb.org/t/p/w500"
        
    async def search_movies(self, query: str, page: int = 1) -> Dict:
        """Search for movies by title"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/search/movie",
                params={
                    "api_key": self.api_key,
                    "query": query,
                    "page": page,
                    "include_adult": False
                }
            )
            return response.json()
    
    async def get_movie_details(self, movie_id: int) -> Dict:
        """Get detailed information about a movie"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/{movie_id}",
                params={"api_key": self.api_key}
            )
            return response.json()
    
    async def get_popular_movies(self, page: int = 1) -> Dict:
        """Get popular movies"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/popular",
                params={
                    "api_key": self.api_key,
                    "page": page
                }
            )
            return response.json()
    
    async def get_top_rated_movies(self, page: int = 1) -> Dict:
        """Get top rated movies"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/top_rated",
                params={
                    "api_key": self.api_key,
                    "page": page
                }
            )
            return response.json()
    
    async def get_movie_recommendations(self, movie_id: int, page: int = 1) -> Dict:
        """Get recommendations for a specific movie"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/movie/{movie_id}/recommendations",
                params={
                    "api_key": self.api_key,
                    "page": page
                }
            )
            return response.json()
    
    def get_poster_url(self, poster_path: str) -> str:
        """Get full URL for movie poster"""
        if not poster_path:
            return "/static/images/no-poster.jpg"
        return f"{self.image_base_url}{poster_path}"
    
    def get_backdrop_url(self, backdrop_path: str) -> str:
        """Get full URL for movie backdrop"""
        if not backdrop_path:
            return "/static/images/no-backdrop.jpg"
        return f"https://image.tmdb.org/t/p/w1280{backdrop_path}"

# Global instance
tmdb_service = TMDBService()
