import { redirect, fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface College {
	id: number;
	name: string;
	address?: string;
	contact?: string;
}

export const load: PageServerLoad = async ({ cookies, fetch }) => {
	const token = cookies.get('token');

	if (!token) {
		throw redirect(302, '/');
	}

	try {
		const response = await fetch(`${PUBLIC_API_BASE_URL}/college/`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${token}`,
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
				colleges: [],
				error: errorData.detail || `Failed to fetch colleges: ${response.statusText}`
			};
		}

		const colleges: College[] = await response.json();

		return {
			colleges,
			error: null
		};
	} catch (error) {
		if (error instanceof Response && error.status === 302) {
			throw error;
		}

		console.error('Error fetching colleges:', error);
		return {
			colleges: [],
			error: error instanceof Error ? error.message : 'Failed to fetch colleges'
		};
	}
};

export const actions: Actions = {
	deleteCollege: async ({ request, cookies, fetch }) => {
		const data = await request.formData();
		const id = data.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'College ID missing' });

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/college/${id}`, {
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
						message: errData.detail || 'Failed to delete college'
					}),
					{ path: '/', maxAge: 5 }
				);
				throw redirect(303, '/college');
			}

			cookies.set(
				'flash',
				JSON.stringify({ type: 'success', message: 'College deleted successfully' }),
				{ path: '/', maxAge: 5 }
			);

			throw redirect(303, '/college');
		} catch (err) {
			if (err instanceof Response) throw err;
			console.error(err);
			cookies.set(
				'flash',
				JSON.stringify({ type: 'error', message: 'Server error while deleting college' }),
				{ path: '/', maxAge: 5 }
			);
			throw redirect(303, '/college');
		}
	}
};
