# ТИКЕТНИЦА

Kanban-style task management application with analytics dashboard.

## Technologies

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Alembic
- **Frontend**: Vue 3, TypeScript, Tailwind CSS, Pinia
- **Testing**: pytest, httpx
- **Deployment**: Docker, Docker Compose

## Requirements

- Python 3.13+
- Node.js 18+
- PostgreSQL 15+ (or Docker)
- yarn

## Project Setup

### 1. Environment Variables

Create `.env` file in the root directory:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/task_tracker
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2. Database Setup

#### Option A: Using Docker Compose (Recommended)

```bash
docker-compose up -d postgres
```

#### Option B: Local PostgreSQL

Create database:

```bash
createdb task_tracker
```

### 3. Database Migrations

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
```

## Local Development

### Backend

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend

```bash
cd client
yarn install
yarn dev
```

Frontend will be available at `http://localhost:3000`

## Docker Deployment

### Start all services

```bash
docker-compose up -d
```

Services:

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- PostgreSQL: `localhost:5432`

### Stop services

```bash
docker-compose down
```

### View logs

```bash
docker-compose logs -f
```

## Testing

### Backend Tests

```bash
pytest
```

With coverage:

```bash
pytest --cov=app --cov-report=html
```

## Project Structure

```
deadline/
├── app/                    # Backend application
│   ├── api/               # API routes
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   ├── utils/             # Utilities
│   ├── config.py          # Configuration
│   ├── database.py        # Database setup
│   └── main.py            # FastAPI app
├── client/                # Frontend application
│   ├── src/
│   │   ├── api/          # API clients
│   │   ├── components/   # Vue components
│   │   ├── composables/  # Vue composables
│   │   ├── stores/       # Pinia stores
│   │   ├── router/       # Vue Router
│   │   └── views/        # Page views
│   └── package.json
├── alembic/              # Database migrations
├── tests/                # Backend tests
├── docker-compose.yml    # Docker services
└── requirements.txt      # Python dependencies
```

## API Endpoints

### Authentication

- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### Tasks

- `GET /tasks` - Get all tasks
- `POST /tasks` - Create task
- `GET /tasks/{id}` - Get task by ID
- `PUT /tasks/{id}` - Update task
- `DELETE /tasks/{id}` - Delete task

### Analytics

- `GET /analytics/dashboard` - Get analytics dashboard data
- `GET /analytics/tasks-by-status` - Tasks grouped by status
- `GET /analytics/tasks-by-priority` - Tasks grouped by priority

## Development Notes

- Backend uses Alembic for database migrations
- Frontend uses Vite as build tool
- CORS is configured for `localhost:3000` and `localhost:5173`
- JWT tokens are used for authentication
- All API routes require authentication except `/auth/register` and `/auth/login`
