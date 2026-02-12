import { redirect, fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface Department {
	id: number;
	name: string;
	year?: number;
	description?: string;
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
			`${PUBLIC_API_BASE_URL}/department?${queryParams}`,
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

			const errorData = await response
				.json()
				.catch(() => ({ detail: 'Unknown error' }));

			return {
				departments: [],
				search,
				error: errorData.detail || 'Failed to fetch departments'
			};
		}

		const departments: Department[] = await response.json();

		return {
			departments,
			search,
			error: null
		};
	} catch (error) {
		return {
			departments: [],
			search,
			error:
				error instanceof Error
					? error.message
					: 'Failed to fetch departments'
		};
	}
};

export const actions: Actions = {
	deleteDepartment: async ({ request, cookies, fetch }) => {
		const formData = await request.formData();
		const id = formData.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'Department ID missing' });

		try {
			const res = await fetch(
				`${PUBLIC_API_BASE_URL}/department/${id}`,
				{
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${token}`,
						'Content-Type': 'application/json'
					}
				}
			);

			if (!res.ok) {
				const errData = await res
					.json()
					.catch(() => ({ detail: 'Delete failed' }));

				cookies.set(
					'flash',
					JSON.stringify({
						type: 'error',
						message:
							errData.detail ||
							'Failed to delete department ❌'
					}),
					{ path: '/', maxAge: 5 }
				);

				throw redirect(303, '/department');
			}

			cookies.set(
				'flash',
				JSON.stringify({
					type: 'success',
					message: 'Department deleted successfully ✅'
				}),
				{ path: '/', maxAge: 5 }
			);

			throw redirect(303, '/department');
		} catch (err) {
			cookies.set(
				'flash',
				JSON.stringify({
					type: 'error',
					message:
						'Server error while deleting department ⚠️'
				}),
				{ path: '/', maxAge: 5 }
			);

			throw redirect(303, '/department');
		}
	}
};
