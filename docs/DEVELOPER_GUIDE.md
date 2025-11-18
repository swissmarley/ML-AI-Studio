# ML-AI Studio Developer Guide

## Architecture Overview

The ML-AI Studio is built as a full-stack application with the following components:

- **Frontend**: React.js with Vite, Tailwind CSS
- **Backend**: FastAPI (Python)
- **Databases**: PostgreSQL (structured data), MongoDB (unstructured data)
- **Containerization**: Docker and Docker Compose

## Project Structure

```
ML-AI-Studio/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Core configuration
│   │   ├── models/      # Database models
│   │   └── services/    # Business logic
│   ├── main.py          # Application entry point
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── hooks/       # Custom React hooks
│   │   └── utils/       # Utility functions
│   └── package.json     # Node dependencies
├── notebooks/           # Jupyter notebooks
└── docker-compose.yml   # Docker orchestration
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)

### Running with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Local Development

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations (when implemented)
alembic upgrade head

# Start server
uvicorn main:app --reload
```

#### Frontend

```bash
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL

# Start development server
npm run dev
```

## API Development

### Adding New Endpoints

1. Create endpoint file in `backend/app/api/v1/endpoints/`
2. Define route handlers
3. Register route in `backend/app/api/v1/__init__.py`

Example:

```python
# backend/app/api/v1/endpoints/example.py
from fastapi import APIRouter, Depends
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/example")
async def example_endpoint(current_user = Depends(get_current_user)):
    return {"message": "Hello, World!"}
```

### Database Models

1. Create model in `backend/app/models/`
2. Import in `backend/app/models/__init__.py`
3. Run migrations: `alembic revision --autogenerate -m "description"`

## Frontend Development

### Adding New Pages

1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.jsx`
3. Add navigation link in `frontend/src/components/Layout.jsx`

### State Management

- React Query for server state
- Context API for authentication
- Local state for component-specific data

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm test
```

## Deployment

### Production Build

```bash
# Frontend
cd frontend
npm run build

# Backend
# Already containerized, ready for deployment
```

### Environment Variables

Ensure all required environment variables are set in production:
- Database URLs
- API keys
- Secret keys
- CORS origins

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## Troubleshooting

### Database Connection Issues

- Check database is running: `docker-compose ps`
- Verify connection strings in `.env`
- Check database logs: `docker-compose logs postgres`

### Frontend Build Issues

- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node.js version: `node --version`
- Verify environment variables

### Backend Issues

- Check Python version: `python --version`
- Verify virtual environment is activated
- Check all dependencies are installed: `pip list`

