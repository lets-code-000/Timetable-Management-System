import { redirect, fail, type Actions } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

interface Department {
	id: number;
	name: string;
	year?: number;
}

interface Faculty {
	id: number;
	name: string;
}

interface Timetable {
	id: number;
	department_id: number;
	class_coordinator_id: number;
	academic_year: string;
	college_id?: number;
	created_at?: string;
	updated_at?: string;
	department?: Department;
	class_coordinator?: Faculty;
}

export const load: PageServerLoad = async ({ cookies, fetch }) => {
	const token = cookies.get('token');

	if (!token) {
		throw redirect(302, '/');
	}

	try {
		const response = await fetch(`${PUBLIC_API_BASE_URL}/timetable`, {
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
				timetables: [],
				error: errorData.detail || `Failed to fetch timetables: ${response.statusText}`
			};
		}

		const timetables: Timetable[] = await response.json();

		return {
			timetables,
			error: null
		};
	} catch (error) {
		if (error instanceof Response && error.status === 302) {
			throw error;
		}

		console.error('Error fetching timetables:', error);
		return {
			timetables: [],
			error: error instanceof Error ? error.message : 'Failed to fetch timetables'
		};
	}
};

export const actions: Actions = {
	deleteTimetable: async ({ request, cookies, fetch }) => {
		const data = await request.formData();
		const id = data.get('id') as string;
		const token = cookies.get('token');

		if (!token) return fail(401, { error: 'Not authorized' });
		if (!id) return fail(400, { error: 'Timetable ID missing' });

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/timetable/${id}`, {
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				console.error('Delete failed:', res.statusText);
				throw redirect(303, '/timetable');
			}

			throw redirect(303, '/timetable');
		} catch (err) {
			console.error(err);
			throw redirect(303, '/timetable');
		}
	}
};
