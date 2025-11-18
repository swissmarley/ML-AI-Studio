import { useState } from 'react'
import { Sparkles, MessageSquare, FileText, Send } from 'lucide-react'
import api from '../utils/api'
import toast from 'react-hot-toast'

export default function AITools() {
  const [activeTab, setActiveTab] = useState('chat')
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!message.trim()) return

    const userMessage = { role: 'user', content: message }
    setMessages([...messages, userMessage])
    setMessage('')
    setLoading(true)

    try {
      const response = await api.post('/ai-tools/chat', {
        message: userMessage.content,
        model: 'gpt-3.5-turbo',
        max_tokens: 1000
      })

      const assistantMessage = { role: 'assistant', content: response.data.response }
      setMessages([...messages, userMessage, assistantMessage])
    } catch (error) {
      console.error('Chat error:', error)
      let errorMessage = 'Failed to send message'
      
      if (!error.response) {
        errorMessage = 'Network Error: Unable to connect to the server.'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast.error(errorMessage)
      setMessages([...messages, userMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

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
            <div className="bg-gray-50 rounded-lg p-4 min-h-[400px] max-h-[500px] overflow-y-auto">
              {messages.length === 0 ? (
                <p className="text-gray-500 text-center mt-20">
                  Start a conversation by typing a message below
                </p>
              ) : (
                <div className="space-y-4">
                  {messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          msg.role === 'user'
                            ? 'bg-primary-600 text-white'
                            : 'bg-white border border-gray-200'
                        }`}
                      >
                        <p className="text-sm">{msg.content}</p>
                      </div>
                    </div>
                  ))}
                  {loading && (
                    <div className="flex justify-start">
                      <div className="bg-white border border-gray-200 rounded-lg p-3">
                        <p className="text-sm text-gray-500">Thinking...</p>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            <div className="flex space-x-4">
              <input
                type="text"
                placeholder="Type your message..."
                className="input flex-1"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <button 
                onClick={handleSendMessage}
                disabled={loading || !message.trim()}
                className="btn btn-primary flex items-center space-x-2"
              >
                <Send className="w-4 h-4" />
                <span>Send</span>
              </button>
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

