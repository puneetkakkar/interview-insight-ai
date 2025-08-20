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
make test          # Run all tests
make test-unit     # Run unit tests only
make test-integration # Run integration tests only
make test-all      # Run all tests with verbose output
make coverage      # Run tests with coverage report
make run           # Run dev server
make logs          # Show service logs
make clean         # Clean up containers and volumes
```

## 🧪 Testing Strategy

This boilerplate follows **Test-Driven Development (TDD)** principles and industry best practices for FastAPI testing.

### TDD Workflow

**For new features:**
1. **Write failing test first** - Define expected behavior in test
2. **Implement code to pass** - Write minimal code to make test pass
3. **Refactor** - Clean up code while keeping tests green

**For code changes:**
1. **Update tests first** - Modify tests to reflect new requirements
2. **Run tests** - Ensure they fail (red)
3. **Implement changes** - Make tests pass (green)
4. **Refactor** - Clean up while maintaining test coverage

### Test Structure

```
tests/
├── conftest.py                    # Global fixtures and configuration
├── unit/                          # Unit tests for business logic
│   ├── test_items.py             # CRUD operations, models, schemas
│   └── test_exceptions.py        # Custom exceptions and handlers
├── integration/                   # API endpoint tests
│   ├── test_api_items.py         # Items API integration tests
│   └── test_api_response_envelope.py # Response envelope tests
└── helpers/                       # Test utilities
    ├── generators.py              # Fake data generation
    └── mocks.py                   # Mock objects and responses
```

### Testing Commands

```bash
make test          # Run all tests
make test-unit     # Run unit tests only
make test-integration # Run integration tests only
make test-all      # Run all tests with verbose output
make coverage      # Run tests with coverage report
```

### Test Coverage Goals

- **Unit Tests**: 90%+ coverage for business logic
- **Integration Tests**: 80%+ coverage for API endpoints
- **Overall Coverage**: 85%+ across the codebase

### Testing Best Practices

1. **AAA Pattern**: Arrange, Act, Assert
2. **Descriptive Names**: Test names should explain what is being tested
3. **Mock External Dependencies**: Database, external APIs, etc.
4. **Test Edge Cases**: Invalid input, error conditions, boundary values
5. **Fast Execution**: Tests should run quickly (< 30 seconds total)
6. **Isolation**: Tests should not depend on each other

### Adding New Tests

**For new endpoints:**
```python
# tests/integration/test_api_new_feature.py
def test_new_endpoint_success():
    """Test new endpoint returns success response."""
    # Arrange
    test_data = {"key": "value"}
    
    # Act
    response = client.post("/api/v1/new-feature", json=test_data)
    
    # Assert
    assert response.status_code == 201
    assert response.json()["success"] is True
```

**For new models/schemas:**
```python
# tests/unit/test_new_model.py
def test_new_model_validation():
    """Test new model validation rules."""
    # Arrange & Act
    valid_data = {"field": "value"}
    model = NewModel(**valid_data)
    
    # Assert
    assert model.field == "value"
```

### Maintaining Tests

**When adding features:**
- Add corresponding tests before or alongside implementation
- Ensure new code paths are covered
- Run `make test-all` to verify all tests pass

**When removing features:**
- Remove or update related tests
- Run `make test-all` to ensure no broken tests remain
- Update test documentation if needed

**When refactoring:**
- Run tests frequently during refactoring
- Update tests to reflect new structure
- Maintain test coverage levels

### Test Data Management

- Use `tests/helpers/generators.py` for fake data
- Use `tests/helpers/mocks.py` for mock objects
- Keep test data realistic but minimal
- Use fixtures for common test setup

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
│   │   ├── response.py           # Response envelope helpers
│   │   └── exceptions/           # Custom exceptions
│   ├── models/
│   │   └── item.py               # Example database model
│   ├── repositories/
│   │   ├── base.py               # Base repository
│   │   └── items.py              # Example repository
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
6. Add tests (TDD approach)
7. Run migrations

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
- Comprehensive testing with TDD approach
- Type hints throughout
- Clean architecture
- Consistent API response envelope

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

**Test Failures**
```bash
# Run tests with verbose output
make test-all

# Check test coverage
make coverage

# Run specific test categories
make test-unit
make test-integration
```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests first (TDD approach)
4. Make your changes
5. **Ensure all tests pass**
6. Submit a pull request

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
- Demonstrating TDD and testing expertise

## API Response Structure

All API responses are wrapped in a consistent envelope to simplify frontend handling. The frontend can always check `success`, display `message`, and use `data` or `error.details` accordingly.

Success (HTTP 2xx):

```json
{
  "success": true,
  "data": { /* payload object or array */ },
  "message": "optional success info"
}
```

Error (HTTP 4xx/5xx):

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 422,
    "message": "Validation Error",
    "details": [ /* validation errors array */ ]
  }
}
```

Notes:

- Validation errors (422) include `details` as an array of error objects with `type`, `loc`, and `msg`.
- Other errors (e.g., 404, 500) include a human-friendly `message` and `details` as a string or array.
- The HTTP status code is preserved and also provided in `error.code`.

Examples:

```json
{
  "success": true,
  "data": {"id": 1, "title": "Item"},
  "message": "Item created successfully"
}
```

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": 404,
    "message": "Not Found",
    "details": "Item with ID 123 not found"
  }
}
```
