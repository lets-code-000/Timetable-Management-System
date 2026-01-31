import { fail } from '@sveltejs/kit';
import { redirect } from 'sveltekit-flash-message/server';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
	const token = cookies.get('token');
	if (!token) redirect(302, '/');

	try {
		const res = await fetch('http://localhost:8000/department/', {
			headers: {
				Authorization: `Bearer ${token}`,
				'Content-Type': 'application/json'
			}
		});

		if (!res.ok) {
			if (res.status === 401) {
				cookies.delete('token', { path: '/' });
				redirect(302, '/');
			}
			return { departments: [] };
		}

		const departments = await res.json();
		return { departments };
	} catch {
		return { departments: [] };
	}
};

export const actions: Actions = {
	default: async (event) => {
		const { request, cookies, fetch } = event;
		const token = cookies.get('token');
		if (!token) return fail(401, { error: 'Not authorized' });

		const formData = await request.formData();
		const building_name = formData.get('building_name') as string;
		const room_no = formData.get('room_no') as string;
		const capacity = formData.get('capacity') as string;
		const department_id = formData.get('department_id') as string;

		const fieldErrors: Record<string, string> = {};
		if (!building_name?.trim()) fieldErrors.building_name = 'Building name is required';
		if (!room_no?.trim()) fieldErrors.room_no = 'Room number is required';
		if (!capacity?.trim()) fieldErrors.capacity = 'Capacity is required';
		else if (isNaN(Number(capacity))) fieldErrors.capacity = 'Capacity must be a number';
		if (!department_id?.trim()) fieldErrors.department_id = 'Department is required';

		if (Object.keys(fieldErrors).length > 0) {
			return fail(400, { fieldErrors, values: { building_name, room_no, capacity, department_id } });
		}

		try {
			const res = await fetch('http://localhost:8000/classroom/', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					building_name: building_name.trim(),
					room_no: room_no.trim(),
					capacity: Number(capacity),
					department_id: Number(department_id)
				})
			});

			if (!res.ok) {
				if (res.status === 401) {
					cookies.delete('token', { path: '/' });
					redirect(302, '/');
				}
				const errData = await res.json().catch(() => ({ detail: 'Creation failed' }));
				return fail(res.status, {
					error: errData.detail || 'Failed to create classroom',
					values: { building_name, room_no, capacity, department_id }
				});
			}
		} catch (err) {
			if (err instanceof Response) throw err;
			return fail(500, {
				error: 'Server error while creating classroom',
				values: { building_name, room_no, capacity, department_id }
			});
		}

		redirect(
			303,
			'/classroom',
			{ type: 'success', message: 'Classroom created successfully' },
			event
		);
	}
};
