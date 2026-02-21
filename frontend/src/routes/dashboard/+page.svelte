<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import * as Card from "$lib/components/ui/card/index.js";

	let username = '';

	function parseJwt(token: string) {
		try {
			const base64Payload = token.split('.')[1];
			const payload = atob(base64Payload);
			return JSON.parse(payload);
		} catch {
			return null;
		}
	}

	onMount(() => {
		const token = localStorage.getItem('token');
		if (!token) {
			goto('/'); // redirect to root (login/register page) if no token
			return;
		}

		const data = parseJwt(token);
		if (data?.sub) {
			username = data.sub; // set username from token
		}
	});

	const stats = [
		{ name: 'Subjects', count: 12, description: 'Total subjects available in the system' },
		{ name: 'Departments', count: 5, description: 'Total departments in the college' },
		{ name: 'Classrooms', count: 20, description: 'Total classrooms allocated' },
		{ name: 'Users', count: 150, description: 'Total registered users' },
		{ name: 'Faculty', count: 25, description: 'Total faculty members' }
	];
</script>

<div class="mt-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-6">
	{#each stats as stat}
		<Card.Root class="border rounded-xl shadow-md hover:shadow-lg transition-all duration-300">
			<Card.Header>
				<Card.Title class="text-lg font-bold">{stat.name}</Card.Title>
				<Card.Description class="text-gray-500">{stat.description}</Card.Description>
			</Card.Header>

			<Card.Content class="text-3xl font-extrabold mt-4">{stat.count}</Card.Content>

			<Card.Footer>
				<p class="text-sm text-gray-400">Updated just now</p>
			</Card.Footer>
		</Card.Root>
	{/each}
</div>
