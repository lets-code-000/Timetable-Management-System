import { redirect ,fail,type Actions} from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';


interface Department {
  id: number;
  name: string;
  year?: number;
  description?: string;
}

export const load: PageServerLoad = async ({ cookies, fetch }) => {
  // Get token from cookie
  const token = cookies.get('token');
  
  // If no token, redirect to login
  if (!token) {
    throw redirect(302, '/');
  }

  try {
    // Fetch departments from FastAPI backend
		const response = await fetch(`${PUBLIC_API_BASE_URL}/department`, {
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
        departments: [],
        error: errorData.detail || `Failed to fetch departments: ${response.statusText}`
      };
    }

    const departments: Department[] = await response.json();
    
    return {
      departments,
      error: null
    };
  } catch (error) {
    // If it's a redirect, re-throw it
    if (error instanceof Response && error.status === 302) {
      throw error;
    }
    
    console.error('Error fetching departments:', error);
    return {
      departments: [],
      error: error instanceof Error ? error.message : 'Failed to fetch departments'
    };
  }
};


export const actions: Actions = {
	deleteDepartment: async ({ request, cookies, fetch }) => {
		const data = await request.formData();
		const id = data.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'Department ID missing' });

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/department/${id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				const errData = await res.json().catch(() => ({ detail: 'Delete failed' }));
				cookies.set(
					'flash',
					JSON.stringify({
						type: 'error',
						message: errData.detail || 'Failed to delete department ❌'
					}),
					{ path: '/', maxAge: 5 }
				);
				throw redirect(303, '/department');
			}

			// ✅ success flash message
			cookies.set(
				'flash',
				JSON.stringify({ type: 'success', message: 'Department deleted successfully ✅' }),
				{ path: '/', maxAge: 5 }
			);

			throw redirect(303, '/department');
		} catch (err) {
			console.error(err);
			cookies.set(
				'flash',
				JSON.stringify({ type: 'error', message: 'Server error while deleting department ⚠️' }),
				{ path: '/', maxAge: 5 }
			);
			throw redirect(303, '/department');
		}
	}
};
