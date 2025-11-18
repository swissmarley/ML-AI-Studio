# ML-AI Studio

A comprehensive web-based Machine Learning and AI Studio that democratizes artificial intelligence development for beginners.

## 🚀 Features

- **Data Management & Visualization**: Upload, organize, visualize, and preprocess data
- **ML Model Builder**: No-code model creation with visual builder
- **Templates Library**: Pre-built project templates for common ML tasks
- **AI Tools Integration**: API management, LLM chat, RAG pipelines
- **Generative AI Studio**: Image, audio, and video generation
- **Python Notebook Environment**: Integrated JupyterLab with Anaconda support
- **Deployment & MLOps**: One-click deployment and monitoring

## 🏗️ Architecture

- **Frontend**: React.js + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Databases**: PostgreSQL (structured), MongoDB (unstructured)
- **Containerization**: Docker
- **Notebook**: JupyterLab integration

## 📦 Installation

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.10+ (for local backend development)

### Quick Start with Docker

```bash
docker-compose up -d
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- JupyterLab: http://localhost:8888

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## 📁 Project Structure

```
ML-AI-Studio/
├── frontend/          # React frontend application
├── backend/           # FastAPI backend application
├── notebooks/         # Jupyter notebook templates
├── docker-compose.yml # Docker orchestration
└── README.md
```

## 🔐 Environment Variables

Create `.env` files in `backend/` and `frontend/` directories. See `.env.example` files for reference.

## 📚 Documentation

- [API Documentation](http://localhost:8000/docs) - Swagger UI
- [User Guide](./docs/USER_GUIDE.md)
- [Developer Guide](./docs/DEVELOPER_GUIDE.md)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines.

## 📄 License

MIT License

