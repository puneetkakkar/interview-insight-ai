# FRAI Boilerplate

A minimal, production-ready FastAPI boilerplate using SQLAlchemy 2.0, Pydantic V2, and PostgreSQL. This project provides a solid foundation for building scalable web APIs with modern Python practices.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy 2.0**: Latest ORM with async support and type hints
- **Pydantic V2**: Data validation and serialization with improved performance
- **PostgreSQL**: Robust relational database with async driver support
- **Alembic**: Database migration management
- **Docker & Docker Compose**: Containerized development and production environments
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Type Hints**: Full type annotation support throughout the codebase
- **Clean Architecture**: Repository pattern with separation of concerns
- **Logging**: Structured logging with request tracking
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Built-in health monitoring endpoints
- **Exception Handling**: Centralized error handling with custom exceptions

## 🏗️ Architecture

The project follows a clean, layered architecture:

```
src/
├── app/
│   ├── api/           # API endpoints and routing
│   ├── core/          # Core application configuration
│   ├── models/        # SQLAlchemy database models
│   ├── repositories/  # Data access layer
│   └── schemas/       # Pydantic data models
├── migrations/        # Database migrations
└── tests/            # Test suite
```

### Key Components

- **Models**: SQLAlchemy models with timestamp and soft delete mixins
- **Repositories**: Generic CRUD operations with async support
- **Schemas**: Pydantic models for request/response validation
- **API Routes**: RESTful endpoints with proper error handling
- **Dependencies**: FastAPI dependency injection system
- **Configuration**: Environment-based settings management

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if running locally)
- UV package manager (recommended) or pip

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd frai-be
```

### 2. Environment Configuration

Copy the example environment file and configure your settings:

```bash
cp env.example .env
```

Edit `.env` with your configuration:

```env
# Database Settings
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=frai_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# Environment
ENVIRONMENT=development
DEBUG=true
RELOAD=true
```

### 3. Install Dependencies

Using UV (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### Development Environment

Start the development environment with Docker Compose:

```bash
make dev-up
```

This will:
- Start PostgreSQL database on port 5433
- Start the FastAPI application on port 8000
- Enable auto-reload for development

### Production Environment

Start the production environment:

```bash
make prod-up
```

This will:
- Start PostgreSQL database on port 5436
- Start the FastAPI application on port 8001
- Use Gunicorn with multiple workers
- Disable debug mode and auto-reload

## 📚 API Documentation

Once the application is running, you can access:

- **Interactive API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative API Docs**: http://localhost:8000/redoc (ReDoc)
- **Health Check**: http://localhost:8000/health
- **API Info**: http://localhost:8000/info

## 🗄️ Database Management

### Migrations

Create a new migration:
```bash
make revision
```

Apply migrations:
```bash
make upgrade
```

Create and apply migrations in one command:
```bash
make migrate
```

### Database Connection

The application automatically connects to PostgreSQL using the settings in your `.env` file. The database URL is constructed as:

```
postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}
```

## 🧪 Testing

### Run Tests Locally

```bash
make test
```

### Run Tests with Coverage

```bash
make coverage
```

### Run Tests in Docker Environment

```bash
make test-env
```

### Test Coverage Report

After running coverage, you'll find an HTML report in the `htmlcov/` directory.

## 🐳 Docker Commands

The project uses an environment-based Docker structure for better organization:

```
docker/
│── dev/     # Development environment
│── test/    # Testing environment  
│── prod/    # Production environment
```

Each environment contains its own Dockerfile and docker-compose.yml for complete isolation.

### Development

```bash
make dev-up      # Start development environment
make dev-down    # Stop development environment
make dev-logs    # View development logs
```

### Production

```bash
make prod-up     # Start production environment
make prod-down   # Stop production environment
make prod-logs   # View production logs
```

### Testing

```bash
make test-env    # Start testing environment
make test-down   # Stop testing environment
```

### Utility

```bash
make clean       # Remove all containers and volumes
make format      # Format code with ruff
make lint        # Run linting checks
```

For detailed Docker configuration information, see [docker/README.md](docker/README.md).

## 📁 Project Structure

```
frai-be/
│
├── docker/                         # Docker configuration
│   ├── README.md                   # Docker documentation
│   ├── dev/                        # Development environment
│   │   ├── Dockerfile.dev          # Development Dockerfile
│   │   └── docker-compose.dev.yml
│   ├── test/                       # Testing environment
│   │   ├── Dockerfile.test         # Testing Dockerfile
│   │   └── docker-compose.test.yml
│   └── prod/                       # Production environment
│       ├── Dockerfile.prod         # Production Dockerfile
│       └── docker-compose.prod.yml
├── src/                            # Source code
│   └── app/
│       ├── api/                    # API endpoints
│       │   └── v1/                 # API version 1
│       ├── core/                   # Core application logic
│       │   ├── config.py           # Configuration management
│       │   ├── db/                 # Database setup
│       │   ├── exceptions/         # Custom exceptions
│       │   ├── logger.py           # Logging configuration
│       │   ├── response.py         # Response formatting
│       │   └── setup.py            # Application setup
│       ├── models/                 # Database models
│       ├── repositories/           # Data access layer
│       ├── schemas/                # Pydantic schemas
│       └── main.py                 # Application entry point
├── migrations/                     # Database migrations
├── tests/                          # Test suite
│   ├── integration/                # Integration tests
│   ├── unit/                       # Unit tests
│   └── conftest.py                 # Test configuration
├── alembic.ini                     # Alembic configuration
├── pyproject.toml                  # Project configuration
├── Makefile                        # Build and deployment commands
└── README.md                       # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Application environment (development/testing/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `RELOAD` | Enable auto-reload | `true` |
| `POSTGRES_SERVER` | PostgreSQL server host | `localhost` |
| `POSTGRES_PORT` | PostgreSQL server port | `5432` |
| `POSTGRES_DB` | PostgreSQL database name | `frai_db` |
| `POSTGRES_USER` | PostgreSQL username | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `postgres` |
| `SECRET_KEY` | JWT secret key | `your-secret-key-here` |

### Database Configuration

The application supports multiple database configurations:

- **Development**: Uses main database with debug logging
- **Testing**: Uses separate test database
- **Production**: Uses main database with production optimizations

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set `ENVIRONMENT=production` and `DEBUG=false`
2. **Database**: Use production PostgreSQL instance
3. **Secrets**: Change default secret keys
4. **CORS**: Restrict allowed origins
5. **Logging**: Configure production logging levels
6. **Monitoring**: Add health checks and metrics

### Docker Production

```bash
make prod-up
```

The production Docker setup includes:
- Gunicorn with multiple workers
- Health checks for database
- Persistent volume for PostgreSQL data
- Optimized container configuration

## 🧹 Code Quality

### Linting and Formatting

```bash
make format    # Auto-fix code style issues
make lint      # Check code quality
```

### Type Checking

```bash
uv run mypy src/
```

### Pre-commit Hooks

Consider setting up pre-commit hooks for:
- Code formatting with ruff
- Type checking with mypy
- Linting with ruff
- Running tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the existing issues
2. Review the API documentation
3. Check the test examples
4. Create a new issue with detailed information

## 🔄 Updates and Maintenance

### Dependencies

Update dependencies regularly:
```bash
uv update
```

### Database Migrations

Always backup your database before running migrations in production.

### Security Updates

Keep dependencies updated, especially security-related packages.

---

**Happy Coding! 🎉**
