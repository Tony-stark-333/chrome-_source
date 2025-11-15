import React from 'react';
import type { UploadedFile } from '../types';
import { FileIcon, CloseIcon } from './Icons';

interface FileViewerProps {
  file: UploadedFile;
  onClose: () => void;
}

const FileViewer: React.FC<FileViewerProps> = ({ file, onClose }) => {
  return (
    <div 
      className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6 md:p-8 z-50" 
      onClick={onClose}
    >
      <div 
        className="relative bg-gray-800 border border-gray-700 shadow-2xl rounded-lg max-w-5xl w-full h-[90vh] flex flex-col" 
        onClick={e => e.stopPropagation()}
      >
        <div className="flex-shrink-0 flex justify-between items-center p-4 border-b border-gray-700">
          <div className="flex items-center gap-3 min-w-0">
            <FileIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
            <h2 className="text-lg font-semibold text-white truncate" title={file.name}>
              {file.name}
            </h2>
          </div>
          <button 
            onClick={onClose}
            className="p-2 rounded-full text-gray-400 hover:bg-gray-700 hover:text-white transition-colors"
            aria-label="Close file viewer"
          >
            <CloseIcon className="h-6 w-6" />
          </button>
        </div>
        <div className="flex-grow overflow-auto bg-gray-900/50 rounded-b-lg">
          <pre className="p-4 md:p-6 text-sm text-gray-300 whitespace-pre-wrap break-words">
            <code>
              {file.content}
            </code>
          </pre>
        </div>
      </div>
    </div>
  );
};

export default FileViewer;