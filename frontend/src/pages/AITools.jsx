import { useState } from 'react'
import { Sparkles, MessageSquare, FileText } from 'lucide-react'

export default function AITools() {
  const [activeTab, setActiveTab] = useState('chat')

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">AI Tools</h1>

      <div className="flex space-x-4 mb-6 border-b">
        <button
          onClick={() => setActiveTab('chat')}
          className={`pb-4 px-4 border-b-2 transition-colors ${
            activeTab === 'chat'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          <div className="flex items-center space-x-2">
            <MessageSquare className="w-5 h-5" />
            <span>LLM Chat</span>
          </div>
        </button>
        <button
          onClick={() => setActiveTab('rag')}
          className={`pb-4 px-4 border-b-2 transition-colors ${
            activeTab === 'rag'
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-600 hover:text-gray-900'
          }`}
        >
          <div className="flex items-center space-x-2">
            <FileText className="w-5 h-5" />
            <span>RAG</span>
          </div>
        </button>
      </div>

      {activeTab === 'chat' && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Chat with LLM</h2>
          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4 min-h-[400px]">
              <p className="text-gray-500 text-center mt-20">
                Chat interface will be displayed here
              </p>
            </div>
            <div className="flex space-x-4">
              <input
                type="text"
                placeholder="Type your message..."
                className="input flex-1"
              />
              <button className="btn btn-primary">Send</button>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'rag' && (
        <div className="card">
          <h2 className="text-xl font-semibold mb-4">Retrieval Augmented Generation</h2>
          <p className="text-gray-600 mb-4">
            Upload documents and query them using RAG
          </p>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <FileText className="w-12 h-12 mx-auto text-gray-400 mb-4" />
              <p className="text-gray-600 mb-2">Upload documents for RAG</p>
              <p className="text-sm text-gray-500">Supports: PDF, DOCX, TXT, MD</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

