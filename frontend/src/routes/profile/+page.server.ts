import { redirect } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface User {
  id: number;
  username: string;
  email: string;
  phone_number: string | null;
  role_id: number | null;
  college_id: number | null;
}

export const load: PageServerLoad = async ({ cookies, fetch }) => {
  const token = cookies.get('token');

  if (!token) {
    throw redirect(302, '/');
  }

  try {
    const response = await fetch(`${PUBLIC_API_BASE_URL}/user/me`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        cookies.delete('token', { path: '/' });
        throw redirect(302, '/');
      }

      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
      return {
        user: null,
        error: errorData.detail || `Failed to fetch user: ${response.statusText}`
      };
    }

    const user: User = await response.json();

    return {
      user,
      error: null
    };
  } catch (error) {
    if (error instanceof Response) {
      throw error;
    }

    console.error('Error fetching user:', error);
    return {
      user: null,
      error: error instanceof Error ? error.message : 'Failed to fetch user'
    };
  }
};
