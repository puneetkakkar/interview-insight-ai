# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Running the Application
- **Development with in-memory storage**: `uv run python -m src.app.main` (fastest startup for coding interviews)
- **Development with PostgreSQL**: `make dev-up` (starts Docker containers)
- **Production**: `make prod-up`

### Testing
- **Run tests locally**: `make test` or `uv run pytest tests/ -v`
- **Run with coverage**: `make test-all` or `uv run pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v`
- **Docker test environment**: `make test-env`

### Code Quality
- **Format code**: `make format` or `uv run ruff --fix .`
- **Lint code**: `make lint` or `uv run ruff .`
- **Type checking**: `uv run mypy src/`

### Database Management (PostgreSQL only)
- **Create migration**: `make revision`
- **Apply migrations**: `make upgrade`  
- **Create and apply**: `make migrate`

## Architecture Overview

This is a FastAPI-based AI-powered backend with a clean, layered architecture supporting both in-memory and PostgreSQL storage modes.

### Key Architectural Patterns

**Dual Storage Architecture**: The system can run in two modes:
- `STORAGE_TYPE=memory`: SQLite in-memory (perfect for interviews/quick dev)
- `STORAGE_TYPE=postgres`: Full PostgreSQL with migrations

**Multi-Agent AI System**: Built on LangGraph v0.3 with:
- Agent registry in `src/app/agents/agent.py`
- Research assistant with web search and calculator tools
- Claude 3.5 Haiku and OpenAI integration
- Mock responses when API keys unavailable

**Clean Separation**: 
- `src/app/core/`: Configuration, database, exceptions, logging
- `src/app/api/v1/`: API endpoints and routing
- `src/app/agents/`: AI agents and LangGraph implementation
- `src/app/schemas/`: Pydantic models for validation
- `src/app/repositories/`: Data access layer (optional, only used with PostgreSQL)

### Critical Components

**Database Abstraction** (`src/app/core/db/database.py`):
- `initialize_database()`: Sets up engine based on STORAGE_TYPE
- `get_db()`: Dependency injection for database sessions
- Sync-to-async wrapper for in-memory SQLite mode

**Configuration** (`src/app/core/config.py`):
- Environment-based settings with Pydantic BaseSettings
- Three-tier settings hierarchy: App, Database, LanguageModel combined into Settings
- Automatic database URL selection: memory → `sqlite+aiosqlite:///:memory:`, postgres → async PostgreSQL
- API key validation with properties: `has_anthropic_api_key`, `has_openai_api_key`
- Available models detection based on API keys (`available_models` property)

**AI Agent System** (`src/app/agents/`):
- Dictionary-based agent registry
- LangGraph state management
- Tool integration (calculator, web search)
- Support for conversation threading and interrupts

## Development Workflow

### Quick Start for Coding Interviews
1. `echo "STORAGE_TYPE=memory" > .env`
2. `uv run python -m src.app.main`
3. Access http://localhost:8000/docs

### Development Environment Variables
The config system supports both .env files and direct environment variables:
- Settings class hierarchy: `AppSettings`, `DatabaseSettings`, `LanguageModelSettings` combined into `Settings`
- Property-based configuration validation in `src/app/core/config.py:144-151`
- Automatic database URL generation based on environment and storage type

### Adding New Features
1. Always check `src/app/core/config.py` for configuration patterns
2. Use existing Pydantic schemas in `src/app/schemas/`
3. Follow the response format in `src/app/core/response.py`
4. Add endpoints to appropriate versioned router in `src/app/api/v1/`
5. **Important**: When adding new models, check if API keys are available via `settings.has_anthropic_api_key` or `settings.has_openai_api_key`

### AI Agent Development
- Extend `agents` dict in `src/app/agents/agent.py:22-31` (currently has research-assistant and transcript-analyzer)
- Default agent is `research-assistant` (defined in `src/app/agents/agent.py:9`)
- Agent registry uses dataclass pattern with `description` and `graph` properties
- Create new agent modules following `research_assistant.py` pattern
- Add tools to `src/app/agents/tools.py`
- Use mocked responses for development without API keys
- Agent type definitions: `AgentGraph = CompiledStateGraph | Pregel`

### Database Development
- For PostgreSQL features: Use repositories pattern in `src/app/repositories/`
- For in-memory mode: Direct SQLAlchemy model usage is fine
- Always handle both storage types in business logic
- Database models go in `src/app/core/db/models.py`

## Testing Strategy

**Test Structure**:
- `tests/unit/`: Fast, isolated tests
- `tests/integration/`: API integration tests
- `tests/conftest.py`: Shared fixtures with database mocking

**Key Testing Patterns**:
- Use `mock_client` fixture for API testing without database
- Environment variables automatically set to testing mode
- Mock database sessions available via `mock_db_session` fixture

## Important Notes

**Environment Configuration**: 
- Storage type switching via `STORAGE_TYPE` environment variable
- AI features work without API keys using cached mock responses
- Debug mode automatically enabled in development

**Docker Structure**:
- `docker/dev/`: Development environment with hot reload
- `docker/test/`: Isolated testing environment  
- `docker/prod/`: Production with Gunicorn

**Package Management**: Uses UV for fast dependency resolution. All commands prefer `uv run` over direct Python execution.

**Code Quality**: 
- Ruff for linting and formatting (configured in pyproject.toml:97-126)
- Line length: 120 characters, target Python 3.11+
- MyPy for type checking with strict mode on `src.app.*` (pyproject.toml:133-144)
- Pytest with asyncio_mode="auto" for testing

**Application Entry Points**:
- Main app: `src/app/main.py` - includes root "/", "/info", and "/health" endpoints
- Direct execution: `python -m src.app.main` runs on 0.0.0.0:8000 with auto-reload