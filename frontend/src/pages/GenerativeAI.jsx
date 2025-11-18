import { useState } from 'react'
import { Image, Music, Video } from 'lucide-react'
import toast from 'react-hot-toast'

export default function GenerativeAI() {
  const [loading, setLoading] = useState({})

  const handleOpenStudio = (type) => {
    setLoading({ ...loading, [type]: true })
    
    // Simulate opening studio (in a real app, this would navigate or open a modal)
    setTimeout(() => {
      toast.success(`${type} Studio is coming soon!`)
      setLoading({ ...loading, [type]: false })
    }, 500)
  }

  const studios = [
    {
      id: 'image',
      name: 'Image Generation',
      description: 'Generate images using Stable Diffusion, DALL-E, or Midjourney',
      icon: Image,
    },
    {
      id: 'audio',
      name: 'Audio Generation',
      description: 'Text-to-speech, music generation, and audio editing',
      icon: Music,
    },
    {
      id: 'video',
      name: 'Video Generation',
      description: 'Text-to-video, image-to-video, and video editing',
      icon: Video,
    },
  ]

  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Generative AI Studio</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {studios.map((studio) => {
          const Icon = studio.icon
          const isLoading = loading[studio.id]
          return (
            <div key={studio.id} className="card hover:shadow-lg transition-shadow">
              <Icon className="w-12 h-12 text-primary-600 mb-4" />
              <h3 className="font-semibold text-lg mb-2">{studio.name}</h3>
              <p className="text-sm text-gray-600 mb-4">{studio.description}</p>
              <button 
                onClick={() => handleOpenStudio(studio.id)}
                disabled={isLoading}
                className="btn btn-primary w-full"
              >
                {isLoading ? 'Opening...' : 'Open Studio'}
              </button>
            </div>
          )
        })}
      </div>
    </div>
  )
}

