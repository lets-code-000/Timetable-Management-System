import { fail } from '@sveltejs/kit';
import { redirect } from 'sveltekit-flash-message/server';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ cookies }) => {
	const token = cookies.get('token');
	if (!token) redirect(302, '/');
	return {};
};

export const actions: Actions = {
	default: async (event) => {
		const { request, cookies, fetch } = event;
		const token = cookies.get('token');
		if (!token) return fail(401, { error: 'Not authorized' });

		const formData = await request.formData();
		const name = formData.get('name') as string;
		const year = formData.get('year') as string;

		const fieldErrors: Record<string, string> = {};
		if (!name?.trim()) fieldErrors.name = 'Name is required';
		if (!year?.trim()) fieldErrors.year = 'Year is required';
		else if (isNaN(Number(year))) fieldErrors.year = 'Year must be a number';

		if (Object.keys(fieldErrors).length > 0) {
			return fail(400, { fieldErrors, values: { name, year } });
		}

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/department/`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: name.trim(), year: Number(year) })
			});

			if (!res.ok) {
				if (res.status === 401) {
					cookies.delete('token', { path: '/' });
					redirect(302, '/');
				}
				const errData = await res.json().catch(() => ({ detail: 'Creation failed' }));
				return fail(res.status, {
					error: errData.detail || 'Failed to create department',
					values: { name, year }
				});
			}
		} catch (err) {
			if (err instanceof Response) throw err;
			return fail(500, {
				error: 'Server error while creating department',
				values: { name, year }
			});
		}

		redirect(
			303,
			'/department',
			{ type: 'success', message: 'Department created successfully' },
			event
		);
	}
};
