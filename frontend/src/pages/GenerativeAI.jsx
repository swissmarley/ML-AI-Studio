import { Image, Music, Video } from 'lucide-react'

export default function GenerativeAI() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Generative AI Studio</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card hover:shadow-lg transition-shadow cursor-pointer">
          <Image className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="font-semibold text-lg mb-2">Image Generation</h3>
          <p className="text-sm text-gray-600 mb-4">
            Generate images using Stable Diffusion, DALL-E, or Midjourney
          </p>
          <button className="btn btn-primary w-full">Open Studio</button>
        </div>

        <div className="card hover:shadow-lg transition-shadow cursor-pointer">
          <Music className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="font-semibold text-lg mb-2">Audio Generation</h3>
          <p className="text-sm text-gray-600 mb-4">
            Text-to-speech, music generation, and audio editing
          </p>
          <button className="btn btn-primary w-full">Open Studio</button>
        </div>

        <div className="card hover:shadow-lg transition-shadow cursor-pointer">
          <Video className="w-12 h-12 text-primary-600 mb-4" />
          <h3 className="font-semibold text-lg mb-2">Video Generation</h3>
          <p className="text-sm text-gray-600 mb-4">
            Text-to-video, image-to-video, and video editing
          </p>
          <button className="btn btn-primary w-full">Open Studio</button>
        </div>
      </div>
    </div>
  )
}

