# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Development Commands

### Development Server
- **Start development**: `pnpm dev` (Next.js 15 with Turbo)
- **Build for production**: `pnpm build`
- **Start production**: `pnpm start`
- **Preview build**: `pnpm preview` (builds and starts)

### Code Quality
- **Lint code**: `pnpm lint` or `pnpm lint:fix` (ESLint with TypeScript rules)
- **Type checking**: `pnpm typecheck` or `tsc --noEmit`
- **Format code**: `pnpm format:write` (Prettier with Tailwind plugin)
- **Check formatting**: `pnpm format:check`
- **Full check**: `pnpm check` (runs linting and type checking)

### Package Management
Use **pnpm** as the package manager (specified in package.json). Commands:
- `pnpm install` - Install dependencies
- `pnpm add <package>` - Add dependency
- `pnpm add -D <package>` - Add dev dependency

## Architecture Overview

This is a Next.js 15 frontend using the modern App Router architecture with TypeScript, shadcn/ui, and Tailwind CSS.

### Key Architectural Patterns

**Next.js App Router Structure**:
- `src/app/`: Route-based file structure
- `src/app/layout.tsx`: Root layout with fonts and navigation
- `src/app/page.tsx`: Homepage component
- `src/app/api/`: API routes (backend proxy layer)

**shadcn/ui Component System**:
- `src/components/ui/`: Radix UI-based components with Tailwind variants
- `components.json`: shadcn/ui configuration (New York style, Zinc base color)
- Components use `class-variance-authority` for variant management
- All components follow accessibility standards with ARIA attributes

**Environment & Configuration**:
- `src/env.js`: Type-safe environment variables using @t3-oss/env-nextjs
- `BACKEND_URL` defaults to `http://localhost:8000` for API proxying
- Environment validation with Zod schemas

**Styling Architecture**:
- Tailwind CSS 4.0 with CSS variables for theming
- `src/styles/globals.css`: Global styles and CSS custom properties
- Mobile-first responsive design approach
- `cn()` utility function combining clsx and tailwind-merge

### Critical Components

**API Layer** (`src/app/api/agent/route.ts`):
- Proxies requests to the FastAPI backend
- Handles GET (list agents) and POST (invoke agent) operations
- Type-safe request/response validation
- Error handling with consistent response format

**Navigation** (`src/components/navigation.tsx`):
- Responsive navigation with mobile hamburger menu
- Client-side routing with `usePathname` for active states
- Accessible menu toggle functionality
- Uses Lucide React icons

**UI Components** (`src/components/ui/`):
- Built on Radix UI primitives for accessibility
- Consistent variant system using CVA (class-variance-authority)
- Components include: Button, Input, Card, Select, Textarea, Badge, Alert, Tabs
- All components export TypeScript interfaces

## Development Workflow

### Project Setup
This is a T3 Stack-inspired project (ct3aMetadata indicates Create T3 App v7.39.3):
1. Environment variables configured in `src/env.js`
2. TypeScript strict mode enabled
3. Path aliases configured: `@/*` maps to `src/*`

### Adding New Components
1. Use shadcn/ui CLI: `pnpx shadcn@latest add <component>`
2. Components auto-configured to `src/components/ui/`
3. Follow existing variant patterns using CVA
4. Import from `@/components/ui` barrel export

### API Development
- API routes in `src/app/api/` act as backend proxies
- Use environment validation from `src/env.js`
- Follow existing error handling patterns
- All API routes return consistent response format

### Styling Guidelines
- Use Tailwind utility classes with `cn()` helper
- CSS variables defined in `globals.css` for theming
- Mobile-first responsive design
- Prefer semantic color tokens (e.g., `text-foreground` over specific colors)

## Configuration Details

**TypeScript**: Strict mode with type checking, path aliases, and Next.js plugin
**ESLint**: TypeScript-aware rules with Next.js config and custom type import preferences
**Prettier**: Tailwind CSS class sorting with plugin
**Tailwind**: Version 4.0 with CSS variables, New York style base

## Important Notes

**Package Manager**: Locked to pnpm@10.15.0 - use pnpm for all operations
**Environment**: Uses @t3-oss/env-nextjs for type-safe environment validation
**Components**: Built on Radix UI primitives, not raw HTML elements
**Icons**: Lucide React for consistent iconography
**Fonts**: Geist Sans and Geist Mono loaded from Google Fonts

**Backend Integration**: 
- Frontend acts as a proxy to FastAPI backend on port 8000
- Agent API endpoints mirror backend structure
- Environment variables handle backend URL configuration