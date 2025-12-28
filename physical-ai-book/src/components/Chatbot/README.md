# AI Chatbot Component

This React component provides an interactive chatbot interface for the Physical AI and Humanoid Robotics book.

## Overview

The chatbot component allows users to ask questions about the book content and receive AI-generated responses based on the book's material. The component provides both full-book context and selected-text context modes.

## Features

- Floating chat widget that doesn't disrupt reading flow
- Support for both full-book and selected-text query contexts
- Loading indicators and error handling
- Network connectivity detection
- Accessibility features
- Response source citations

## Props

- `apiUrl` (string, optional): The backend API endpoint URL (default: 'http://localhost:8000/api/query')
- `initialContextMode` (string, optional): Default context mode ('full_book' or 'selected_text', default: 'full_book')

## Usage

```jsx
import Chatbot from './src/components/Chatbot/Chatbot';

function App() {
  return (
    <div>
      <main>
        {/* Your main content */}
      </main>
      <Chatbot
        apiUrl="https://your-api-url.com/api/query"
        initialContextMode="full_book"
      />
    </div>
  );
}
```

## Functionality

### Context Modes
- **Full Book Context**: Searches the entire book for relevant information
- **Selected Text Context**: Focuses on the text currently selected on the page

### User Interactions
1. Users can toggle the chat widget open/closed
2. Users can select text on the page to ask questions about specific content
3. Users can change context modes via the dropdown
4. Users can clear the chat history
5. Users can send questions via the input field

### Accessibility Features
- Proper ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- Semantic HTML structure

## Error Handling

The component includes comprehensive error handling:
- Network connectivity detection
- API timeout handling
- Rate limit error messages
- Service unavailable messages
- Retry logic with exponential backoff

## Styling

The component includes its own CSS file that:
- Provides a responsive design
- Integrates well with Docusaurus themes
- Includes proper spacing and visual hierarchy
- Supports both light and dark modes