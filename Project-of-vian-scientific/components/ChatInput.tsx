import React, { useState } from 'react';
import { SendIcon, UploadIcon } from './Icons';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  onUploadClick: () => void;
  isLoading: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, onUploadClick, isLoading, placeholder }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="p-4 bg-gray-800/70 backdrop-blur-sm border-t border-gray-700">
      <div className="relative">
        <button
          onClick={onUploadClick}
          className="absolute left-3 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-blue-400 hover:bg-gray-700 rounded-full transition-colors"
          aria-label="Upload files"
        >
          <UploadIcon className="w-6 h-6" />
        </button>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder || "Ask a question about your project..."}
          className="w-full bg-gray-900 border border-gray-700 rounded-2xl py-3 pr-24 pl-14 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none transition-shadow"
          rows={1}
          disabled={isLoading}
        />
        <button
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-2 bg-blue-600 text-white rounded-full transition-colors disabled:bg-gray-600 disabled:cursor-not-allowed hover:bg-blue-500"
          aria-label="Send message"
        >
          {isLoading ? (
            <div className="w-6 h-6 border-2 border-white/50 border-t-white rounded-full animate-spin"></div>
          ) : (
            <SendIcon className="w-6 h-6" />
          )}
        </button>
      </div>
    </div>
  );
};

export default ChatInput;