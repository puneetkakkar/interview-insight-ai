# Docker Configuration for InterviewInsight AI

This directory contains Docker configurations for different environments of the InterviewInsight AI backend application.

## 🏗️ Architecture

The Docker setup is organized into three distinct environments:

```
docker/
├── dev/     # Development environment
├── test/    # Testing environment  
└── prod/    # Production environment
```

Each environment has its own:
- `Dockerfile` - Container image definition
- `docker-compose.yml` - Service orchestration
- Environment-specific configurations

## 🚀 Quick Start

### Development Environment
```bash
# Start development environment
make dev-up

# Stop development environment
make dev-down

# View logs
make dev-logs
```

### Production Environment
```bash
# Start production environment
make prod-up

# Stop production environment
make prod-down

# View logs
make prod-logs
```

### Testing Environment
```bash
# Start testing environment
make test-env

# Stop testing environment
make test-down
```

## 🔧 Environment Configurations

### Development Environment (`dev/`)
- **Purpose**: Local development and debugging
- **Ports**: 
  - FastAPI: 8000
  - PostgreSQL: 5433
- **Features**: 
  - Hot reload enabled
  - Debug mode enabled
  - Development database
  - Volume mounting for code changes

### Testing Environment (`test/`)
- **Purpose**: Automated testing and CI/CD
- **Ports**:
  - FastAPI: 8002
  - PostgreSQL: 5434
- **Features**:
  - Isolated test database
  - No volume mounting
  - Optimized for testing

### Production Environment (`prod/`)
- **Purpose**: Production deployment
- **Ports**:
  - FastAPI: 8001
  - PostgreSQL: 5436
- **Features**:
  - Gunicorn with multiple workers
  - Production database
  - Health checks
  - Optimized for performance

## 🗄️ Database Configuration

### Database Names
- **Development**: Uses `interview_insight_dev_db` database
- **Testing**: Uses `interview_insight_test_db` database (isolated)
- **Production**: Uses `interview_insight_db` database

### Database Volumes
Each environment uses separate Docker volumes to ensure data isolation:
- `postgres-data-dev` - Development data
- `postgres-data-test` - Test data
- `postgres-data-prod` - Production data

## 🐳 Docker Commands

### Make Commands
The project includes a comprehensive Makefile for Docker operations:

```bash
# Development
make dev-up      # Start development environment
make dev-down    # Stop development environment
make dev-logs    # View development logs

# Production
make prod-up     # Start production environment
make prod-down   # Stop production environment
make prod-logs   # View production logs

# Testing
make test-env    # Start testing environment
make test-down   # Stop testing environment

# Utility
make clean       # Remove all containers and volumes
make format      # Format code with ruff
make lint        # Run linting checks
```

### Manual Docker Commands
```bash
# Development
cd docker/dev
docker-compose up -d

# Production
cd docker/prod
docker-compose up -d

# Testing
cd docker/test
docker-compose up -d
```

## 🔧 Customization

### Environment Variables
Each environment can be customized using `.env` files:

```bash
# Development
cp ../../env.example .env
# Edit .env with your settings

# Production
cp ../../env.example .env
# Edit .env with production settings
```

### Port Configuration
To change ports, modify the `docker-compose.yml` files:

```yaml
ports:
  - "8000:8000"  # Host:Container
```

### Database Configuration
Database settings can be modified in the environment files:

```yaml
environment:
  - POSTGRES_DB=your_database_name
  - POSTGRES_USER=your_username
  - POSTGRES_PASSWORD=your_password
```

## 📊 Monitoring & Health Checks

### Health Endpoints
- **Application Health**: `/health` - Application status
- **Database Health**: `/health/db` - Database connectivity
- **Info Endpoint**: `/info` - Application information

### Logging
Each environment provides comprehensive logging:
- **Application Logs**: FastAPI application logs
- **Database Logs**: PostgreSQL logs
- **Container Logs**: Docker container logs

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**:
   ```bash
   cd docker/prod
   cp ../../env.example .env
   # Edit .env with production values
   ```

2. **Start Services**:
   ```bash
   make prod-up
   ```

3. **Verify Deployment**:
   ```bash
   curl http://localhost:8001/health
   curl http://localhost:8001/info
   ```

### Scaling
The production environment is designed for horizontal scaling:
- **Gunicorn Workers**: Configurable worker processes
- **Database**: Ready for read replicas
- **Load Balancing**: Container-ready for orchestration platforms

## 🔒 Security Considerations

### Production Security
- **Database**: Use strong passwords and restrict access
- **Networks**: Isolate containers in production
- **Secrets**: Use Docker secrets or environment variables
- **Updates**: Regularly update base images

### Development Security
- **Local Only**: Development environment binds to localhost
- **Test Data**: Use non-sensitive test data
- **Isolation**: Separate development and production environments

## 🧪 Testing with Docker

### Running Tests
```bash
# Start test environment
make test-env

# Run tests
make test

# Stop test environment
make test-down
```

### Test Database
The test environment provides:
- Isolated PostgreSQL instance
- Clean database for each test run
- No interference with development data

## 🔄 Maintenance

### Regular Tasks
- **Log Rotation**: Monitor log file sizes
- **Database Backups**: Regular PostgreSQL backups
- **Image Updates**: Update base images for security
- **Volume Cleanup**: Remove unused volumes

### Troubleshooting
```bash
# Check container status
docker ps

# View logs
docker logs <container-name>

# Access container shell
docker exec -it <container-name> /bin/bash

# Check database connectivity
docker exec -it <container-name> psql -U postgres -d interview_insight_db
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [FastAPI Docker Deployment](https://fastapi.tiangolo.com/deployment/docker/)

---

**Happy Containerizing! 🐳**
