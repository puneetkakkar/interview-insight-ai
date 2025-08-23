# FRAI AI Boilerplate - Frontend

A modern, responsive frontend built with Next.js 15, TypeScript, Tailwind CSS, and shadcn/ui components.

## 🚀 Features

- **Modern UI Components**: Built with shadcn/ui for consistent, accessible design
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **TypeScript**: Full type safety and better developer experience
- **Performance**: Optimized with Next.js 15 and modern React patterns
- **Accessibility**: WCAG compliant components with proper ARIA attributes
- **Dark Mode Ready**: CSS variables for easy theming

## 🛠️ Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript 5.8+
- **Styling**: Tailwind CSS 4.0
- **Components**: shadcn/ui component library
- **Icons**: Lucide React
- **State Management**: React hooks
- **Package Manager**: pnpm

## 📦 Available Components

### Core UI Components
- **Button** - Multiple variants and sizes
- **Input** - Form input with validation states
- **Label** - Accessible form labels
- **Textarea** - Multi-line text input
- **Select** - Dropdown selection
- **Card** - Content containers
- **Badge** - Status indicators
- **Separator** - Visual dividers
- **Alert** - Notification messages
- **Tabs** - Tabbed interfaces

### Component Features
- **Variants**: Multiple visual styles for each component
- **Sizes**: Consistent sizing system
- **Accessibility**: ARIA attributes and keyboard navigation
- **Customization**: Easy styling with Tailwind classes
- **Responsive**: Mobile-first design approach

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- pnpm (recommended) or npm

### Installation

1. **Install dependencies**:
   ```bash
   pnpm install
   ```

2. **Start development server**:
   ```bash
   pnpm dev
   ```

3. **Build for production**:
   ```bash
   pnpm build
   ```

4. **Preview production build**:
   ```bash
   pnpm preview
   ```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   └── api/               # API routes
│   ├── components/             # React components
│   │   ├── ui/                # shadcn/ui components
│   │   │   ├── button.tsx     # Button component
│   │   │   ├── input.tsx      # Input component
│   │   │   ├── card.tsx       # Card components
│   │   │   ├── select.tsx     # Select component
│   │   │   ├── textarea.tsx   # Textarea component
│   │   │   ├── badge.tsx      # Badge component
│   │   │   ├── separator.tsx  # Separator component
│   │   │   ├── alert.tsx      # Alert components
│   │   │   ├── tabs.tsx       # Tabs components
│   │   │   ├── index.ts       # Component exports
│   │   │   └── README.md      # Component documentation
│   │   └── README.md          # This file
│   ├── lib/                    # Utility functions
│   │   └── utils.ts           # shadcn/ui utilities
│   └── styles/                 # Global styles
│       └── globals.css        # Tailwind and CSS variables
├── public/                     # Static assets
├── package.json                # Dependencies and scripts
├── tailwind.config.js          # Tailwind configuration
├── tsconfig.json              # TypeScript configuration
└── README.md                  # This file
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

This project is part of the FRAI AI Boilerplate and follows the same licensing terms.

## 🆘 Support

For questions and support:
- Check the component documentation in `src/components/ui/README.md`
- Review the main project README
- Open an issue for bugs or feature requests

---

**Built with ❤️ using modern web technologies**
