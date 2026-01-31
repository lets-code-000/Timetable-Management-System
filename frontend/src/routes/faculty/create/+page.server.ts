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
		const name = formData.get('name') as string;
		const department_id = formData.get('department_id') as string;

		const fieldErrors: Record<string, string> = {};
		if (!name?.trim()) fieldErrors.name = 'Name is required';
		if (!department_id?.trim()) fieldErrors.department_id = 'Department is required';

		if (Object.keys(fieldErrors).length > 0) {
			return fail(400, { fieldErrors, values: { name, department_id } });
		}

		try {
			const res = await fetch('http://localhost:8000/faculty/', {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					name: name.trim(),
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
					error: errData.detail || 'Failed to create faculty',
					values: { name, department_id }
				});
			}
		} catch (err) {
			if (err instanceof Response) throw err;
			return fail(500, {
				error: 'Server error while creating faculty',
				values: { name, department_id }
			});
		}

		redirect(
			303,
			'/faculty',
			{ type: 'success', message: 'Faculty created successfully' },
			event
		);
	}
};
