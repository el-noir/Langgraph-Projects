'use client';

import React, { useState, useEffect, useRef } from 'react';
import { chatStream, newChat, NewChatResponse } from '@/lib/api';
import ChatMessage from './ChatMessage';
import MessageInput from './MessageInput';

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatInterfaceProps {
  currentThreadId?: string;
  onThreadChange?: (threadId: string) => void;
}

export const ChatInterface: React.FC<ChatInterfaceProps> = ({ 
  currentThreadId, 
  onThreadChange 
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [threadId, setThreadId] = useState<string | undefined>(currentThreadId);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Update thread ID when prop changes
  useEffect(() => {
    if (currentThreadId !== threadId) {
      setThreadId(currentThreadId);
      setMessages([]); // Clear messages when switching threads
      setError(null);
    }
  }, [currentThreadId]);

  const handleNewChat = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      const response: NewChatResponse = await newChat.post();
      
      setThreadId(response.thread_id);
      setMessages([]);
      
      if (onThreadChange) {
        onThreadChange(response.thread_id);
      }
      
      console.log('New chat created:', response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create new chat');
      console.error('Error creating new chat:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!content.trim()) return;

    // Create user message
    const userMessage: Message = {
      id: `user-${Date.now()}`,
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // If no thread ID, create a new chat first
      let currentThread = threadId;
      if (!currentThread) {
        const newChatResponse = await newChat.post();
        currentThread = newChatResponse.thread_id;
        setThreadId(currentThread);
        if (onThreadChange) {
          onThreadChange(currentThread);
        }
      }

      // Create abort controller for this request
      abortControllerRef.current = new AbortController();

      // Stream the response
      const response = await chatStream.post(content, currentThread);
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) {
        throw new Error('No response body reader available');
      }

      // Create assistant message placeholder
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, assistantMessage]);

      let assistantContent = '';

      // Read the SSE stream
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.substring(6));
              
              if (data.chunk) {
                // Handle chunk data - could be BaseMessage or other format
                let textContent = '';
                
                if (typeof data.chunk === 'string') {
                  textContent = data.chunk;
                } else if (data.chunk.content) {
                  textContent = typeof data.chunk.content === 'string' 
                    ? data.chunk.content 
                    : JSON.stringify(data.chunk.content);
                } else if (data.chunk.chunk?.content) {
                  textContent = data.chunk.chunk.content;
                }
                
                if (textContent) {
                  assistantContent += textContent;
                  
                  // Update the assistant message
                  setMessages(prev => 
                    prev.map(msg => 
                      msg.id === assistantMessage.id 
                        ? { ...msg, content: assistantContent }
                        : msg
                    )
                  );
                }
              }
            } catch (parseError) {
              console.warn('Failed to parse SSE data:', line, parseError);
            }
          }
        }
      }

    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') {
        console.log('Request aborted');
      } else {
        const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
        setError(errorMessage);
        console.error('Error sending message:', err);
      }
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleStopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <div className="chat-title">
          <h2>Chat</h2>
          {threadId && (
            <span className="thread-id">Thread: {threadId.slice(0, 8)}...</span>
          )}
        </div>
        <button 
          onClick={handleNewChat}
          disabled={isLoading}
          className="new-chat-button"
        >
          + New Chat
        </button>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-state">
            <h3>Start a new conversation</h3>
            <p>Send a message to begin chatting with the AI assistant.</p>
          </div>
        ) : (
          <>
            {messages.map(message => (
              <ChatMessage key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      <MessageInput 
        onSend={handleSendMessage}
        disabled={isLoading}
        onStop={handleStopGeneration}
        isLoading={isLoading}
      />
    </div>
  );
};

export default ChatInterface;
