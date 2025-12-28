# RAG Chatbot Integration for Physical AI Book

This project integrates a RAG (Retrieval-Augmented Generation) chatbot into the Physical AI and Humanoid Robotics book documentation website, allowing users to ask questions about the book content and receive AI-generated responses.

## Overview

The RAG chatbot system consists of:
- A FastAPI backend that handles query processing
- A React frontend component that provides the chat interface
- Integration with vector databases for document retrieval
- AI model integration for response generation

## Features

- **Interactive Chat Interface**: Floating chat widget that doesn't disrupt the reading experience
- **Dual Context Modes**:
  - Full Book Context: Search the entire book content
  - Selected Text Context: Focus on specific text the user has selected
- **Source Citations**: Responses include references to the original content
- **Error Handling**: Graceful degradation when services are unavailable
- **Accessibility**: Full support for screen readers and keyboard navigation
- **Rate Limiting**: Protection against API abuse

## Architecture

### Backend (FastAPI)
- `/api/query`: Main endpoint for processing user queries
- `/api/health`: Health check endpoint
- Integration with Qdrant vector database for document retrieval
- OpenAI API for response generation
- Built-in caching for frequently asked questions

### Frontend (React/Docusaurus)
- Floating chatbot widget component
- Context mode switching (full book vs selected text)
- Loading indicators and error messages
- Network connectivity detection
- Accessibility features

## Setup and Installation

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `poetry install` (or `pip install -r requirements.txt`)
3. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openai_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   ```
4. Start the server: `uvicorn api:app --reload --port 8000`

### Frontend Setup
1. Navigate to the documentation directory: `cd physical-ai-book`
2. Install dependencies: `npm install`
3. Start the development server: `npm run start`

## API Endpoints

### POST /api/query
Process a user query against book content using RAG.

**Request Body:**
```json
{
  "query": "string (required) - The user's question",
  "selected_text": "string (optional) - Text selected by user for context",
  "context_mode": "enum ['full_book', 'selected_text'] (optional, default: 'full_book')"
}
```

**Response:**
```json
{
  "response": "string - Generated response",
  "sources": "array - Source citations",
  "processing_time": "number - Processing time in seconds",
  "status": "string - Processing status",
  "error_message": "string (optional) - Error details if status is 'error'"
}
```

### GET /api/health
Health check endpoint to verify the service is running.

## Environment Variables

### Backend
- `OPENAI_API_KEY`: OpenAI API key for generating responses
- `QDRANT_URL`: URL for the Qdrant vector database
- `QDRANT_API_KEY`: API key for the Qdrant vector database
- `QDRANT_COLLECTION_NAME`: Name of the collection in Qdrant
- `API_HOST`: Host to bind the API server to (default: 0.0.0.0)
- `API_PORT`: Port to run the API server on (default: 8000)

### Frontend
- `REACT_APP_API_URL`: URL of the backend API (default: http://localhost:8000/api/query)

## Deployment

### Local Development
1. Start the backend server: `cd backend && uvicorn api:app --reload`
2. Start the frontend: `cd physical-ai-book && npm run start`

### Production Deployment
The system is configured for deployment on Vercel and GitHub Pages with appropriate CORS settings.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Troubleshooting

### Common Issues
- **API Connection Errors**: Verify that the backend server is running and accessible
- **Rate Limiting**: The API is limited to 10 requests per minute per IP
- **Slow Responses**: Check your OpenAI API key and network connectivity

### Error Messages
- "Service temporarily unavailable": Try again later
- "Too many requests": Wait before making additional requests
- "Connection timeout": Check your internet connection

## Performance

The system is designed to respond to queries within 5 seconds in 95% of cases. Performance can be affected by:
- Network latency
- Vector database query performance
- AI model response times

## Security

- Input sanitization is performed on all user queries
- Rate limiting prevents API abuse
- API keys are stored securely as environment variables
- CORS is configured to allow only trusted origins

## License

[Add license information here]