import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface User {
  id: number;
  username: string;
  email: string;
}

export const load: PageServerLoad = async ({ cookies, fetch }) => {
  // Get token from cookie
  const token = cookies.get('token');
  
  // If no token, redirect to login
  if (!token) {
    throw redirect(302, '/');
  }

  try {
    // Fetch users from FastAPI backend
    const response = await fetch(`${PUBLIC_API_BASE_URL}/user`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      // If unauthorized, clear cookie and redirect to login
      if (response.status === 401) {
        cookies.delete('token', { path: '/' });
        throw redirect(302, '/');
      }
      
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      return {
        users: [],
        error: errorData.detail || `Failed to fetch users: ${response.statusText}`
      };
    }

    const users: User[] = await response.json();
    
    return {
      users,
      error: null
    };
  } catch (error) {
    // If it's a redirect, re-throw it
    if (error instanceof Response && error.status === 302) {
      throw error;
    }

    console.error('Error fetching users:', error);
    return {
      users: [],
      error: error instanceof Error ? error.message : 'Failed to fetch users'
    };
  }
};
