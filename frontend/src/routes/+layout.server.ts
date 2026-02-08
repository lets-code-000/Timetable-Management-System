import { redirect } from '@sveltejs/kit';
import { loadFlash } from 'sveltekit-flash-message/server';
import { PUBLIC_API_BASE_URL } from '$env/static/public';

export const load = loadFlash(async ({ cookies, url, fetch }) => {
	const token = cookies.get('token');
	const isLoginPage = url.pathname === '/';

	if (!token && !isLoginPage) {
		throw redirect(302, '/');
	}

	let currentUser = null;

	if (token) {
		try {
			const response = await fetch(`${PUBLIC_API_BASE_URL}/user/me`, {
				method: 'GET',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				currentUser = await response.json();
			} else if (response.status === 401) {
				cookies.delete('token', { path: '/' });
				throw redirect(302, '/');
			}
		} catch (error) {
			if (error instanceof Response) {
				throw error;
			}
			console.error('Error fetching current user:', error);
		}
	}

	return {
		isAuthenticated: !!token,
		isLoginPage,
		currentUser
	};
});
