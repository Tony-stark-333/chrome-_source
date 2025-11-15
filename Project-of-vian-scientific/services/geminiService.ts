import { GoogleGenAI, Chat } from "@google/genai";
import type { UploadedFile } from '../types';

const API_KEY = process.env.API_KEY;

if (!API_KEY) {
  throw new Error("API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

export const createChatWithProjectContext = (files: UploadedFile[]): Chat => {
  const fileContents = files.map(file => 
    `---\nFile: \`${file.name}\`\n\`\`\`\n${file.content}\n\`\`\`\n---`
  ).join('\n\n');

  const history = [
    {
      role: "user" as const,
      parts: [{ text: `
        You are an expert software engineer and project analysis assistant.
        I have provided you with the complete source code for a project.
        Analyze the following project files and prepare to answer my questions about them.

        Here are the files:
        ${fileContents}
      `}],
    },
    {
      role: "model" as const,
      parts: [{ text: "I have analyzed the provided project files. I am ready to answer your questions about the code, architecture, and overall structure." }],
    }
  ];

  const chat = ai.chats.create({
    model: 'gemini-2.5-flash',
    history: history,
  });

  return chat;
};