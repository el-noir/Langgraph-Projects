'use client';

import React from 'react';
import { Message } from './ChatInterface';

export interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`message ${isUser ? 'message-user' : 'message-assistant'}`}>
      <div className="message-header">
        <span className="message-role">
          {isUser ? '👤 You' : '🤖 Assistant'}
        </span>
        <span className="message-timestamp">
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </span>
      </div>
      <div className="message-content">
        {message.content || <span className="message-loading">Thinking...</span>}
      </div>
    </div>
  );
};

export default ChatMessage;
