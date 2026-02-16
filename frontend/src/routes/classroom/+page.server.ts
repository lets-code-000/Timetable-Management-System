import { redirect, fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface Department {
	id: number;
	name: string;
	year: number;
}

interface Classroom {
	id: number;
	building_name: string;
	room_no: string;
	capacity: number;
	department: Department;
}

export const load: PageServerLoad = async ({ cookies, url, fetch }) => {
	const token = cookies.get('token');
	if (!token) throw redirect(302, '/');

	const search = url.searchParams.get('search') || '';

	const queryParams = new URLSearchParams({
		...(search && { search_text: search })
	});

	try {
		const response = await fetch(
			`${PUBLIC_API_BASE_URL}/classroom/?${queryParams}`,
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
				classrooms: [],
				search,
				error: errorData.detail || 'Failed to fetch classrooms'
			};
		}

		const classrooms: Classroom[] = await response.json();

		return {
			classrooms,
			search,
			error: null
		};

	} catch (error) {
		return {
			classrooms: [],
			search,
			error: error instanceof Error ? error.message : 'Failed to fetch classrooms'
		};
	}
};


export const actions: Actions = {
	deleteClassroom: async ({ request, cookies, fetch }) => {
		const form = await request.formData();
		const id = form.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'Missing classroom ID' });

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/classroom/${id}`, {
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
						message: errData.detail || 'Failed to delete classroom ❌'
					}),
					{ path: '/', maxAge: 5 }
				);
				throw redirect(303, '/classroom');
			}

			cookies.set(
				'flash',
				JSON.stringify({
					type: 'success',
					message: 'Classroom deleted successfully ✅'
				}),
				{ path: '/', maxAge: 5 }
			);
			throw redirect(303, '/classroom');
		} catch (err) {
			console.error(err);
			cookies.set(
				'flash',
				JSON.stringify({
					type: 'error',
					message: 'Server error while deleting classroom ⚠️'
				}),
				{ path: '/', maxAge: 5 }
			);
			throw redirect(303, '/classroom');
		}
	}
};
