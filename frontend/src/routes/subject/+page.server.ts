import { redirect, fail } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
  const token = cookies.get('token');
  if (!token) throw redirect(302, '/');

  try {
    const res = await fetch(`${PUBLIC_API_BASE_URL}/subject`, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!res.ok) {
      if (res.status === 401) {
        cookies.delete('token', { path: '/' });
        throw redirect(302, '/');
      }
      const errorData = await res.json().catch(() => ({ detail: 'Unknown error' }));
      return { subjects: [], error: errorData.detail || 'Failed to fetch subjects' };
    }

    const subjects = await res.json();
    return { subjects, error: null };
  } catch (err) {
    return { subjects: [], error: err instanceof Error ? err.message : 'Failed to fetch subjects' };
  }
};

export const actions: Actions = {
  deleteSubject: async ({ request, cookies }) => {
    const token = cookies.get('token');
    if (!token) throw redirect(302, '/');

    const formData = await request.formData();
    const id = formData.get('id');

    try {
      const res = await fetch(`${PUBLIC_API_BASE_URL}/subject/${id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!res.ok) {
        const error = await res.json();
        return fail(400, { error: error.detail || 'Failed to delete subject' });
      }

      return { success: true };
    } catch (err) {
      return fail(500, { error: 'Server error while deleting subject' });
    }
  }
};
