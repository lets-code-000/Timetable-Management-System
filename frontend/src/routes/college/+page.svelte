<script lang="ts">
	import { Building2, Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	import PageHeader from '$lib/component/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button';
	import ActionMenu from '$lib/component/ActionMenu.svelte';
	import { PUBLIC_API_BASE_URL } from '$env/static/public';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	let colleges = $state(data.colleges || []);
	let toast = $state<{ type: 'success' | 'error'; message: string } | null>(null);

	function showToast(type: 'success' | 'error', message: string) {
		toast = { type, message };
		setTimeout(() => {
			toast = null;
		}, 3000);
	}

	async function handleDelete(id: number) {
		const token = document.cookie
			.split('; ')
			.find(row => row.startsWith('token='))
			?.split('=')[1];

		if (!token) {
			showToast('error', 'Not authorized');
			return;
		}

		// Optimistic update - remove from UI immediately
		const previousColleges = [...colleges];
		colleges = colleges.filter(c => c.id !== id);

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/college/${id}`, {
				method: 'DELETE',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json'
				}
			});

			if (!res.ok) {
				// Revert on error
				colleges = previousColleges;
				const errData = await res.json().catch(() => ({ detail: 'Delete failed' }));
				showToast('error', errData.detail || 'Failed to delete college');
				return;
			}

			showToast('success', 'College deleted successfully');
		} catch (err) {
			// Revert on error
			colleges = previousColleges;
			showToast('error', 'Server error while deleting college');
		}
	}

	function handleEdit(id: number) {
		// Edit functionality will be implemented in next PR
		console.log('Edit college:', id);
	}
</script>

<!-- Toast Notification -->
{#if toast}
	<div class="fixed top-4 right-4 z-50 animate-in fade-in slide-in-from-top-2 duration-300">
		<div class="flex items-center gap-2 rounded-lg px-4 py-3 shadow-lg {toast.type === 'success' ? 'bg-green-600' : 'bg-red-600'} text-white">
			<span class="text-sm font-medium">{toast.message}</span>
			<button onclick={() => toast = null} class="ml-2 hover:opacity-80">✕</button>
		</div>
	</div>
{/if}

<div class="min-h-screen bg-gray-100 p-8">
	<div class="mx-auto max-w-6xl">
		<PageHeader
			title="Colleges"
			subtitle="Manage all Colleges and their details"
			Icon={Building2}
		/>

		<div class="rounded-lg bg-white p-6 shadow-md">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-semibold">All Colleges</h2>
				<Button href="/college/create">
					<Plus class="h-4 w-4" />
					Create
				</Button>
			</div>

			{#if colleges && colleges.length > 0}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									College Name
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Address
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Contact
								</th>
								<th class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500">
									Actions
								</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each colleges as college}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">{college.name}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{college.address || '-'}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{college.contact || '-'}</td>
									<td class="px-6 py-4 text-center">
										<ActionMenu
											onEdit={() => handleEdit(college.id)}
											onDelete={() => handleDelete(college.id)}
										/>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<div class="py-8 text-center text-gray-500">
					<p>No colleges found.</p>
				</div>
			{/if}
		</div>

		{#if data.error}
			<div class="mt-4 rounded-lg bg-red-100 p-4 text-red-700">
				<p class="font-semibold">Error loading colleges:</p>
				<p>{data.error}</p>
			</div>
		{/if}
	</div>
</div>
