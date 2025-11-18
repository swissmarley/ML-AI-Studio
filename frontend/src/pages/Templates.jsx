import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { FileText, Image, TrendingUp, Users, ShoppingCart } from 'lucide-react'
import toast from 'react-hot-toast'
import api from '../utils/api'

const templates = [
  {
    id: 1,
    name: 'Image Classification',
    description: 'Classify images using ResNet, VGG, or EfficientNet',
    icon: Image,
    category: 'Computer Vision',
  },
  {
    id: 2,
    name: 'Text Classification',
    description: 'Sentiment analysis and text categorization',
    icon: FileText,
    category: 'NLP',
  },
  {
    id: 3,
    name: 'Time Series Forecasting',
    description: 'Predict future values from time series data',
    icon: TrendingUp,
    category: 'Time Series',
  },
  {
    id: 4,
    name: 'Customer Churn Prediction',
    description: 'Predict which customers are likely to churn',
    icon: Users,
    category: 'Business',
  },
  {
    id: 5,
    name: 'Price Prediction',
    description: 'Predict prices for real estate, stocks, etc.',
    icon: ShoppingCart,
    category: 'Regression',
  },
]

export default function Templates() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState({})

  const handleUseTemplate = async (template) => {
    setLoading({ ...loading, [template.id]: true })
    
    try {
      // Create a project from the template
      const projectData = {
        name: `${template.name} Project`,
        description: `Project created from ${template.name} template`,
        project_type: template.category.toLowerCase().replace(' ', '_'),
        tags: [template.category]
      }
      
      const response = await api.post('/projects', projectData)
      toast.success(`Template "${template.name}" applied!`)
      navigate('/models') // Navigate to model builder to continue
    } catch (error) {
      console.error('Error using template:', error)
      let errorMessage = 'Failed to use template'
      
      if (!error.response) {
        errorMessage = 'Network Error: Unable to connect to the server.'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      }
      
      toast.error(errorMessage)
    } finally {
      setLoading({ ...loading, [template.id]: false })
    }
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Templates Library</h1>
      <p className="text-gray-600 mb-8">
        Pre-built project templates to get you started quickly
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template) => {
          const Icon = template.icon
          const isLoading = loading[template.id]
          return (
            <div key={template.id} className="card hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <Icon className="w-10 h-10 text-primary-600" />
                <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                  {template.category}
                </span>
              </div>
              <h3 className="font-semibold text-lg mb-2">{template.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{template.description}</p>
              <button 
                onClick={() => handleUseTemplate(template)}
                disabled={isLoading}
                className="btn btn-primary w-full"
              >
                {isLoading ? 'Creating...' : 'Use Template'}
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}

