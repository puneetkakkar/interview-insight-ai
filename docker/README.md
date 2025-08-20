# Docker Configuration

This directory contains all Docker-related configuration files organized by environment for better maintainability and clarity.

## 📁 Directory Structure

```
docker/
├── README.md                    # This file
├── dev/                     # Development environment
│   ├── Dockerfile.dev      # Development Dockerfile
│   └── docker-compose.dev.yml
├── test/                    # Testing environment
│   ├── Dockerfile.test     # Testing Dockerfile
│   └── docker-compose.test.yml
└── prod/                    # Production environment
    ├── Dockerfile.prod      # Production Dockerfile
    └── docker-compose.prod.yml
```

## 🏗️ Environment Overview

### Development Environment (`dev/`)
- **Purpose**: Local development with hot-reload
- **Ports**: API on 8000, Database on 5433
- **Features**: 
  - Source code mounted as volumes for live editing
  - Auto-reload enabled
  - Debug mode enabled
  - Development dependencies included

### Testing Environment (`test/`)
- **Purpose**: Isolated testing with dedicated database
- **Ports**: API on internal, Database on 5434
- **Features**:
  - Separate test database
  - No external port exposure for API
  - Optimized for running tests
  - Clean environment for each test run

### Production Environment (`prod/`)
- **Purpose**: Production deployment
- **Ports**: API on 8001, Database on 5436
- **Features**:
  - Gunicorn with multiple workers
  - Production-optimized settings
  - Health checks and monitoring
  - Persistent data volumes

## 🚀 Usage

### Development
```bash
make dev-up      # Start development environment
make dev-down    # Stop development environment
make dev-logs    # View development logs
```

### Testing
```bash
make test-env    # Run tests in dedicated environment
make test-down   # Stop testing environment
```

### Production
```bash
make prod-up     # Start production environment
make prod-down   # Stop production environment
make prod-logs   # View production logs
```

### Utility
```bash
make clean       # Remove all containers and volumes
```

## 🔧 Configuration

### Environment Variables
Each environment uses the same `.env` file but with different configurations:
- `ENVIRONMENT`: Set automatically per environment
- `DEBUG`: Enabled in dev, disabled in test/prod
- `RELOAD`: Enabled in dev, disabled in test/prod

### Database Configuration
- **Development**: Uses `fastapi_db` database
- **Testing**: Uses `fastapi_test_db` database (isolated)
- **Production**: Uses production database with persistent volumes

### Port Mapping
- **Development**: API (8000), DB (5433)
- **Testing**: API (internal), DB (5434)
- **Production**: API (8001), DB (5436)

## 🐳 Docker Images

### Base Images
- **Python**: 3.11-slim for all environments
- **PostgreSQL**: 15 for database

### Multi-stage Builds
- **Development**: Includes development tools and dependencies
- **Testing**: Minimal setup for running tests
- **Production**: Optimized runtime with Gunicorn

## 📋 Best Practices

### Development
- Use volume mounts for live code editing
- Enable debug mode and auto-reload
- Mount source code and tests directories

### Testing
- Isolate test database from development
- Use minimal container configuration
- Ensure clean environment for each test run

### Production
- Use multi-worker Gunicorn setup
- Implement health checks
- Use persistent volumes for data
- Disable debug features

## 🔍 Troubleshooting

### Common Issues

**Port Conflicts**
```bash
# Check what's using a port
lsof -i :8000

# Change ports in docker-compose files if needed
```

**Database Connection Issues**
```bash
# Check container health
docker compose -f docker/environments/dev/docker-compose.dev.yml ps

# View database logs
docker compose -f docker/environments/dev/docker-compose.dev.yml logs db-dev
```

**Build Issues**
```bash
# Clean and rebuild
make clean
make dev-up
```

### Logs and Debugging
```bash
# View logs for specific environment
make dev-logs
make prod-logs

# View logs for specific service
docker compose -f docker/environments/dev/docker-compose.dev.yml logs api-dev
```

## 🔄 Maintenance

### Updating Dependencies
```bash
# Rebuild containers after dependency changes
make dev-down
make dev-up
```

### Database Migrations
```bash
# Run migrations in development
make migrate
```

### Cleanup
```bash
# Remove all containers and volumes
make clean
```

---

**Note**: Always use the Makefile commands for consistency across environments. The environment-specific Docker Compose files are automatically referenced by the Makefile.
