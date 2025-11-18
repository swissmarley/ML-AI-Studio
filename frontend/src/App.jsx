import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './hooks/useAuth'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import DataManagement from './pages/DataManagement'
import ModelBuilder from './pages/ModelBuilder'
import Templates from './pages/Templates'
import AITools from './pages/AITools'
import GenerativeAI from './pages/GenerativeAI'
import Notebooks from './pages/Notebooks'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="data" element={<DataManagement />} />
        <Route path="models" element={<ModelBuilder />} />
        <Route path="templates" element={<Templates />} />
        <Route path="ai-tools" element={<AITools />} />
        <Route path="generative-ai" element={<GenerativeAI />} />
        <Route path="notebooks" element={<Notebooks />} />
      </Route>
    </Routes>
  )
}

function App() {
  return (
    <AuthProvider>
      <Toaster position="top-right" />
      <AppRoutes />
    </AuthProvider>
  )
}

export default App


