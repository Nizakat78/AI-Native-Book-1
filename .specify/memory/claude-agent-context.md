# Claude Agent Context: RAG Chatbot Integration

## Project Overview
This project involves integrating a RAG (Retrieval-Augmented Generation) chatbot into a Docusaurus-based documentation website for a Physical AI book. The chatbot allows users to ask questions about the book content and receive responses based on the book's content.

## Technical Architecture

### Frontend
- Built with Docusaurus (React-based documentation framework)
- Chatbot UI component integrated as a floating widget
- Communicates with backend via HTTP/JSON API
- Supports both full book context and selected text context queries

### Backend
- FastAPI-based service for handling queries
- Integration with existing RAG pipeline
- Uses vector database (likely Qdrant) for document retrieval
- OpenAI API for response generation

### API Endpoints
- POST /api/query: Process user queries with optional selected text context
- GET /api/health: Health check endpoint

## Key Components

### UserQuery Entity
- query_text: The user's question
- selected_text: Optional selected text for context
- context_mode: 'full_book' or 'selected_text'

### QueryResponse Entity
- response_text: Generated response
- sources: Citations and sources used
- processing_time: Query processing duration
- status: Success/error status

## Integration Patterns

### Frontend Integration
- React component that can be embedded in Docusaurus pages
- Floating widget design that doesn't disrupt reading experience
- Context switching between full book and selected text modes

### Backend Integration
- FastAPI endpoints that integrate with existing RAG pipeline
- Context-aware retrieval based on user selection
- Error handling and graceful degradation

## Best Practices

### User Experience
- Fast response times (target: <5 seconds)
- Clear feedback during query processing
- Proper error handling and user-friendly messages
- Non-intrusive UI that enhances rather than disrupts reading

### Technical Implementation
- Follow existing code patterns and architecture
- Maintain compatibility with Docusaurus build process
- Ensure proper error handling and logging
- Implement appropriate security measures

## Important Constraints

### Not Building
- New ingestion or retrieval logic
- Authentication or user accounts
- Chat history persistence
- UI/UX design system overhaul

### Focus Areas
- Seamless frontend-backend communication
- Accurate response generation based on book content
- Support for both full book and selected text queries
- Local development and GitHub Pages deployment compatibility

## Files and Directories
- Frontend: physical-ai-book/src/components/Chatbot/
- Backend: backend/api.py, backend/agent.py
- Documentation: specs/1-rag-chatbot-integration/