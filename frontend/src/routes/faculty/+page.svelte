<script lang="ts">
	import { GraduationCap, Trash2, Plus } from 'lucide-svelte';
	import { enhance } from '$app/forms';
	import type { PageData } from './$types';
	import PageHeader from '$lib/component/PageHeader.svelte';
	import { Button } from '$lib/components/ui/button';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();
</script>

<div class="min-h-screen bg-gray-100 p-8">
	<div class="mx-auto max-w-7xl">
		
		<PageHeader
	title="Faculties"
	subtitle="Manage all faculties"
	Icon={GraduationCap}
/>


		<div class="rounded-lg bg-white p-6 shadow-md">
			<div class="mb-4 flex items-center justify-between">
				<h2 class="text-2xl font-semibold">All Faculties</h2>
				<Button href="/faculty/create">
					<Plus class="h-4 w-4" />
					Create
				</Button>
			</div>

			{#if data.faculties && data.faculties.length > 0}
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Name
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Department
								</th>
								<th class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
									Year
								</th>
								<th class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500">
									Actions
								</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each data.faculties as faculty}
								<tr class="hover:bg-gray-50">
									<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
										{faculty.name}
									</td>
									<td class="px-6 py-4 text-sm text-gray-700">
										{faculty.department?.name || 'N/A'}
									</td>
									<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-700">
										{faculty.department?.year || '-'}
									</td>
									<td class="px-6 py-4 text-center">
										<form method="POST" action="?/deleteFaculty" use:enhance>
											<input type="hidden" name="id" value={faculty.id} />
											<button
												type="submit"
												class="text-red-600 hover:text-red-800"
												title="Delete Faculty"
											>
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
				<div class="py-12 text-center text-gray-500">
					<p class="mt-4 text-lg font-medium">No faculties found</p>
					<p class="mt-1 text-sm">There are no faculties in the system yet.</p>
				</div>
			{/if}
		</div>

		{#if data.error}
			<div class="mt-4 rounded-lg bg-red-100 p-4 text-red-700">
				<p class="font-semibold">Error loading faculties:</p>
				<p>{data.error}</p>
			</div>
		{/if}
	</div>
</div>
