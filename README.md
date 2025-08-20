# FastAPI Minimal Boilerplate

A minimal, production-ready FastAPI boilerplate designed for rapid development and coding interviews. Built with SQLAlchemy 2.0, Pydantic V2, and PostgreSQL.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- UV package manager (recommended) or pip

### 1. Clone and Setup
```bash
git clone <your-repo>
cd fastapi-minimal-boilerplate
cp env.example .env
# Edit .env with your database credentials
```

### 2. Start Services
```bash
# Start database and API services
make up

# Or manually:
docker compose up -d
```

### 3. Run Migrations
```bash
# Create and apply initial migrations
make migrate

# Or step by step:
make revision  # Create migration
make upgrade   # Apply migration
```

### 4. Start Development Server
```bash
# Run locally (outside Docker)
make run

# Or with Docker (already running from step 2)
# Access at http://localhost:8000
```

### 5. Verify Setup
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Example endpoint: http://localhost:8000/api/v1/items

## 🛠️ Development Commands

```bash
make help          # Show all available commands
make up            # Start services
make down          # Stop services
make build         # Build Docker images
make migrate       # Create and apply migrations
make revision      # Create new migration
make upgrade       # Apply migrations
make test          # Run tests
make run           # Run dev server
make logs          # Show service logs
make clean         # Clean up containers and volumes
```

## 📁 Project Structure

```
src/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── items.py          # Example CRUD endpoints
│   ├── core/
│   │   ├── config.py             # Settings and configuration
│   │   ├── db/
│   │   │   ├── database.py       # Database connection
│   │   │   └── models.py         # Base model
│   │   └── exceptions/           # Custom exceptions
│   ├── crud/
│   │   ├── crud_base.py          # Base CRUD operations
│   │   └── crud_items.py         # Example CRUD implementation
│   ├── models/
│   │   └── item.py               # Example database model
│   ├── schemas/
│   │   └── item.py               # Pydantic schemas
│   └── main.py                   # FastAPI application
├── migrations/                    # Alembic migrations
└── tests/                        # Test suite
```

## 🗄️ Database Migrations

### Creating Migrations
```bash
# After modifying models in src/app/models/
make revision
```

**Important**: Always import new models in `src/app/models/__init__.py` before running `make revision`.

### Applying Migrations
```bash
make upgrade
```

### Migration Workflow
1. Modify models in `src/app/models/`
2. Import new models in `src/app/models/__init__.py`
3. Run `make revision` to generate migration
4. Review generated migration file
5. Run `make upgrade` to apply changes

## 🔧 Configuration

Environment variables are loaded from `.env` file:

- **Database**: PostgreSQL connection settings
- **App**: Application name, version, description
- **Security**: Secret key and algorithm (minimal setup)

## 🧪 Testing

```bash
make test          # Run all tests
make test -k       # Run tests with verbose output
```

Tests include:
- Unit tests for CRUD operations
- Database integration tests
- API endpoint tests

## 🚀 Production Deployment

### Docker Compose
```bash
# Comment out development command in docker-compose.yml
# Uncomment gunicorn command for production
docker compose up -d
```

### Environment Variables
- Set `ENVIRONMENT=production`
- Use strong `SECRET_KEY`
- Configure production database credentials

## 🔌 Extending the Boilerplate

### Adding New Models
1. Create model in `src/app/models/`
2. Add to `src/app/models/__init__.py`
3. Create schemas in `src/app/schemas/`
4. Implement CRUD operations
5. Add API endpoints
6. Run migrations

### Example: Adding User Authentication
```python
# Prompt Claude: "Add JWT authentication with user model and login endpoints"
# This will generate the necessary code for user management
```

### Example: Adding AI Integration
```python
# Prompt Claude: "Add LangChain RAG integration with document processing endpoints"
# This will add AI/ML capabilities to your API
```

## 🎯 Features

### ✅ Included
- FastAPI with async support
- SQLAlchemy 2.0 + PostgreSQL
- Pydantic V2 schemas
- Alembic migrations
- Docker Compose setup
- Comprehensive testing
- Type hints throughout
- Clean architecture

### ❌ Removed (for simplicity)
- Redis caching
- Background task queues
- Complex authentication
- Admin panel
- Rate limiting
- Client-side caching
- Multiple database support

## 🐛 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check if database is running
docker compose ps

# Check database logs
docker compose logs db
```

**Migration Errors**
```bash
# Reset migrations (development only)
docker compose down -v
docker compose up -d
make migrate
```

**Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill process or change port in docker-compose.yml
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Built for speed and simplicity** 🚀

Perfect for:
- Coding interviews
- Rapid prototyping
- Learning FastAPI
- Building production APIs
- Extending with AI/ML features
