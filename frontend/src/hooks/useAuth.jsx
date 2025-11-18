import { useState, createContext, useContext } from 'react'

const AuthContext = createContext()

// Authentication disabled - app works without login
export function AuthProvider({ children }) {
  // Always authenticated with a default user
  const [user] = useState({
    id: 1,
    username: 'user',
    email: 'user@example.com',
    full_name: 'User'
  })
  const [isAuthenticated] = useState(true)
  const [loading] = useState(false)

  const login = async () => {
    // No-op - authentication disabled
    return { access_token: 'dummy-token' }
  }

  const register = async () => {
    // No-op - authentication disabled
    return user
  }

  const logout = () => {
    // No-op - authentication disabled
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}

