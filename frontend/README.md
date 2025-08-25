# InterviewInsight AI Frontend

> **Modern Next.js 15 Frontend with AI-Powered Transcript Analysis**

A sophisticated, responsive Next.js 15 frontend featuring advanced AI-powered interview transcript analysis capabilities. Built with TypeScript, Tailwind CSS, and shadcn/ui components for a production-ready user experience that transforms interview transcripts into actionable insights.

[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8+-blue.svg)](https://typescriptlang.org)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4.0-38B2AC.svg)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)

## 🚀 Features

### Core Frontend Features
- **Next.js 15**: Latest React framework with App Router and Turbo mode
- **TypeScript**: Full type safety with strict mode and comprehensive type definitions
- **Modern UI**: shadcn/ui component library with Radix UI primitives
- **Responsive Design**: Mobile-first approach with Tailwind CSS 4.0
- **Performance Optimized**: Code splitting, image optimization, and bundle analysis
- **Accessibility**: WCAG AA compliant with proper ARIA attributes and keyboard navigation

### AI-Powered Application Features
- **Interview Transcript Analysis**: Upload and analyze interview transcripts with AI
- **Real-time Processing**: Live analysis with loading states and progress indicators
- **Timeline Visualization**: Interactive timeline with categorized content and timestamps
- **Entity Recognition**: Automatic extraction of people, companies, technologies, and locations
- **Sentiment Analysis**: Identification of highlights and lowlights in conversations
- **Expandable Results**: Collapsible sections for detailed analysis results
- **Session Management**: Client-side state persistence with sessionStorage
- **Error Handling**: Comprehensive error states with retry functionality

### User Experience Features
- **Smart Textarea**: Auto-expanding input with character counting and validation
- **Loading States**: Multiple loading indicators with skeleton animations
- **Theme Support**: CSS variables for light/dark mode theming (ready for implementation)
- **Framer Motion**: Smooth animations and transitions throughout the application

## 🛠️ Tech Stack

### Core Technologies
- **Framework**: Next.js 15 with App Router and Turbo mode
- **Language**: TypeScript 5.8+ with strict mode
- **Runtime**: React 19 with modern hooks and Suspense
- **Package Manager**: pnpm 10.15.0+ (locked version)

### Styling & UI
- **Styling**: Tailwind CSS 4.0 with CSS variables
- **Components**: shadcn/ui (New York style, Zinc base color)  
- **Icons**: Lucide React for consistent iconography
- **Animations**: Framer Motion for smooth transitions
- **Primitives**: Radix UI for accessible component foundations

### Development & Quality
- **Environment Management**: @t3-oss/env-nextjs for type-safe env vars
- **Validation**: Zod for schema validation
- **Code Quality**: ESLint + TypeScript ESLint + Prettier
- **Utils**: clsx + tailwind-merge for conditional styling (cn utility)
- **Theming**: next-themes for theme management
- **Type Safety**: Full TypeScript coverage with path aliases (@/* -> src/*)

## 📦 Available Components

### shadcn/ui Components
- **Button**: Multiple variants (default, destructive, outline, secondary, ghost, link) and sizes (sm, default, lg, icon)
- **Input**: Form input with validation states and proper focus management
- **Label**: Accessible form labels with Radix UI Label primitive
- **Textarea**: Multi-line text input with auto-resize capability
- **Select**: Dropdown selection with keyboard navigation and search
- **Card**: Content containers with header, content, and footer sections
- **Badge**: Status indicators with variant styles (default, secondary, destructive, outline)
- **Separator**: Visual dividers for content sections
- **Alert**: Notification messages with destructive and default variants
- **Tabs**: Tabbed interfaces with proper ARIA attributes

### Custom Application Components
- **TranscriptAnalyzer**: Main interview analysis interface with smart textarea and processing states
- **AnalysisDashboard**: Results display with timeline, entities, and sentiment analysis
- **TimelineAccordion**: Expandable timeline visualization with categorized content
- **ExpandableLists**: Collapsible lists for entities and topics with proper state management
- **LoadingSpinner**: Customizable loading indicators with multiple sizes
- **HeroSection**: Landing page hero with gradient backgrounds and animations
- **Footer**: Application footer with consistent styling
- **ThemeProvider/ThemeToggle**: Theme management components (ready for implementation)

### Component Architecture
- **Variant System**: Class Variance Authority (CVA) for consistent styling variants
- **Accessibility First**: All components follow WCAG 2.1 AA guidelines
- **TypeScript Native**: Full type definitions with proper prop interfaces
- **Responsive Design**: Mobile-first approach with breakpoint-specific styles
- **Animation Support**: Framer Motion integration for smooth transitions

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ (recommended: Node.js 20+)
- pnpm 10.15.0+ (locked version for consistency)
- Backend API running on port 8000 (see backend README)

### Environment Setup

1. **Clone and Install**:
   ```bash
   cd frontend
   pnpm install
   ```

2. **Environment Configuration**:
   Create `.env.local` (optional - defaults work for local development):
   ```bash
   # Backend API URL (defaults to http://localhost:8000)
   BACKEND_URL=http://localhost:8000
   
   # Skip environment validation for Docker builds
   SKIP_ENV_VALIDATION=false
   ```

3. **Start Development Server**:
   ```bash
   pnpm dev
   ```
   This starts the Next.js development server with Turbo mode on http://localhost:3000

4. **Build for Production**:
   ```bash
   pnpm build
   pnpm start
   ```

5. **Quick Preview**:
   ```bash
   pnpm preview  # Builds and starts in one command
   ```

### Development with Backend

The frontend expects the FastAPI backend to be running on port 8000:

1. **Start Backend** (in backend directory):
   ```bash
   # Quick start with in-memory storage
   echo "STORAGE_TYPE=memory" > .env
   uv run python -m src.app.main
   ```

2. **Start Frontend** (in frontend directory):
   ```bash
   pnpm dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                              # Next.js 15 App Router
│   │   ├── layout.tsx                   # Root layout with fonts and providers
│   │   ├── page.tsx                     # Homepage with TranscriptAnalyzer
│   │   ├── analysis/
│   │   │   └── page.tsx                 # Analysis results page with dashboard
│   │   └── api/                         # API routes (backend proxy)
│   │       ├── agent/
│   │       │   └── route.ts             # Agent API proxy
│   │       └── transcript/
│   │           └── analyze/
│   │               └── route.ts         # Transcript analysis API proxy
│   ├── components/                       # React components
│   │   ├── ui/                          # shadcn/ui components
│   │   │   ├── button.tsx               # Button with CVA variants
│   │   │   ├── input.tsx                # Form input component
│   │   │   ├── label.tsx                # Accessible form labels
│   │   │   ├── textarea.tsx             # Multi-line text input
│   │   │   ├── select.tsx               # Dropdown selection
│   │   │   ├── card.tsx                 # Content containers
│   │   │   ├── badge.tsx                # Status indicators
│   │   │   ├── separator.tsx            # Visual dividers
│   │   │   ├── alert.tsx                # Notification messages
│   │   │   ├── tabs.tsx                 # Tabbed interfaces
│   │   │   ├── loading-spinner.tsx      # Custom loading component
│   │   │   ├── button-loader.tsx        # Button with loading states
│   │   │   ├── chips.tsx                # Tag/chip components
│   │   │   └── index.ts                 # Component barrel exports
│   │   ├── transcript-analyzer.tsx      # Main analysis interface
│   │   ├── analysis-dashboard.tsx       # Results dashboard
│   │   ├── timeline-accordion.tsx       # Timeline visualization
│   │   ├── expandable-lists.tsx         # Entity/topic lists
│   │   ├── hero-section.tsx            # Landing page hero
│   │   ├── footer.tsx                  # Application footer
│   │   ├── theme-provider.tsx          # Theme context provider
│   │   └── theme-toggle.tsx            # Theme switching component
│   ├── lib/
│   │   └── utils.ts                    # cn() utility (clsx + tailwind-merge)
│   ├── types/
│   │   └── interview.ts                # TypeScript interfaces for API
│   ├── styles/
│   │   └── globals.css                 # Tailwind + CSS variables
│   └── env.js                          # Type-safe environment validation
├── public/                             # Static assets
│   ├── favicon.ico                     # Application icon
│   └── images/
│       └── interview-analyzer-image.svg # App illustration
├── components.json                     # shadcn/ui configuration
├── next.config.js                      # Next.js configuration
├── tailwind.config.js                  # Tailwind CSS 4.0 config
├── postcss.config.js                   # PostCSS configuration
├── prettier.config.js                  # Prettier configuration
├── eslint.config.js                    # ESLint configuration
├── tsconfig.json                       # TypeScript configuration
├── package.json                        # Dependencies and scripts
└── README.md                          # This documentation
```

## 🎨 Styling & Theming

### CSS Variables
The project uses CSS custom properties for consistent theming:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --secondary: 210 40% 96%;
  /* ... more variables */
}
```

### Tailwind CSS
- **Utility-first**: Rapid UI development
- **Custom colors**: Extended color palette
- **Responsive**: Mobile-first breakpoints
- **Dark mode**: CSS variable-based theming

## 🔧 Component Usage

### Basic Button
```tsx
import { Button } from "@/components/ui/button";

<Button variant="default" size="lg">
  Click me
</Button>
```

### Form with Components
```tsx
import { Input, Label, Button } from "@/components/ui";

<form className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input id="email" type="email" placeholder="Enter email" />
  </div>
  <Button type="submit">Submit</Button>
</form>
```

### Card Layout
```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>
    Content goes here
  </CardContent>
</Card>
```

## 📱 Responsive Design

The frontend is built with a mobile-first approach:

- **Mobile**: Single column layout, optimized touch targets
- **Tablet**: Two-column grid for better space utilization
- **Desktop**: Full-width layout with proper spacing

## ♿ Accessibility

All components follow accessibility best practices:

- **ARIA Labels**: Proper labeling for screen readers
- **Keyboard Navigation**: Full keyboard support
- **Focus Management**: Visible focus indicators
- **Semantic HTML**: Proper HTML structure
- **Color Contrast**: WCAG AA compliant

## 🚀 Performance

- **Next.js 15**: Latest performance optimizations
- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Built-in image optimization
- **Bundle Analysis**: Built-in bundle analyzer
- **TypeScript**: Compile-time error checking

## 🔧 API Integration

### Backend Proxy Layer

The frontend uses Next.js API routes as a proxy layer to the FastAPI backend:

#### Transcript Analysis API
```typescript
// Frontend API call
const response = await fetch("/api/transcript/analyze", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    transcript_text: "Your interview transcript...",
    model: "claude-3-5-haiku-latest",
    custom_categories: ["technical", "behavioral"]
  }),
});
```

#### Environment Configuration
The backend URL is configured through type-safe environment variables:

```typescript
// src/env.js
export const env = createEnv({
  server: {
    BACKEND_URL: z.string().url().default("http://localhost:8000"),
  },
  // ... validation and runtime config
});
```

## 🎨 Application Flow

### User Journey
1. **Landing Page**: User sees hero section with process explanation
2. **Transcript Input**: Smart textarea with auto-expansion and character count
3. **Processing**: Loading states with animated indicators and progress feedback
4. **Results Navigation**: Automatic redirect to analysis page
5. **Analysis Dashboard**: Comprehensive results with expandable sections

### State Management
```typescript
interface InterviewSummaryState {
  transcript: string;
  summary: TranscriptSummary | null;
  isLoading: boolean;
  error: string | null;
}

