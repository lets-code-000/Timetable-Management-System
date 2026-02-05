import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async () => {
	return {
		title: 'Timetable Management System',
		content: `
			<p>
				A web application for managing and visualizing timetables for educational institutions.
				It enables administrators to create and manage timetables while allowing students
				to view schedules in an interactive format.
			</p>

			<h2>Key Features</h2>
			<ul>
				<li>Automatic clash-free timetable generation</li>
				<li>Faculty availability management</li>
				<li>Room and resource allocation</li>
				<li>Scalable for multiple departments</li>
			</ul>
		`
	};
};
