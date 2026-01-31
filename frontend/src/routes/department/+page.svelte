<script lang="ts">
	import { LayoutDashboard, Trash2, Plus } from 'lucide-svelte';
	import type { PageData } from './$types';
	import { enhance } from '$app/forms';
	import PageHeader from '$lib/component/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
</script>

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

			{#if data.departments && data.departments.length > 0}
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
							{#each data.departments as department}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">{department.name}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{department.year}</td>
									<td class="px-6 py-4 text-sm text-gray-600">{department.description || '-'}</td>
									<td class="px-6 py-4 text-center">
										<form method="POST"  action="?/deleteDepartment" use:enhance>
											<input type="hidden" name="id" value={department.id} />
											<button type="submit" class="text-red-600 hover:text-red-800">
												<Trash2 class="w-5 h-5 inline-block" />
											</button>
										</form>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<div class="py-8 text-center text-gray-500">
					<p>No departments found.</p>
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
