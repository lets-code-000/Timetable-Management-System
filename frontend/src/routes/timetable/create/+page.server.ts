import { fail } from '@sveltejs/kit';
import { redirect } from 'sveltekit-flash-message/server';
import type { Actions, PageServerLoad } from './$types';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load: PageServerLoad = async ({ cookies, fetch }) => {
	const token = cookies.get('token');
	if (!token) redirect(302, '/');

	try {
		const [deptRes, facultyRes] = await Promise.all([
			fetch(`${PUBLIC_API_BASE_URL}/department/`, {
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			}),
			fetch(`${PUBLIC_API_BASE_URL}/faculty/`, {
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			})
		]);

		if (deptRes.status === 401 || facultyRes.status === 401) {
			cookies.delete('token', { path: '/' });
			redirect(302, '/');
		}

		const departments = deptRes.ok ? await deptRes.json() : [];
		const faculties = facultyRes.ok ? await facultyRes.json() : [];

		return { departments, faculties };
	} catch {
		return { departments: [], faculties: [] };
	}
};

export const actions: Actions = {
	default: async (event) => {
		const { request, cookies, fetch } = event;
		const token = cookies.get('token');
		if (!token) return fail(401, { error: 'Not authorized' });

		const formData = await request.formData();
		const department_id = formData.get('department_id') as string;
		const class_coordinator_id = formData.get('class_coordinator_id') as string;
		const semester = formData.get('semester') as string;
		const academic_year = formData.get('academic_year') as string;

		const fieldErrors: Record<string, string> = {};
		if (!department_id?.trim()) fieldErrors.department_id = 'Department is required';
		if (!class_coordinator_id?.trim())
			fieldErrors.class_coordinator_id = 'Class coordinator is required';
		if (!semester?.trim()) fieldErrors.semester = 'Semester is required';
		if (!academic_year?.trim()) fieldErrors.academic_year = 'Academic year is required';

		if (Object.keys(fieldErrors).length > 0) {
			return fail(400, {
				fieldErrors,
				values: { department_id, class_coordinator_id, semester, academic_year }
			});
		}

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/timetable/`, {
				method: 'POST',
				headers: {
					Authorization: `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					department_id: Number(department_id),
					class_coordinator_id: Number(class_coordinator_id),
					semester: Number(semester),
					academic_year: academic_year.trim()
				})
			});

			if (!res.ok) {
				if (res.status === 401) {
					cookies.delete('token', { path: '/' });
					redirect(302, '/');
				}
				const errData = await res.json().catch(() => ({ detail: 'Creation failed' }));
				return fail(res.status, {
					error: errData.detail || 'Failed to create timetable',
					values: { department_id, class_coordinator_id, semester, academic_year }
				});
			}
		} catch (err) {
			if (err instanceof Response) throw err;
			return fail(500, {
				error: 'Server error while creating timetable',
				values: { department_id, class_coordinator_id, semester, academic_year }
			});
		}

		redirect(
			303,
			'/timetable',
			{ type: 'success', message: 'Timetable created successfully' },
			event
		);
	}
};
