import api from '@/utils/api'
import type { UserCreate, UserResponse, Token } from '@/types/auth'

export const authApi = {
  async register(userData: UserCreate): Promise<UserResponse> {
    const response = await api.post<UserResponse>('/auth/register', userData)
    return response.data
  },

  async login(username: string, password: string): Promise<Token> {
    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)
    
    const response = await api.post<Token>(
      '/auth/login',
      params.toString(),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    return response.data
  },

  async refresh(refreshToken: string): Promise<Token> {
    const response = await api.post<Token>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },

  async getUsers(): Promise<UserResponse[]> {
    const response = await api.get<UserResponse[]>('/auth/users')
    return response.data
  },
}
