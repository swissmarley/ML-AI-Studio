import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useDropzone } from 'react-dropzone'
import api from '../utils/api'
import toast from 'react-hot-toast'
import { Upload, File, Trash2, Eye } from 'lucide-react'

export default function DataManagement() {
  const [uploading, setUploading] = useState(false)
  const queryClient = useQueryClient()

  const { data: datasets, isLoading } = useQuery({
    queryKey: ['datasets'],
    queryFn: () => api.get('/datasets').then((res) => res.data),
    onError: (error) => {
      console.error('Error fetching datasets:', error)
      if (!error.response) {
        toast.error('Network Error: Unable to connect to the server.')
      }
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id) => api.delete(`/datasets/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries(['datasets'])
      toast.success('Dataset deleted')
    },
  })

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return

    setUploading(true)
    const file = acceptedFiles[0]

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('name', file.name)

      const response = await api.post('/datasets/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      queryClient.invalidateQueries(['datasets'])
      toast.success('Dataset uploaded successfully!')
    } catch (error) {
      console.error('Upload error:', error)
      let errorMessage = 'Upload failed'
      
      if (!error.response) {
        errorMessage = 'Network Error: Unable to connect to the server. Please ensure the backend is running.'
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message
      } else if (error.message) {
        errorMessage = error.message
      }
      
      toast.error(errorMessage)
    } finally {
      setUploading(false)
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/json': ['.json'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/parquet': ['.parquet'],
    },
    maxSize: 100 * 1024 * 1024, // 100MB
  })

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Data Management</h1>
      </div>

      {/* Upload area */}
      <div className="card mb-8">
        <h2 className="text-xl font-semibold mb-4">Upload Dataset</h2>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-500 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
          {isDragActive ? (
            <p className="text-primary-600">Drop the file here...</p>
          ) : (
            <div>
              <p className="text-gray-600 mb-2">
                Drag and drop a file here, or click to select
              </p>
              <p className="text-sm text-gray-500">
                Supports: CSV, JSON, Excel, Parquet (Max 100MB)
              </p>
            </div>
          )}
          {uploading && (
            <p className="mt-4 text-primary-600">Uploading...</p>
          )}
        </div>
      </div>

      {/* Datasets list */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Your Datasets</h2>
        {isLoading ? (
          <p className="text-gray-500">Loading...</p>
        ) : datasets && datasets.length > 0 ? (
          <div className="space-y-4">
            {datasets.map((dataset) => (
              <div
                key={dataset.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50"
              >
                <div className="flex items-center space-x-4">
                  <File className="w-8 h-8 text-primary-600" />
                  <div>
                    <h3 className="font-medium">{dataset.name}</h3>
                    <p className="text-sm text-gray-500">
                      {dataset.file_format.toUpperCase()} • {formatFileSize(dataset.file_size)}
                      {dataset.row_count && ` • ${dataset.row_count.toLocaleString()} rows`}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <button className="p-2 text-gray-600 hover:text-primary-600 hover:bg-gray-100 rounded">
                    <Eye className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => deleteMutation.mutate(dataset.id)}
                    className="p-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No datasets yet. Upload your first dataset!</p>
        )}
      </div>
    </div>
  )
}

