import { redirect } from '@sveltejs/kit';
import { loadFlash } from 'sveltekit-flash-message/server';

export const load = loadFlash(async ({ cookies, url }) => {
	const token = cookies.get('token');
	const isLoginPage = url.pathname === '/';

	if (!token && !isLoginPage) {
		throw redirect(302, '/');
	}

	return {
		isAuthenticated: !!token,
		isLoginPage
	};
});
