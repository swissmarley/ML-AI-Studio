import { useState } from 'react'
import { BookOpen, Plus } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Notebooks() {
  const [loading, setLoading] = useState(false)

  const handleNewNotebook = () => {
    setLoading(true)
    
    // Try to open JupyterLab in a new window
    const jupyterUrl = 'http://localhost:8888'
    const newWindow = window.open(jupyterUrl, '_blank')
    
    if (newWindow) {
      toast.success('Opening JupyterLab...')
    } else {
      toast.error('Please allow popups to open JupyterLab, or click the link below')
    }
    
    setTimeout(() => setLoading(false), 1000)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Jupyter Notebooks</h1>
        <button 
          onClick={handleNewNotebook}
          disabled={loading}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>{loading ? 'Opening...' : 'New Notebook'}</span>
        </button>
      </div>

      <div className="card">
        <div className="text-center py-12">
          <BookOpen className="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 className="text-xl font-semibold mb-2">JupyterLab Integration</h3>
          <p className="text-gray-600 mb-6">
            Access your Jupyter notebooks directly from the platform
          </p>
          <a
            href="http://localhost:8888"
            target="_blank"
            rel="noopener noreferrer"
            className="btn btn-primary inline-flex items-center space-x-2"
          >
            <span>Open JupyterLab</span>
          </a>
          <p className="text-sm text-gray-500 mt-4">
            Note: Make sure JupyterLab is running on port 8888
          </p>
        </div>
      </div>
    </div>
  )
}

