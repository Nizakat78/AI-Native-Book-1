# Quickstart Guide: RAG Chatbot Integration

## Overview
This guide provides instructions for setting up and running the RAG chatbot integration with the Physical AI book documentation site.

## Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Poetry (for Python dependency management)
- Docker (optional, for containerized development)

## Backend Setup

### 1. Install Python Dependencies
```bash
cd backend  # Navigate to your backend directory
poetry install
```

### 2. Set Environment Variables
Create a `.env` file in the backend directory:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 3. Start the FastAPI Server
```bash
poetry run uvicorn api:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd physical-ai-book  # Navigate to your Docusaurus directory
npm install
```

### 2. Start the Docusaurus Development Server
```bash
npm run start
```

The documentation site will be available at `http://localhost:3000`.

## API Usage

### Query Endpoint
Send a POST request to `/api/query` with the following JSON payload:

```json
{
  "query": "What is the main principle of humanoid locomotion?",
  "selected_text": "Humanoid locomotion requires precise balance control.",
  "context_mode": "selected_text"
}
```

### Example cURL Request
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is the main principle of humanoid locomotion?",
    "selected_text": "Humanoid locomotion requires precise balance control.",
    "context_mode": "selected_text"
  }'
```

## Frontend Integration

The chatbot component will be automatically integrated into all documentation pages. The component appears as a floating widget in the bottom-right corner of the screen.

### Configuration
The chatbot can be configured by modifying the component props in `src/components/Chatbot/index.js`:

```javascript
<Chatbot
  apiUrl="http://localhost:8000/api/query"  // Backend API URL
  initialContextMode="full_book"            // Default context mode
  enableSelectedTextMode={true}             // Enable selected text context
/>
```

## Testing the Integration

### 1. Verify Backend Health
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2025-12-28T10:00:00Z"
}
```

### 2. Test a Query
```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the key concepts in Chapter 1?",
    "context_mode": "full_book"
  }'
```

### 3. End-to-End Test
1. Navigate to the documentation site in your browser
2. Type a question in the chatbot widget
3. Verify that you receive a relevant response based on the book content

## Development Workflow

### Local Development
1. Start both backend and frontend servers
2. Make changes to either component
3. Test the integration end-to-end

### Adding New Features
1. Update the API contracts if adding new endpoints
2. Implement backend functionality
3. Update frontend components to use new features
4. Test thoroughly

## Troubleshooting

### Common Issues

**Issue**: API requests return 404 errors
**Solution**: Verify that the backend server is running and accessible at the configured URL

**Issue**: Slow response times
**Solution**: Check your OpenAI API key and network connectivity; consider implementing caching for frequently asked questions

**Issue**: Chatbot component doesn't appear
**Solution**: Verify that the component is properly imported and rendered in your Docusaurus layout

## Next Steps

1. Implement response streaming for better user experience
2. Add conversation history and session management
3. Enhance error handling and user feedback
4. Add analytics and usage tracking