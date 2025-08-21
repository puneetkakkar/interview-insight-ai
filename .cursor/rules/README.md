# Cursor Rules Structure

This directory contains Cursor rules organized in a nested structure that follows the documented approach, with `.cursor/rules/` directories in each project folder.

## Directory Structure

```
.cursor/rules/                    # Project-wide rules
├── README.md                     # This file
└── project-overview.mdc         # Overall project architecture and commands

backend/
├── .cursor/rules/               # Backend-specific rules
│   ├── development.mdc          # Python/FastAPI development guidelines
│   └── docker.mdc              # Backend Docker development

frontend/
└── .cursor/rules/               # Frontend-specific rules
    └── development.mdc          # Next.js/React development guidelines
```

## Rule Organization

### Project-Wide Rules (`.cursor/rules/`)
- **`project-overview.mdc`**: Overall project structure, architecture, and general commands
- Applies to the entire project
- Contains cross-cutting concerns and overview information

### Backend Rules (`backend/.cursor/rules/`)
- **`development.mdc`**: Python 3.11+, FastAPI, SQLAlchemy 2.0, Pydantic V2
- **`docker.mdc`**: Docker environments, Make commands, containerization
- Applies to Python files in the backend directory
- Contains backend-specific development patterns and practices

### Frontend Rules (`frontend/.cursor/rules/`)
- **`development.mdc`**: Next.js 15, React 19, TypeScript, Tailwind CSS
- Applies to TypeScript/React files in the frontend directory
- Contains frontend-specific development patterns and practices

## Benefits of This Structure

1. **Proper Nesting**: Follows the documented Cursor rules structure
2. **Context-Aware**: Rules apply based on file location and type
3. **Maintainable**: Each project area has its own rules
4. **Scalable**: Easy to add new rules for specific technologies
5. **Organized**: Clear separation of concerns by project area
6. **File References**: Uses proper `[filename](mdc:filename)` format for file references

## Usage

- **Project-wide rules** are available for all files
- **Backend rules** apply to Python files in the `backend/` directory
- **Frontend rules** apply to TypeScript/React files in the `frontend/` directory
- **Glob patterns** ensure rules only apply to relevant file types
- **File references** use relative paths from each rule's location

This structure mirrors the documented approach and provides targeted assistance based on what you're working on!
