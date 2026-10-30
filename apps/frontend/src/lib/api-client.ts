import type { ApiResponse } from '@pdf-chatbot/shared';

const configuredApiUrl = (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api/v1')
  .trim()
  .replace(/\/+$/, '');

// Accept either the backend origin or the full versioned API URL. This keeps
// Vercel environment configuration from accidentally calling /auth/* routes.
export const API_BASE_URL = /\/api\/v1$/i.test(configuredApiUrl)
  ? configuredApiUrl
  : `${configuredApiUrl}/api/v1`;

export async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...options.headers,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const data: ApiResponse<T> = await response.json();
  return data;
}
