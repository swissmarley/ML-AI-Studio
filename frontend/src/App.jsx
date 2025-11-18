import { Routes, Route, Navigate } from 'react-router-dom'
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
import Login from './pages/Login'
import Register from './pages/Register'
import { useAuth } from './hooks/useAuth'

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth()
  
  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }
  
  return isAuthenticated ? children : <Navigate to="/login" />
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <Layout />
          </ProtectedRoute>
        }
      >
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
