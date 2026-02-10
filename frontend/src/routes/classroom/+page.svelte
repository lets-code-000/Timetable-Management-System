<script lang="ts">
	import type { PageData } from './$types';
	import { Building2, Plus } from 'lucide-svelte';
	import PageHeader from '$lib/component/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button';
	import ActionMenu from '$lib/component/ActionMenu.svelte';
	import { PUBLIC_API_BASE_URL } from '$env/static/public';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let classrooms = $state(data.classrooms || []);
	let toast = $state<{ type: 'success' | 'error'; message: string } | null>(null);

	function showToast(type: 'success' | 'error', message: string) {
		toast = { type, message };
		setTimeout(() => { toast = null; }, 3000);
	}

	async function handleDelete(id: number) {
		const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
		if (!token) { showToast('error', 'Not authorized'); return; }

		const previous = [...classrooms];
		classrooms = classrooms.filter(c => c.id !== id);

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/classroom/${id}`, {
				method: 'DELETE',
				headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
			});
			if (!res.ok) {
				classrooms = previous;
				const errData = await res.json().catch(() => ({ detail: 'Delete failed' }));
				showToast('error', errData.detail || 'Failed to delete classroom');
				return;
			}
			showToast('success', 'Classroom deleted successfully');
		} catch (err) {
			classrooms = previous;
			showToast('error', 'Server error while deleting classroom');
		}
	}

	function handleEdit(id: number) {
		console.log('Edit classroom:', id);
	}
</script>

{#if toast}
	<div class="fixed top-4 right-4 z-50">
		<div class="flex items-center gap-2 rounded-lg px-4 py-3 shadow-lg {toast.type === 'success' ? 'bg-green-600' : 'bg-red-600'} text-white">
			<span class="text-sm font-medium">{toast.message}</span>
			<button onclick={() => toast = null} class="ml-2 hover:opacity-80">✕</button>
		</div>
	</div>
{/if}

<div class="min-h-screen bg-gray-100 p-8">
	<div class="mx-auto max-w-7xl">
		<PageHeader title="Classrooms" subtitle="Manage all classrooms and their details" Icon={Building2} />

		<div class="rounded-lg bg-white p-6 shadow-md">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-semibold">All Classrooms</h2>
				<Button href="/classroom/create">
					<Plus class="h-4 w-4" />
					Create
				</Button>
			</div>

			{#if classrooms && classrooms.length > 0}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Room No</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Building</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Department</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Year</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">Capacity</th>
								<th class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500">Actions</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each classrooms as classroom}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">{classroom.room_no}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{classroom.building_name}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{classroom.department?.name || 'N/A'}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{classroom.department?.year || 'N/A'}</td>
									<td class="px-6 py-4 text-sm text-gray-700">
										<span class="inline-flex rounded-full bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
											{classroom.capacity}
										</span>
									</td>
									<td class="px-6 py-4 text-center">
										<ActionMenu onEdit={() => handleEdit(classroom.id)} onDelete={() => handleDelete(classroom.id)} />
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<div class="py-12 text-center text-gray-500">
					<p class="mt-4 text-lg font-medium">No classrooms found</p>
				</div>
			{/if}
		</div>

		{#if data.error}
			<div class="mt-4 rounded-lg bg-red-100 p-4 text-red-700">
				<p class="font-semibold">Error loading classrooms:</p>
				<p>{data.error}</p>
			</div>
		{/if}
	</div>
</div>