// Session persistence
sessionStorage.setItem("analysis:summary", JSON.stringify(analysisData.data));
```

## 🧪 Development

### Available Scripts

```bash
# Development
pnpm dev          # Start development server
pnpm build        # Build for production
pnpm start        # Start production server
pnpm preview      # Preview production build

# Code Quality
pnpm lint         # Run ESLint
pnpm lint:fix     # Fix ESLint issues
pnpm format:check # Check Prettier formatting
pnpm format:write # Write Prettier formatting
pnpm typecheck    # Run TypeScript type checking

# Testing (when implemented)
pnpm test         # Run tests
pnpm test:watch   # Run tests in watch mode
```

### Development Workflow

1. **Feature Development**:
   - Create feature branch
   - Implement changes
   - Add tests if applicable
   - Update documentation

2. **Code Quality**:
   - Run linting: `pnpm lint`
   - Check types: `pnpm typecheck`
   - Format code: `pnpm format:write`

3. **Testing**:
   - Build project: `pnpm build`
   - Preview build: `pnpm preview`

## 📚 Dependencies

### Core Dependencies
- **Next.js 15**: React framework
- **React 19**: UI library
- **TypeScript**: Type safety

### UI Dependencies
- **shadcn/ui**: Component library
- **Radix UI**: Accessible primitives
- **Tailwind CSS**: Utility-first CSS
- **Lucide React**: Icon library

### Development Dependencies
- **ESLint**: Code linting
- **Prettier**: Code formatting
- **TypeScript**: Type checking

## 🔮 Future Enhancements

- [ ] **Storybook**: Component documentation
- [ ] **Testing**: Jest + React Testing Library
- [ ] **E2E Testing**: Playwright or Cypress
- [ ] **Internationalization**: i18n support
- [ ] **PWA**: Progressive Web App features
- [ ] **Analytics**: Performance monitoring
- [ ] **Error Boundaries**: Better error handling

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Add tests if applicable**
5. **Update documentation**
6. **Submit a pull request**

### Code Standards
- Follow TypeScript best practices
- Use shadcn/ui component patterns
- Maintain accessibility standards
- Write clear commit messages
- Update relevant documentation

## 📄 License

This project is part of the InterviewInsight AI platform and follows the same licensing terms.

## 🆘 Support

For questions and support:
- Check the component documentation in `src/components/ui/README.md`
- Review the main project README
- Open an issue for bugs or feature requests

---

**Built with ❤️ using modern web technologies**
