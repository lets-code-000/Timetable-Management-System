import { redirect, fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface Department {
	id: number;
	name: string;
	year?: number;
	description?: string;
}

interface Faculty {
	id: number;
	name: string;
	department: Department;
}

export const load: PageServerLoad = async ({ cookies, url, fetch }) => {
	const token = cookies.get('token');

	if (!token) {
		throw redirect(302, '/');
	}

	const search = url.searchParams.get('search') || '';

	const queryParams = new URLSearchParams({
		...(search && { name: search })
	});

	try {
		const response = await fetch(
			`${PUBLIC_API_BASE_URL}/faculty?${queryParams}`,
			{
				method: 'GET',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			}
		);

		if (!response.ok) {
			if (response.status === 401) {
				cookies.delete('token', { path: '/' });
				throw redirect(302, '/');
			}

			const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));

			return {
				faculties: [],
				search,
				error: errorData.detail || 'Failed to fetch faculties'
			};
		}

		const faculties: Faculty[] = await response.json();

		return {
			faculties,
			search,
			error: null
		};

	} catch (error) {
		return {
			faculties: [],
			search,
			error: error instanceof Error ? error.message : 'Failed to fetch faculties'
		};
	}
};


export const actions: Actions = {
	deleteFaculty: async ({ request, cookies, fetch }) => {
		const data = await request.formData();
		const id = data.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'Faculty ID missing' });

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/faculty/${id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				console.error('Delete failed:', res.statusText);
				throw redirect(303, '/faculty');
			}

			throw redirect(303, '/faculty');
		} catch (err) {
			console.error(err);
			throw redirect(303, '/faculty');
		}
	}
};
