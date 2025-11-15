import React from 'react';
import type { UploadedFile } from '../types';
import { FileIcon, TrashIcon } from './Icons';

interface FileSidebarProps {
  files: UploadedFile[];
  onClearFiles: () => void;
  onFileSelect: (file: UploadedFile) => void;
}

const FileSidebar: React.FC<FileSidebarProps> = ({ files, onClearFiles, onFileSelect }) => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-sm p-4 w-full md:w-64 lg:w-80 flex flex-col h-full border-r border-gray-700">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-200">Project Files</h2>
        {files.length > 0 && (
          <button
            onClick={onClearFiles}
            className="p-2 rounded-md text-gray-400 hover:bg-red-500/20 hover:text-red-400 transition-colors"
            aria-label="Clear all files"
          >
            <TrashIcon className="w-5 h-5" />
          </button>
        )}
      </div>
      <div className="flex-grow overflow-y-auto pr-2">
        {files.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p>Upload files and folders to provide context for the AI.</p>
          </div>
        ) : (
          <ul className="space-y-2">
            {files.map((file) => (
              <li key={file.name}>
                <button
                  onClick={() => onFileSelect(file)}
                  className="w-full flex items-center p-2 bg-gray-700/50 rounded-md text-left hover:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <FileIcon className="w-5 h-5 mr-3 text-blue-400 flex-shrink-0" />
                  <span className="text-sm text-gray-300 truncate" title={file.name}>
                    {file.name}
                  </span>
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default FileSidebar;