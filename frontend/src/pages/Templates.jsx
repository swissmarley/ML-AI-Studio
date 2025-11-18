import { FileText, Image, TrendingUp, Users, ShoppingCart } from 'lucide-react'

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
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Templates Library</h1>
      <p className="text-gray-600 mb-8">
        Pre-built project templates to get you started quickly
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map((template) => {
          const Icon = template.icon
          return (
            <div key={template.id} className="card hover:shadow-lg transition-shadow cursor-pointer">
              <div className="flex items-start justify-between mb-4">
                <Icon className="w-10 h-10 text-primary-600" />
                <span className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                  {template.category}
                </span>
              </div>
              <h3 className="font-semibold text-lg mb-2">{template.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{template.description}</p>
              <button className="btn btn-primary w-full">Use Template</button>
            </div>
          )
        })}
      </div>
    </div>
  )
}

