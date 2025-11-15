import React, { useState, useRef, useCallback } from 'react';
import type { UploadedFile, ChatMessage } from './types';
import FileSidebar from './components/FileSidebar';
import ChatInput from './components/ChatInput';
import ChatView from './components/ChatView';
import FileViewer from './components/FileViewer';
import { createChatWithProjectContext } from './services/geminiService';
import { CloseIcon } from './components/Icons';
import EnvGuide from './components/EnvGuide';
import type { Chat } from '@google/genai';


declare const JSZip: any;

const ALLOWED_EXTENSIONS = ['js', 'jsx', 'ts', 'tsx', 'html', 'css', 'scss', 'json', 'md', 'txt', 'py', 'java', 'c', 'cpp', 'cs', 'go', 'rb', 'php', 'swift', 'kt', 'rs', 'toml', 'yaml', 'yml'];

const App: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [chatSession, setChatSession] = useState<Chat | null>(null);
  const [isGuideVisible, setIsGuideVisible] = useState(false);
  const [viewingFile, setViewingFile] = useState<UploadedFile | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSendMessage = useCallback(async (prompt: string) => {
    if (isLoading || !chatSession) return;
  
    const userMessage: ChatMessage = { role: 'user', content: prompt };
    setMessages(prev => [...prev, userMessage, { role: 'bot', content: '' }]);
    setIsLoading(true);
  
    try {
      const stream = await chatSession.sendMessageStream({ message: prompt });
  
      for await (const chunk of stream) {
        const chunkText = chunk.text;
        setMessages(prev => {
            const newMessages = [...prev];
            const lastMessage = newMessages[newMessages.length - 1];
            lastMessage.content += chunkText;
            return newMessages;
        });
      }
    } catch (error) {
      console.error("Error sending message:", error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      const botErrorMessage: ChatMessage = { role: 'bot', content: `Sorry, an error occurred: ${errorMessage}` };
      // Replace the last, partial message with the error message
      setMessages(prev => [...prev.slice(0, -1), botErrorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [isLoading, chatSession]);

  const handleFileUpload = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (uploadedFiles.length > 0) {
      if (!window.confirm('Uploading a new ZIP file will clear the current session and file context. Are you sure you want to proceed?')) {
        event.target.value = ''; // Reset file input to allow re-selection of the same file
        return;
      }
    }

    if (!file.name.endsWith('.zip')) {
      alert('Please upload a .zip file.');
      event.target.value = '';
      return;
    }

    setIsLoading(true);
    setUploadedFiles([]);
    setChatSession(null);
    setMessages([{ role: 'system', content: `Processing ${file.name}...` }]);
    setViewingFile(null);

    try {
      const zip = await JSZip.loadAsync(file);
      const newFiles: UploadedFile[] = [];
      const promises: Promise<void>[] = [];

      zip.forEach((relativePath: string, zipEntry: any) => {
        if (!zipEntry.dir && !zipEntry.name.startsWith('__MACOSX/') && !zipEntry.name.split('/').pop()?.startsWith('.')) {
          const extension = relativePath.split('.').pop()?.toLowerCase();
          if (extension && ALLOWED_EXTENSIONS.includes(extension)) {
            const promise = zipEntry.async('string').then((content: string) => {
              newFiles.push({ name: relativePath, content });
            });
            promises.push(promise);
          }
        }
      });

      await Promise.all(promises);
      
      setUploadedFiles(newFiles);

      if (newFiles.length > 0) {
        setMessages([{ role: 'system', content: `Initializing AI with ${newFiles.length} files... This may take a moment.` }]);
        try {
          const chat = createChatWithProjectContext(newFiles);
          setChatSession(chat);
          // We clear the first message ("I have analyzed...") from the history for a cleaner UI start
          setMessages([{ role: 'system', content: `Successfully loaded ${newFiles.length} files. You can now ask questions about the project.` }]);
        } catch (error) {
           console.error("Error initializing chat session:", error);
           const errorMessage = error instanceof Error ? error.message : 'Unknown error';
           setMessages([{ role: 'system', content: `Failed to initialize AI session: ${errorMessage}` }]);
           setChatSession(null);
           setUploadedFiles([]);
        }
      } else {
        setMessages([{ role: 'system', content: "No valid files found in the uploaded ZIP. Please ensure your project includes files with supported extensions." }]);
      }
    } catch (error) {
      console.error("Error processing zip file:", error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      setMessages([{ role: 'system', content: `An error occurred while processing the zip file: ${errorMessage}` }]);
    } finally {
      setIsLoading(false);
    }

    event.target.value = '';
  }, [uploadedFiles]);

  const handleClearFiles = useCallback(() => {
    setUploadedFiles([]);
    setChatSession(null);
    setMessages([]);
    setViewingFile(null);
  }, []);

  const triggerFileUpload = () => fileInputRef.current?.click();
  
  const GuideModal = () => (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 md:p-8 z-50" onClick={() => setIsGuideVisible(false)}>
      <div className="relative bg-gray-800 border border-gray-700 shadow-2xl rounded-lg max-w-5xl w-full max-h-[90vh] flex flex-col" onClick={e => e.stopPropagation()}>
        <div className="flex-shrink-0 flex justify-between items-center p-4 border-b border-gray-700">
          <h2 className="text-lg font-semibold text-white">Environment Setup Guide</h2>
          <button 
            onClick={() => setIsGuideVisible(false)}
            className="p-2 rounded-full text-gray-400 hover:bg-gray-700 hover:text-white transition-colors"
            aria-label="Close guide"
          >
            <CloseIcon className="h-6 w-6" />
          </button>
        </div>
        <div className="flex-grow overflow-y-auto">
           <EnvGuide />
        </div>
      </div>
    </div>
  );

  return (
    <div className="flex h-screen w-screen bg-gray-900 text-gray-100 font-sans">
      {isGuideVisible && <GuideModal />}
      {viewingFile && <FileViewer file={viewingFile} onClose={() => setViewingFile(null)} />}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        className="hidden"
        accept=".zip"
      />
      <div className="hidden md:flex md:flex-shrink-0">
         <FileSidebar 
            files={uploadedFiles} 
            onClearFiles={handleClearFiles} 
            onFileSelect={setViewingFile}
         />
      </div>
      <div className="flex flex-col flex-grow">
        <main className="flex-grow overflow-y-auto p-4 md:p-6 lg:p-8">
          <ChatView
            messages={messages}
            isLoading={isLoading}
            uploadedFiles={uploadedFiles}
            triggerFileUpload={triggerFileUpload}
            setIsGuideVisible={setIsGuideVisible}
          />
        </main>
        {uploadedFiles.length > 0 && (
          <ChatInput 
              onSendMessage={handleSendMessage}
              onUploadClick={triggerFileUpload}
              isLoading={isLoading}
              placeholder={chatSession ? "Ask a question about your project..." : "Upload a project to start"}
          />
        )}
      </div>
    </div>
  );
};

export default App;