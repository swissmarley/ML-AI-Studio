import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Plus, Brain, Play } from 'lucide-react'

export default function ModelBuilder() {
  const [showCreateModal, setShowCreateModal] = useState(false)
  const queryClient = useQueryClient()

  const { data: models } = useQuery({
    queryKey: ['models'],
    queryFn: () => api.get('/models').then((res) => res.data),
    onError: (error) => {
      console.error('Error fetching models:', error)
      if (!error.response) {
        toast.error('Network Error: Unable to connect to the server.')
      }
    },
  })

  const createMutation = useMutation({
    mutationFn: (data) => api.post('/models', data),
    onSuccess: () => {
      queryClient.invalidateQueries(['models'])
      setShowCreateModal(false)
      toast.success('Model created!')
    },
    onError: (error) => {
      console.error('Error creating model:', error)
      let errorMessage = 'Failed to create model'
      
      if (!error.response) {
        errorMessage = 'Network Error: Unable to connect to the server.'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast.error(errorMessage)
    },
  })

  const handleCreate = (e) => {
    e.preventDefault()
    const formData = new FormData(e.target)
    createMutation.mutate({
      name: formData.get('name'),
      description: formData.get('description'),
      model_type: formData.get('model_type'),
      algorithm: formData.get('algorithm'),
    })
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Model Builder</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="btn btn-primary flex items-center space-x-2"
        >
          <Plus className="w-5 h-5" />
          <span>Create Model</span>
        </button>
      </div>

      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-semibold mb-4">Create New Model</h2>
            <form onSubmit={handleCreate} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Name
                </label>
                <input name="name" required className="input" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea name="description" className="input" rows="3" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Model Type
                </label>
                <select name="model_type" required className="input">
                  <option value="">Select type</option>
                  <option value="classification">Classification</option>
                  <option value="regression">Regression</option>
                  <option value="clustering">Clustering</option>
                  <option value="time_series">Time Series</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Algorithm
                </label>
                <select name="algorithm" required className="input">
                  <option value="">Select algorithm</option>
                  <option value="random_forest">Random Forest</option>
                  <option value="xgboost">XGBoost</option>
                  <option value="neural_network">Neural Network</option>
                  <option value="svm">SVM</option>
                </select>
              </div>
              <div className="flex space-x-4">
                <button type="submit" className="btn btn-primary flex-1">
                  Create
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn btn-secondary flex-1"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {models && models.length > 0 ? (
          models.map((model) => (
            <div key={model.id} className="card">
              <div className="flex items-start justify-between mb-4">
                <Brain className="w-8 h-8 text-primary-600" />
                <span className="px-2 py-1 text-xs bg-primary-100 text-primary-700 rounded">
                  {model.status}
                </span>
              </div>
              <h3 className="font-semibold text-lg mb-2">{model.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{model.description}</p>
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>{model.model_type}</span>
                <span>{model.algorithm}</span>
              </div>
              <button className="btn btn-primary w-full flex items-center justify-center space-x-2">
                <Play className="w-4 h-4" />
                <span>Train Model</span>
              </button>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <Brain className="w-16 h-16 mx-auto text-gray-400 mb-4" />
            <p className="text-gray-500">No models yet. Create your first model!</p>
          </div>
        )}
      </div>
    </div>
  )
}

