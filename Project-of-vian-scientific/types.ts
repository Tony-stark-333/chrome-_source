export interface UploadedFile {
  name: string;
  content: string;
}

// FIX: Add ChatMessage interface to be used in ChatMessage.tsx
export interface ChatMessage {
  role: 'user' | 'bot' | 'system';
  content: string;
}