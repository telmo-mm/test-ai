# Movie Recommendation Engine

An interactive movie recommendation system built with FastAPI and HTMX.

## Features

- 🎬 Search and discover movies
- ⭐ Rate movies with instant feedback
- 🤖 Get personalized recommendations
- 🎯 Filter by genre, year, and rating
- 📱 Responsive design
- 🐳 Docker support for easy deployment

## Quick Start with Docker (Recommended)

### Prerequisites
- Docker and Docker Compose installed
- TMDB API key (get it from https://www.themoviedb.org/settings/api)

### Setup

1. **Clone and setup**:
```bash
git clone https://github.com/telmo-mm/test-ai.git
cd test-ai
make dev-setup
```

2. **Add your TMDB API key**:
   Edit the `.env` file and add your TMDB API key:
```bash
TMDB_API_KEY=your_actual_api_key_here
```

3. **Start development server**:
```bash
make dev
```

4. **Open your browser**: http://localhost:8000

### Development Commands

```bash
make dev          # Start development environment (SQLite)
make prod         # Start production environment (PostgreSQL)
make logs         # View application logs
make shell        # Access container shell
make down         # Stop all services
make clean        # Clean up containers and volumes
```

## Manual Setup (Without Docker)

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment**:
```bash
cp .env.example .env
# Edit .env and add your TMDB API key
```

4. **Run the application**:
```bash
uvicorn app.main:app --reload
```

5. **Open http://localhost:8000**

## Tech Stack

- **Backend**: FastAPI (async, fast, modern Python)
- **Frontend**: HTMX + Tailwind CSS (no complex JavaScript!)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Movie Data**: TMDB API
- **Deployment**: Docker & Docker Compose

## Project Structure

```
movie-recommender/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── database.py          # Database configuration
│   ├── routers/             # API routes
│   │   ├── movies.py        # Movie search and details
│   │   ├── ratings.py       # Movie rating system
│   │   └── recommendations.py # Recommendation engine
│   ├── services/            # Business logic
│   │   └── tmdb.py          # TMDB API integration
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS, images, etc.
├── docker-compose.yml       # Production Docker setup
├── docker-compose.dev.yml   # Development Docker setup
├── Dockerfile              # Docker image definition
├── Makefile                # Development commands
└── requirements.txt        # Python dependencies
```

## API Endpoints

- `GET /` - Home page
- `GET /movies` - Movie search page
- `GET /recommendations` - Recommendations page
- `GET /api/movies/search?q={query}` - Search movies
- `GET /api/movies/popular` - Get popular movies
- `POST /api/ratings/rate` - Rate a movie
- `GET /api/recommendations/` - Get personalized recommendations

## How It Works

1. **Search Movies**: Uses TMDB API to search and display movies
2. **Rate Movies**: Users rate movies on a 1-5 star scale
3. **Generate Recommendations**: Based on user ratings, suggests similar movies
4. **Real-time Updates**: HTMX provides seamless, fast interactions

## Getting Your TMDB API Key

1. Go to https://www.themoviedb.org/
2. Create an account (free)
3. Go to Settings → API
4. Request an API key (choose "Developer")
5. Copy your API key to the `.env` file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `make dev`
5. Submit a pull request

## License

MIT License - feel free to use this project for learning and development!
