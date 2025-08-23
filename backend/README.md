# FRAI Boilerplate

A minimal, production-ready FastAPI boilerplate using SQLAlchemy 2.0, Pydantic V2, and optional database storage. This project provides a solid foundation for building scalable web APIs with modern Python practices, perfect for coding interviews and rapid prototyping.

## 🚀 Features

- **FastAPI Framework**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy 2.0**: Latest ORM with async support and type hints
- **Flexible Storage**: Choose between PostgreSQL or in-memory SQLite storage
- **Pydantic V2**: Data validation and serialization with improved performance
- **Docker & Docker Compose**: Containerized development and production environments
- **Comprehensive Testing**: Unit and integration tests with pytest
- **Type Hints**: Full type annotation support throughout the codebase
- **Clean Architecture**: Repository pattern with separation of concerns
- **Logging**: Structured logging with request tracking
- **CORS Support**: Configurable cross-origin resource sharing
- **Health Checks**: Built-in health monitoring endpoints
- **Exception Handling**: Centralized error handling with custom exceptions

### 🤖 AI Features

- **LangGraph Multi-Agent System**: Lightweight multi-agent architecture using LangGraph v0.3
- **Claude Integration**: Anthropic Claude 3.5 Haiku integration via API
- **Research Agent**: Pre-configured research assistant with web search and calculator tools
- **Extensible Architecture**: Easy to add new agents and tools via LangGraph
- **Mock Responses**: Development-friendly mock responses when API keys aren't available

## 🏗️ Architecture

The project follows a clean, layered architecture:

```
src/
├── app/
│   ├── api/           # API endpoints and routing
│   ├── agents/        # AI agents and LangGraph implementation
│   ├── core/          # Core application configuration
│   ├── models/        # SQLAlchemy database models (optional)
│   ├── repositories/  # Data access layer (optional)
│   ├── schemas/       # Pydantic data models
│   └── utils/         # Utility functions
├── data/              # Mock data and cached responses
├── migrations/        # Database migrations (PostgreSQL only)
└── tests/            # Test suite
```

### Key Components

- **Models**: SQLAlchemy models with timestamp and soft delete mixins (optional)
- **Repositories**: Generic CRUD operations with async support (optional)
- **Schemas**: Pydantic models for request/response validation
- **API Routes**: RESTful endpoints with proper error handling
- **Dependencies**: FastAPI dependency injection system
- **Configuration**: Environment-based settings management

### AI Architecture

The AI module provides a lightweight, extensible foundation for AI-powered features:

```
src/app/agents/
├── __init__.py           # Module initialization
├── agent.py              # Multi-agent system with LangGraph
├── research_assistant.py # Research agent implementation
└── tools.py              # Calculator and database search tools
```

- **Multi-Agent System**: Dictionary-based agent registry with LangGraph integration
- **Research Agent**: Pre-configured agent with web search and calculator tools
- **Tool Integration**: Calculator tool using numexpr, web search via DuckDuckGo
- **Claude Integration**: Anthropic API integration for natural language generation
- **Extensible Design**: Easy to add new agents, tools, and capabilities

## 📋 Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional, for PostgreSQL)
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
# Storage Configuration
# Choose between 'postgres' or 'memory'
STORAGE_TYPE=memory

# PostgreSQL Settings (only needed if STORAGE_TYPE=postgres)
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=frai_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password

# AI Settings
ANTHROPIC_API_KEY=your-anthropic-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

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

### 4. AI Configuration

For AI features, you'll need an Anthropic API key:

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Add it to your `.env` file:
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key-here
```

**Note**: AI features work without an API key in development mode using mocked responses for testing.

## 🚀 Quick Start

### In-Memory Storage (Recommended for Interviews)

For coding interviews or quick prototyping, use in-memory storage:

```bash
# Set storage type to memory
echo "STORAGE_TYPE=memory" >> .env

