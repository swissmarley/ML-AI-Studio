import { BookOpen, Plus } from 'lucide-react'

export default function Notebooks() {
  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Jupyter Notebooks</h1>
        <button className="btn btn-primary flex items-center space-x-2">
          <Plus className="w-5 h-5" />
          <span>New Notebook</span>
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
        </div>
      </div>
    </div>
  )
}

