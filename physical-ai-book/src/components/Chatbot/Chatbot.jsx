import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = ({ apiUrl = 'http://localhost:8000/api/query', initialContextMode = 'full_book' }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [contextMode, setContextMode] = useState(initialContextMode);
  const [selectedText, setSelectedText] = useState('');
  const [isWidgetOpen, setIsWidgetOpen] = useState(false);
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const messagesEndRef = useRef(null);

  // Check network connectivity
  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  // Function to get selected text from the page
  const getSelectedText = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setSelectedText(selectedText);
      setContextMode('selected_text');
    }
    return selectedText;
  };

  // Handle text selection on the page
  useEffect(() => {
    const handleSelection = () => {
      const selected = window.getSelection().toString().trim();
      if (selected) {
        // Optionally notify user that text is selected for context
        console.log('Text selected for context:', selected.substring(0, 50) + '...');
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Check if user is online before making request
    if (!isOnline) {
      const offlineMessage = {
        id: Date.now(),
        text: 'It looks like you are offline. Please check your internet connection and try again.',
        sender: 'bot',
        isError: true,
      };
      setMessages(prev => [...prev, offlineMessage]);
      return;
    }

    // Get current selected text if in selected_text mode
    const currentSelectedText = contextMode === 'selected_text' ?
      window.getSelection().toString().trim() || selectedText :
      null;

    // Add user message to chat
    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);

    const queryToSend = inputValue;
    setInputValue('');
    setIsLoading(true);

    try {
      // Prepare the request payload
      const requestBody = {
        query: queryToSend,
        context_mode: contextMode,
      };

      // Include selected text if in selected_text mode
      if (contextMode === 'selected_text' && currentSelectedText) {
        requestBody.selected_text = currentSelectedText;
      }

      // Function to make API call with retry logic and timeout handling
      const makeRequestWithRetry = async (maxRetries = 3) => {
        let lastError;

        for (let attempt = 1; attempt <= maxRetries; attempt++) {
          try {
            // Create a timeout promise to handle long-running queries
            const timeoutPromise = new Promise((_, reject) => {
              setTimeout(() => reject(new Error('Request timeout after 30 seconds')), 30000);
            });

            // Make the API request
            const requestPromise = fetch(apiUrl, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(requestBody),
            });

            // Race the request against the timeout
            const response = await Promise.race([requestPromise, timeoutPromise]);

            if (!response.ok) {
              throw new Error(`API request failed with status ${response.status}`);
            }

            return await response.json();
          } catch (error) {
            lastError = error;
            console.warn(`Attempt ${attempt} failed:`, error.message);

            // If not the last attempt, wait before retrying
            if (attempt < maxRetries) {
              const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
              await new Promise(resolve => setTimeout(resolve, delay));
            }
          }
        }

        // If all attempts failed, throw the last error
        throw lastError;
      };

      // Make the request with retry logic
      const data = await makeRequestWithRetry();

      // Add bot response to chat
      const botMessage = {
        id: Date.now() + 1,
        text: data.response || 'Sorry, I could not generate a response.',
        sender: 'bot',
        sources: data.sources || [],
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat with more specific handling
      let errorMessageText = 'Sorry, I encountered an error processing your request.';

      if (error.message.includes('timeout')) {
        errorMessageText = 'The request timed out. The system may be busy. Please try again.';
      } else if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        errorMessageText = 'Unable to connect to the server. Please check your internet connection.';
      } else if (error.message.includes('429')) {
        errorMessageText = 'Too many requests. Please wait a moment before trying again.';
      } else if (error.message.includes('503') || error.message.includes('502')) {
        errorMessageText = 'The service is temporarily unavailable. Please try again later.';
      }

      const errorMessage = {
        id: Date.now() + 1,
        text: errorMessageText,
        sender: 'bot',
        isError: true,
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleWidget = () => {
    setIsWidgetOpen(!isWidgetOpen);
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="chatbot-container" role="complementary" aria-label="AI Book Assistant">
      {/* Floating widget button */}
      <button
        className="chatbot-toggle-button"
        onClick={toggleWidget}
        aria-label={isWidgetOpen ? "Close chat" : "Open chatbot assistant"}
        aria-expanded={isWidgetOpen}
        aria-controls="chatbot-widget"
      >
        {isWidgetOpen ? '✕' : '💬'}
      </button>

      {/* Chat widget */}
      {isWidgetOpen && (
        <div id="chatbot-widget" className="chatbot-widget" role="dialog" aria-modal="true" aria-label="AI Assistant Chat Interface">
          <div className="chatbot-header" role="banner">
            <h3>AI Book Assistant</h3>
            <div className="chatbot-controls" role="toolbar">
              <label htmlFor="context-mode-select" className="sr-only">Context Mode</label>
              <select
                id="context-mode-select"
                value={contextMode}
                onChange={(e) => setContextMode(e.target.value)}
                className="context-mode-select"
                disabled={isLoading}
                aria-label="Select context mode"
              >
                <option value="full_book">Full Book Context</option>
                <option value="selected_text">Selected Text Context</option>
              </select>
              <button
                onClick={clearChat}
                className="clear-chat-button"
                disabled={isLoading}
                aria-label="Clear chat history"
              >
                🗑️
              </button>
              <button
                onClick={toggleWidget}
                className="minimize-button"
                aria-label="Minimize chat"
              >
                −
              </button>
            </div>
          </div>

          <div className="chatbot-messages" role="log" aria-live="polite" aria-label="Chat messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome" role="status" aria-live="polite">
                <p>Hello! I'm your AI assistant for the Physical AI and Humanoid Robotics book.</p>
                <p>You can ask me questions about the book content.</p>
                {contextMode === 'selected_text' && (
                  <p>Select text on the page to ask questions about specific content.</p>
                )}
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`chatbot-message ${message.sender}-message`}
                  role="listitem"
                  aria-label={message.sender === 'user' ? 'Your message' : 'Assistant response'}
                >
                  <div className="message-content">
                    <p>{message.text}</p>
                    {message.sources && message.sources.length > 0 && (
                      <div className="message-sources">
                        <details>
                          <summary aria-label="Show sources for this response">Sources</summary>
                          <ul>
                            {message.sources.map((source, idx) => (
                              <li key={idx}>
                                {source.page_reference ? `${source.page_reference}: ` : ''}
                                {source.content.substring(0, 100)}...
                              </li>
                            ))}
                          </ul>
                        </details>
                      </div>
                    )}
                    {message.isError && (
                      <small className="error-message" role="alert" aria-live="assertive">Error occurred, please try again</small>
                    )}
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="chatbot-message bot-message" role="status" aria-live="polite">
                <div className="message-content">
                  <div className="typing-indicator" aria-label="Assistant is typing">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} aria-hidden="true" />
          </div>

          <form onSubmit={handleSubmit} className="chatbot-input-form" role="form" aria-label="Chat input form">
            <label htmlFor="chatbot-input" className="sr-only">Type your question</label>
            <input
              id="chatbot-input"
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder={contextMode === 'selected_text' ?
                "Ask about selected text..." :
                "Ask about the book content..."}
              disabled={isLoading}
              className="chatbot-input"
              aria-label="Type your question"
              autoComplete="off"
              aria-describedby={isLoading ? "loading-indicator" : undefined}
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isLoading}
              className="chatbot-send-button"
              aria-label="Send message"
            >
              {isLoading ? 'Sending...' : 'Send'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;