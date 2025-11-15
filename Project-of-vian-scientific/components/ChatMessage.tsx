import React, { useMemo } from 'react';
import type { ChatMessage } from '../types';
import { UserIcon, BotIcon } from './Icons';

interface ChatMessageProps {
  message: ChatMessage;
  isStreaming?: boolean;
}

declare const marked: any;
declare const DOMPurify: any;

const ChatMessageComponent: React.FC<ChatMessageProps> = ({ message, isStreaming }) => {
  const isUser = message.role === 'user';
  const isSystem = message.role === 'system';

  const renderedContent = useMemo(() => {
    if (isUser || isSystem) {
      return { __html: message.content.replace(/\n/g, '<br />') };
    }

    if (typeof marked !== 'undefined' && typeof DOMPurify !== 'undefined') {
      const rawMarkup = marked.parse(message.content, {
        gfm: true,
        breaks: true,
      });
      let sanitizedMarkup = DOMPurify.sanitize(rawMarkup);
      if (isStreaming) {
        // For markdown content, the cursor should be outside the last paragraph if any
        if (sanitizedMarkup.endsWith('</p>')) {
          sanitizedMarkup = sanitizedMarkup.slice(0, -4) + '<span class="blinking-cursor"></span></p>';
        } else {
          sanitizedMarkup += '<span class="blinking-cursor"></span>';
        }
      }
      return { __html: sanitizedMarkup };
    }
    
    let fallbackContent = message.content.replace(/\n/g, '<br />');
    if (isStreaming) {
      fallbackContent += '<span class="blinking-cursor"></span>';
    }
    return { __html: fallbackContent };
  }, [message.content, isUser, isSystem, isStreaming]);


  if (isSystem) {
    return (
      <div className="text-center my-4">
        <span className="text-xs text-gray-500 bg-gray-800 px-3 py-1 rounded-full">{message.content}</span>
      </div>
    );
  }

  return (
    <div className={`flex items-start gap-4 my-6 ${isUser ? 'justify-end' : ''}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-full bg-indigo-500 flex items-center justify-center flex-shrink-0">
          <BotIcon className="w-5 h-5 text-white" />
        </div>
      )}
      <div className={`max-w-md lg:max-w-3xl px-5 py-3 rounded-2xl ${isUser ? 'bg-blue-600 rounded-br-none' : 'bg-gray-700 rounded-bl-none'}`}>
        <div 
          className="text-white prose prose-invert max-w-none" 
          dangerouslySetInnerHTML={renderedContent} 
        />
      </div>
       {isUser && (
        <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0">
          <UserIcon className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  );
};

export default ChatMessageComponent;