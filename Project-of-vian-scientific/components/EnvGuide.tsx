import React from 'react';
import { InformationCircleIcon, FileIcon } from './Icons';

const CodeBlock: React.FC<{ language: string, fileName?: string, children: React.ReactNode }> = ({ language, fileName, children }) => (
  <div className="my-4 text-left">
    {fileName && (
        <div className="flex items-center text-sm text-gray-400 bg-gray-800 rounded-t-md px-4 py-2">
            <FileIcon className="w-4 h-4 mr-2" />
            <span>{fileName}</span>
        </div>
    )}
    <pre className={`bg-gray-900 p-4 rounded-b-md ${fileName ? 'rounded-t-none' : 'rounded-md'} overflow-x-auto`}>
      <code className={`language-${language} text-sm`}>
        {children}
      </code>
    </pre>
  </div>
);

const EnvGuide: React.FC = () => {
  return (
    <div className="bg-gray-800/50 backdrop-blur-sm border border-gray-700 rounded-lg p-6 md:p-8 max-w-4xl mx-auto text-gray-300">
      <h1 className="text-2xl md:text-3xl font-bold text-gray-100 mb-4 text-center">
        Environment Setup Guide
      </h1>
      <p className="text-gray-400 mb-6 text-center">
        This guide shows how to create the <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.env</code> file for the Vian Scientific backend. This is a critical step for security as it stores your credentials and must <strong className="text-red-400">not</strong> be committed to your project's history.
      </p>

      <div className="space-y-8">
        <div>
          <h2 className="text-xl font-semibold text-gray-200 border-b border-gray-600 pb-2 mb-4">1. The .env File</h2>
          <p>In your project's backend directory, create a new file named <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.env</code> with the following pre-configured content.</p>
          <CodeBlock language="ini" fileName="app/backend/.env">
{`# Environment variables for Flask and Email Service

# --- Email Configuration ---
# Configured for your Gmail account
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=vrventures.333@gmail.com

# ⚠️ CRITICAL: You must generate an "App Password" from your
# Google Account settings and paste it here.
# Do NOT use your regular Gmail password.
EMAIL_PASS=YOUR_16_CHARACTER_APP_PASSWORD

# --- Flask Configuration ---
# A strong, random secret key for signing sessions and tokens
SECRET_KEY=YOUR_VERY_STRONG_RANDOM_SECRET_KEY_HERE

# The database connection string
DATABASE_URL=sqlite:///app.db`}
          </CodeBlock>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-200 border-b border-gray-600 pb-2 mb-4">2. Generate Your Gmail App Password</h2>
          <div className="flex items-start bg-yellow-900/30 border border-yellow-700 rounded-lg p-4">
            <InformationCircleIcon className="w-6 h-6 text-yellow-400 mr-3 mt-1 flex-shrink-0" />
            <div>
              <h3 className="font-bold text-yellow-300">Action Required: Get Your App Password</h3>
              <p className="text-sm text-yellow-200 mt-1">To send emails, you cannot use your regular Gmail password. You must generate a special 16-character "App Password" from your Google Account settings.</p>
              <ol className="list-decimal list-inside text-sm text-yellow-200/90 mt-2 space-y-1">
                <li>Go to your Google Account settings: <a href="https://myaccount.google.com" target="_blank" rel="noopener noreferrer" className="underline hover:text-white">myaccount.google.com</a></li>
                <li>Go to <strong className="text-yellow-300">Security</strong>.</li>
                <li>Ensure <strong className="text-yellow-300">2-Step Verification</strong> is turned ON. This is required.</li>
                <li>Under "Signing in to Google," click on <strong className="text-yellow-300">App Passwords</strong>.</li>
                <li>Select "Mail" for the app and "Other (Custom name)" for the device.</li>
                <li>Google will generate a 16-character password. Use this for the <code className="bg-gray-700 px-1 py-0.5 rounded">EMAIL_PASS</code> value in your <code className="bg-gray-700 px-1 py-0.5 rounded">.env</code> file.</li>
              </ol>
            </div>
          </div>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-200 border-b border-gray-600 pb-2 mb-4">3. Generate a SECRET_KEY</h2>
          <p>Your <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">SECRET_KEY</code> must be a long, random, and unpredictable string. You can use a password generator or run this Python command to create one:</p>
          <CodeBlock language="bash">
{`python -c "import secrets; print(secrets.token_hex(32))"`}
          </CodeBlock>
          <p>Copy the output and paste it as the value for <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">SECRET_KEY</code> in your <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.env</code> file.</p>
        </div>

        <div>
          <h2 className="text-xl font-semibold text-gray-200 border-b border-gray-600 pb-2 mb-4">4. Secure Your Credentials (Crucial!)</h2>
          <p>Your <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.env</code> file contains secret passwords. You must <strong className="text-red-400">never</strong> commit this file to your project history. To prevent this, add it to your <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.gitignore</code> file.</p>
          <CodeBlock language="ini" fileName=".gitignore">
{`# Python
__pycache__/
*.pyc
.env
venv/
*.db
app.db

# Node
node_modules/
dist/
build/
.npm
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# OS
.DS_Store
Thumbs.db`}
          </CodeBlock>
          <p>By adding <code className="bg-gray-700 px-1 py-0.5 rounded text-sm">.env</code> to this file, Git will ignore it, keeping your passwords safe and out of your repository.</p>
        </div>
      </div>
    </div>
  );
};

export default EnvGuide;