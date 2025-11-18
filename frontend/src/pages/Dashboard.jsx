import { useQuery } from '@tanstack/react-query'
import api from '../utils/api'
import { Database, Brain, FileText, TrendingUp } from 'lucide-react'

export default function Dashboard() {
  const { data: projects } = useQuery({
    queryKey: ['projects'],
    queryFn: () => api.get('/projects').then((res) => res.data),
  })

  const { data: datasets } = useQuery({
    queryKey: ['datasets'],
    queryFn: () => api.get('/datasets').then((res) => res.data),
  })

  const { data: models } = useQuery({
    queryKey: ['models'],
    queryFn: () => api.get('/models').then((res) => res.data),
  })

  const stats = [
    {
      name: 'Projects',
      value: projects?.length || 0,
      icon: FileText,
      color: 'bg-blue-500',
    },
    {
      name: 'Datasets',
      value: datasets?.length || 0,
      icon: Database,
      color: 'bg-green-500',
    },
    {
      name: 'Models',
      value: models?.length || 0,
      icon: Brain,
      color: 'bg-purple-500',
    },
    {
      name: 'Active Experiments',
      value: 0,
      icon: TrendingUp,
      color: 'bg-orange-500',
    },
  ]

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <div key={stat.name} className="card">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">{stat.name}</p>
                  <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      {/* Recent projects */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Projects</h2>
        {projects && projects.length > 0 ? (
          <div className="space-y-4">
            {projects.slice(0, 5).map((project) => (
              <div
                key={project.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
              >
                <div>
                  <h3 className="font-medium">{project.name}</h3>
                  <p className="text-sm text-gray-500">{project.project_type}</p>
                </div>
                <span className="px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded-full">
                  {project.status}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No projects yet. Create your first project!</p>
        )}
      </div>
    </div>
  )
}

