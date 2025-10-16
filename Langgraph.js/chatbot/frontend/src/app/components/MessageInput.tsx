'use client';

import React, { useState, KeyboardEvent } from 'react';

export interface MessageInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  onStop?: () => void;
  isLoading?: boolean;
}

export const MessageInput: React.FC<MessageInputProps> = ({ 
  onSend, 
  disabled = false,
  onStop,
  isLoading = false
}) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input);
      setInput('');
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="message-input-container">
      <div className="message-input-wrapper">
        <textarea
          className="message-input"
          placeholder="Type your message... (Shift+Enter for new line)"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
        />
        <div className="message-input-actions">
          {isLoading && onStop ? (
            <button 
              onClick={onStop}
              className="stop-button"
              type="button"
            >
              ⏹ Stop
            </button>
          ) : (
            <button 
              onClick={handleSend}
              disabled={disabled || !input.trim()}
              className="send-button"
              type="button"
            >
              ↑ Send
            </button>
          )}
        </div>
      </div>
      <div className="message-input-hint">
        Press Enter to send, Shift+Enter for new line
      </div>
    </div>
  );
};

export default MessageInput;
