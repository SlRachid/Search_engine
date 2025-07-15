# AI Search Engine Frontend

A modern, responsive React TypeScript frontend for the AI Search Engine. Built with Tailwind CSS and Lucide React icons.

## Features

- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 🔍 **Advanced Search**: Support for clustering, semantic, and vector search
- ⚡ **Real-time Status**: Live engine health and statistics monitoring
- 📱 **Mobile Responsive**: Works perfectly on all device sizes
- 🎯 **Interactive Results**: Expandable search results with copy functionality
- 🔧 **TypeScript**: Full type safety and better development experience

## Quick Start

### Prerequisites

- Node.js 16+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start the development server:**
```bash
npm start
```

3. **Open your browser:**
Navigate to `http://localhost:3000`

### Building for Production

```bash
npm run build
```

The build files will be created in the `build/` directory.

## Project Structure

```
frontend/
├── public/                 # Static files
├── src/
│   ├── components/         # React components
│   │   ├── SearchBar.tsx   # Main search interface
│   │   ├── SearchResults.tsx # Results display
│   │   └── StatusBar.tsx   # Engine status monitoring
│   ├── services/           # API services
│   │   └── api.ts          # Backend communication
│   ├── types/              # TypeScript definitions
│   │   └── index.ts        # API response types
│   ├── App.tsx             # Main application component
│   ├── index.tsx           # Application entry point
│   └── index.css           # Global styles with Tailwind
├── package.json            # Dependencies and scripts
├── tailwind.config.js      # Tailwind CSS configuration
├── tsconfig.json           # TypeScript configuration
└── README.md               # This file
```

## Components

### SearchBar
- Main search input with autocomplete suggestions
- Advanced options panel (search type, result count)
- Loading states and validation

### SearchResults
- Expandable result cards
- Copy to clipboard functionality
- Score and metadata display
- Responsive grid layout

### StatusBar
- Real-time engine health monitoring
- Statistics display (posts, topics, GPU/CPU mode)
- Model and embedding status indicators

## API Integration

The frontend communicates with the backend through the `api.ts` service:

```typescript
// Search for documents
const results = await searchAPI.search(query, topN, searchType);

// Get engine statistics
const stats = await searchAPI.getStats();

// Check engine health
const health = await searchAPI.healthCheck();
```

## Configuration

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Tailwind CSS

The project uses Tailwind CSS for styling. Custom colors and animations are defined in `tailwind.config.js`.

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

### Code Style

- TypeScript for type safety
- Functional components with hooks
- Tailwind CSS for styling
- Lucide React for icons

## Deployment

### Build and Deploy

1. Build the application:
```bash
npm run build
```

2. Deploy the `build/` directory to your web server

### Docker (Optional)

```dockerfile
FROM node:16-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## Troubleshooting

### Common Issues

1. **Backend Connection Error**
   - Ensure the backend API is running on `http://localhost:8000`
   - Check CORS settings in the backend

2. **Build Errors**
   - Clear node_modules and reinstall: `rm -rf node_modules && npm install`
   - Check TypeScript errors: `npx tsc --noEmit`

3. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check that `index.css` imports Tailwind directives

### Development Tips

- Use React Developer Tools for debugging
- Check the browser console for API errors
- Monitor the Network tab for request/response details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here] 