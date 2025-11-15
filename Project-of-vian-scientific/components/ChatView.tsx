import React, { useRef, useEffect } from 'react';
import type { ChatMessage, UploadedFile } from '../types';
import ChatMessageComponent from './ChatMessage';
import { UploadIcon, InformationCircleIcon } from './Icons';

interface ChatViewProps {
  messages: ChatMessage[];
  isLoading: boolean;
  uploadedFiles: UploadedFile[];
  triggerFileUpload: () => void;
  setIsGuideVisible: (visible: boolean) => void;
}

const ChatView: React.FC<ChatViewProps> = ({
  messages,
  isLoading,
  uploadedFiles,
  triggerFileUpload,
  setIsGuideVisible,
}) => {
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="max-w-4xl mx-auto h-full">
      {uploadedFiles.length > 0 ? (
        <>
          {messages.map((msg, index) => (
            <ChatMessageComponent
              key={index}
              message={msg}
              isStreaming={isLoading && msg.role === 'bot' && index === messages.length - 1}
            />
          ))}
          {isLoading && messages.length > 0 && messages[messages.length - 1].role === 'user' && (
            <ChatMessageComponent message={{ role: 'bot', content: 'Thinking...' }} />
          )}
          <div ref={chatEndRef} />
        </>
      ) : (
        <div className="relative flex flex-col items-center justify-center h-full text-center">
          <div className="absolute top-0 right-0 p-4">
            <button
              onClick={() => setIsGuideVisible(true)}
              className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/10"
              aria-label="View setup guide"
            >
              <InformationCircleIcon className="w-6 h-6" />
              <span className="hidden sm:inline">Setup Guide</span>
            </button>
          </div>
          <div className="max-w-2xl">
            <img src="/vian-logo.png" alt="Vian Scientific Logo" className="w-24 h-24 mx-auto mb-6" />
            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-6xl">
              <a href="https://www.vianscientific.com" target="_blank" rel="noopener noreferrer" className="hover:underline">
                Vian Scientific
              </a>
            </h1>
            <p className="mt-6 text-lg leading-8 text-gray-300">
              Your AI-powered project analysis assistant. Upload your project's
              <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.zip</code>
              file to get started. I'll analyze the structure, code, and dependencies to help answer your questions.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <button
                onClick={triggerFileUpload}
                className="flex items-center gap-3 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-500 transition-colors shadow-lg shadow-blue-600/20"
              >
                <UploadIcon className="w-6 h-6" />
                <span>Upload Project ZIP</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatView;