# Quick Start Guide

## Prerequisites

- Docker and Docker Compose installed
- Git installed

## Getting Started

### 1. Clone and Setup

```bash
# Clone the repository (if applicable)
cd ML-AI-Studio

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Configure Environment Variables

Edit `backend/.env` and set:
- Database credentials (or use defaults)
- API keys for AI services (optional initially)
- Secret keys (change in production!)

Edit `frontend/.env` and set:
- `VITE_API_URL=http://localhost:8000`

### 3. Start Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **JupyterLab**: http://localhost:8888

### 5. Create Your First Account

1. Open http://localhost:3000
2. Click "Register"
3. Create an account
4. Log in

### 6. Upload Your First Dataset

1. Go to **Data Management**
2. Drag and drop a CSV file
3. View the dataset summary

### 7. Create Your First Model

1. Go to **Model Builder**
2. Click **Create Model**
3. Fill in the form
4. Train the model with your dataset

## Troubleshooting

### Services won't start

```bash
# Check if ports are in use
netstat -an | grep -E '3000|8000|8888|5432|27017'

# Restart services
docker-compose down
docker-compose up -d
```

### Database connection errors

```bash
# Check database logs
docker-compose logs postgres
docker-compose logs mongodb

# Restart databases
docker-compose restart postgres mongodb
```

### Frontend can't connect to backend

- Verify `VITE_API_URL` in `frontend/.env`
- Check backend is running: `docker-compose ps backend`
- Check backend logs: `docker-compose logs backend`

## Next Steps

- Read the [User Guide](./docs/USER_GUIDE.md)
- Explore the [Developer Guide](./docs/DEVELOPER_GUIDE.md)
- Try out the templates in the Templates Library
- Experiment with AI Tools

## Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears data)
docker-compose down -v
```

