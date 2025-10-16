'use client';

import { useState } from 'react';
import Sidebar from "./components/Sidebar";
import ChatInterface from "./components/ChatInterface";

export default function Home() {
  const [currentThreadId, setCurrentThreadId] = useState<string | undefined>(undefined);

  const handleThreadChange = (threadId: string) => {
    setCurrentThreadId(threadId);
  };

  const handleNewChat = () => {
    setCurrentThreadId(undefined);
  };

  return (
    <main className="app-container">
      <Sidebar 
        currentThreadId={currentThreadId}
        onThreadSelect={handleThreadChange}
        onNewChat={handleNewChat}
      />
      <ChatInterface 
        currentThreadId={currentThreadId}
        onThreadChange={handleThreadChange}
      />
    </main>
  );
}