'use client';

import React, { useState } from 'react';

export interface Thread {
  id: string;
  title: string;
  createdAt: Date;
}

export interface SidebarProps {
  currentThreadId?: string;
  onThreadSelect?: (threadId: string) => void;
  onNewChat?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  currentThreadId, 
  onThreadSelect,
  onNewChat 
}) => {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [isCollapsed, setIsCollapsed] = useState(false);

  const handleThreadClick = (threadId: string) => {
    if (onThreadSelect) {
      onThreadSelect(threadId);
    }
  };

  return (
    <div className={`sidebar ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
      <div className="sidebar-header">
        <button 
          className="sidebar-toggle"
          onClick={() => setIsCollapsed(!isCollapsed)}
          title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {isCollapsed ? '→' : '←'}
        </button>
        {!isCollapsed && <h2>Chat History</h2>}
      </div>

      {!isCollapsed && (
        <>
          <button 
            className="sidebar-new-chat"
            onClick={onNewChat}
          >
            + New Chat
          </button>

          <div className="sidebar-threads">
            {threads.length === 0 ? (
              <div className="sidebar-empty">
                <p>No chat history yet</p>
                <p className="sidebar-hint">Start a new conversation!</p>
              </div>
            ) : (
              threads.map(thread => (
                <div
                  key={thread.id}
                  className={`sidebar-thread ${
                    currentThreadId === thread.id ? 'sidebar-thread-active' : ''
                  }`}
                  onClick={() => handleThreadClick(thread.id)}
                >
                  <div className="sidebar-thread-title">{thread.title}</div>
                  <div className="sidebar-thread-date">
                    {thread.createdAt.toLocaleDateString()}
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default Sidebar;