# Start the application
uv run python -m src.app.main
```

This will:
- Start the FastAPI application on port 8000
- Use SQLite in-memory database (no setup required)
- Enable auto-reload for development

### PostgreSQL Storage

For production or when you need persistent data:

```bash
# Set storage type to postgres
echo "STORAGE_TYPE=postgres" >> .env

# Start with Docker Compose
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

### 🤖 AI API Endpoints

The AI module provides the following endpoints:

#### Agents
- `GET /api/v1/agent/` - List all available agents
- `POST /api/v1/agent/{agent_id}/invoke` - Invoke a specific agent
- `POST /api/v1/agent/invoke` - Invoke the default agent

#### Example Usage

```bash
# List available agents
curl http://localhost:8000/api/v1/agent/

# Invoke research agent
curl -X POST http://localhost:8000/api/v1/agent/research-assistant/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2+2?", "model": "claude-3-5-haiku-latest"}'

# Invoke default agent
curl -X POST http://localhost:8000/api/v1/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Wikipedia"}'
```

## 🗄️ Database Management

### Storage Options

The application supports two storage modes:

#### 1. In-Memory Storage (Default for Interviews)
- **Configuration**: `STORAGE_TYPE=memory`
- **Database**: SQLite in-memory
- **Pros**: No setup required, instant startup, perfect for interviews
- **Cons**: Data is lost on restart, no persistence

#### 2. PostgreSQL Storage
- **Configuration**: `STORAGE_TYPE=postgres`
- **Database**: PostgreSQL with async driver
- **Pros**: Persistent data, production-ready, full SQL features
- **Cons**: Requires database setup, slower startup

### Switching Storage Types

To switch between storage types:

```bash
# For in-memory (coding interviews)
export STORAGE_TYPE=memory

# For PostgreSQL
export STORAGE_TYPE=postgres

# Or edit .env file
echo "STORAGE_TYPE=memory" > .env
```

### PostgreSQL Migrations

When using PostgreSQL, you can manage migrations:

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

## 🧪 Testing

### Run Tests Locally

```bash
make test
```

### Run Tests with Coverage

```bash
make test-all
```

### Run Tests in Docker Environment

```bash
make test-env
```

### Test Coverage Report

After running coverage, you'll find an HTML report in the `htmlcov/` directory.

## 🤖 AI Development

### Current Agents

The system currently includes:

- **Research Assistant**: A research agent with web search and calculator capabilities
  - Web search via DuckDuckGo
  - Mathematical calculations using numexpr
  - Claude 3.5 Haiku integration

### Adding New Agents

To add a new agent, extend the agents dictionary in `src/app/agents/agent.py`:

```python
# Add your new agent
agents["custom"] = Agent(
    description="A custom agent for specific tasks.",
    graph=create_custom_agent()
)
```

### Adding New Tools

Extend the tools list in your agent creation function:

```python
def create_custom_agent():
    # Add your custom tools
    custom_tools = [your_custom_tool, another_tool]
    
    # Create agent with tools
    agent = StateGraph(AgentState)
    agent.add_node("tools", ToolNode(custom_tools))
    # ... rest of agent setup
```

### Supported Language Models

The system supports multiple language model providers:

- **Anthropic**: Claude 3.5 Haiku, Claude 3 Haiku, Claude Sonnet 4.0
- **OpenAI**: GPT-4o, GPT-4o Mini
- **Fake Models**: For testing without API keys

### Claude Prompt Engineering

Use Claude prompts to extend functionality:

- **Add Database Tools**: "Prompt Claude to add database query tools to the research agent"
- **Custom Workflows**: "Prompt Claude to design a workflow agent for business processes"
- **New Agent Types**: "Prompt Claude to create specialized agents for different domains"

## 🐳 Docker Commands

The project uses an environment-based Docker structure for better organization:

