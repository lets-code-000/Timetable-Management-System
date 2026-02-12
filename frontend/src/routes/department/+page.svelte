<script lang="ts">
	import { LayoutDashboard, Plus, Search } from 'lucide-svelte';
	import type { PageData } from './$types';
	import PageHeader from '$lib/component/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button';
	import ActionMenu from '$lib/component/ActionMenu.svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { PUBLIC_API_BASE_URL } from '$env/static/public';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	const departments = $derived(data?.departments || []);
	const searchValue = $derived(data?.search || '');

	let timeout: ReturnType<typeof setTimeout>;

	let toast = $state<{ type: 'success' | 'error'; message: string } | null>(null);

	function showToast(type: 'success' | 'error', message: string) {
		toast = { type, message };
		setTimeout(() => { toast = null; }, 3000);
	}

	function handleSearch(event: Event) {
		const value = (event.target as HTMLInputElement).value;

		clearTimeout(timeout);

		timeout = setTimeout(() => {
			const url = new URL(page.url);

			if (value.trim()) {
				url.searchParams.set('search', value);
			} else {
				url.searchParams.delete('search');
			}

			goto(url.toString(), { keepFocus: true, invalidateAll: true });
		}, 300);
	}

	async function handleDelete(id: number) {
		const token = document.cookie.split('; ').find(row => row.startsWith('token='))?.split('=')[1];
		if (!token) { showToast('error', 'Not authorized'); return; }

		const previous = [...departments];

		try {
			const res = await fetch(`${PUBLIC_API_BASE_URL}/department/${id}`, {
				method: 'DELETE',
				headers: { 
					'Authorization': `Bearer ${token}`, 
					'Content-Type': 'application/json' 
				}
			});

			if (!res.ok) {
				showToast('error', 'Failed to delete department');
				return;
			}

			showToast('success', 'Department deleted successfully');

			goto(page.url.toString(), { invalidateAll: true });

		} catch (err) {
			showToast('error', 'Server error while deleting department');
		}
	}

	function handleEdit(id: number) {
		console.log('Edit department:', id);
	}
</script>

{#if toast}
	<div class="fixed top-4 right-4 z-50">
		<div
			class="flex items-center gap-2 rounded-lg px-4 py-3 shadow-lg
			{toast.type === 'success' ? 'bg-green-600' : 'bg-red-600'} text-white"
		>
			<span class="text-sm font-medium">{toast.message}</span>
			<button onclick={() => toast = null} class="ml-2 hover:opacity-80">✕</button>
		</div>
	</div>
{/if}

<div class="min-h-screen bg-gray-100 p-8">
	<div class="mx-auto max-w-6xl">
		<PageHeader
			title="Departments"
			subtitle="Manage all Departments and their details"
			Icon={LayoutDashboard}
		/>

		<div class="rounded-lg bg-white p-6 shadow-md">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-semibold">Departments</h2>
				<Button href="/department/create">
					<Plus class="h-4 w-4" />
					Create
				</Button>
			</div>

			<div class="mb-4 max-w-sm">
				<div class="relative">
					<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
					<input
						type="text"
						placeholder="Search departments..."
						value={searchValue}
						oninput={handleSearch}
						class="w-full rounded-md border border-gray-300 py-2 pl-9 pr-3 text-sm focus:border-black focus:outline-none"
					/>
				</div>
			</div>

			{#if departments.length > 0}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Department Name
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Year
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Description
								</th>
								<th class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500">
									Actions
								</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each departments as department}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">
										{department.name}
									</td>
									<td class="px-6 py-4 text-sm text-gray-700">
										{department.year}
									</td>
									<td class="px-6 py-4 text-sm text-gray-600">
										{department.description || '-'}
									</td>
									<td class="px-6 py-4 text-center">
										<ActionMenu
											onEdit={() => handleEdit(department.id)}
											onDelete={() => handleDelete(department.id)}
										/>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<div class="py-8 text-center text-gray-500">
					{#if searchValue}
						<p>No such department found for "<strong>{searchValue}</strong>"</p>
					{:else}
						<p>No departments found.</p>
					{/if}
				</div>
			{/if}
		</div>

		{#if data.error}
			<div class="mt-4 rounded-lg bg-red-100 p-4 text-red-700">
				<p class="font-semibold">Error loading departments:</p>
				<p>{data.error}</p>
			</div>
		{/if}
	</div>
</div>