```
docker/
├── dev/     # Development environment
├── test/    # Testing environment  
└── prod/    # Production environment
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
│   ├── app/
│   │   ├── agents/                 # AI and LangGraph modules
│   │   │   ├── __init__.py         # AI module initialization
│   │   │   ├── agent.py            # Multi-agent system
│   │   │   ├── research_assistant.py # Research agent implementation
│   │   │   └── tools.py            # Calculator and search tools
│   │   ├── api/                    # API endpoints
│   │   │   └── v1/                 # API version 1
│   │   │       └── agent.py        # AI Agent API
│   │   ├── core/                   # Core application logic
│   │   │   ├── config.py           # Configuration management
│   │   │   ├── db/                 # Database setup
│   │   │   ├── exceptions/         # Custom exceptions
│   │   │   ├── llm.py              # Language model management
│   │   │   ├── logger.py           # Logging configuration
│   │   │   ├── response.py         # Response formatting
│   │   │   └── setup.py            # Application setup
│   │   ├── models/                 # Database models (optional)
│   │   ├── repositories/           # Data access layer (optional)
│   │   ├── schemas/                # Pydantic schemas
│   │   └── main.py                 # Application entry point
│   ├── data/                       # Mock data and cached responses
│   └── utils/                      # Utility functions
├── migrations/                     # Database migrations (PostgreSQL only)
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
| `STORAGE_TYPE` | Storage type: 'postgres' or 'memory' | `postgres` |
| `ENVIRONMENT` | Application environment (development/testing/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `RELOAD` | Enable auto-reload | `true` |
| `POSTGRES_SERVER` | PostgreSQL server host (only if STORAGE_TYPE=postgres) | `localhost` |
| `POSTGRES_PORT` | PostgreSQL server port (only if STORAGE_TYPE=postgres) | `5432` |
| `POSTGRES_DB` | PostgreSQL database name (only if STORAGE_TYPE=postgres) | `frai_db` |
| `POSTGRES_USER` | PostgreSQL username (only if STORAGE_TYPE=postgres) | `postgres` |
| `POSTGRES_PASSWORD` | PostgreSQL password (only if STORAGE_TYPE=postgres) | `postgres` |
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude | `None` (optional) |
| `OPENAI_API_KEY` | OpenAI API key for GPT models | `None` (optional) |

### Storage Configuration

The application automatically configures itself based on the `STORAGE_TYPE` setting:

- **`STORAGE_TYPE=memory`**: Uses SQLite in-memory database, perfect for coding interviews
- **`STORAGE_TYPE=postgres`**: Uses PostgreSQL with full database features

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set `ENVIRONMENT=production` and `DEBUG=false`
2. **Storage Type**: Choose between `memory` (for stateless) or `postgres` (for persistent)
3. **API Keys**: Ensure proper API keys are set for AI features
4. **CORS**: Restrict allowed origins
5. **Logging**: Configure production logging levels
6. **Monitoring**: Add health checks and metrics

### Docker Production

```bash
make prod-up
```

The production Docker setup includes:
- Gunicorn with multiple workers
- Health checks for database (if using PostgreSQL)
- Persistent volume for PostgreSQL data (if using PostgreSQL)
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

Always backup your database before running migrations in production (PostgreSQL only).

### Security Updates

Keep dependencies updated, especially security-related packages.

## 💡 Coding Interview Tips

This boilerplate is designed to be interview-friendly:

### Quick Start for Interviews
```bash
# Clone and setup in under 2 minutes
git clone <repo>
cd frai-be
echo "STORAGE_TYPE=memory" > .env
uv run python -m src.app.main
```

### Key Benefits for Interviews
- **No Database Setup**: In-memory storage works immediately
- **AI Features Ready**: Research agent with web search and calculator pre-configured
- **Clean Architecture**: Easy to explain and extend
- **Fast Startup**: Application ready in seconds
- **Modern Stack**: Shows knowledge of current best practices

### Common Interview Extensions
- Add new API endpoints
- Implement custom business logic
- Extend the AI agent system
- Add authentication/authorization
- Implement caching strategies

---

**Happy Coding! 🎉**
