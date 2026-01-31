<script lang="ts">
	import { Building2, Trash2, Plus } from 'lucide-svelte';
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

			{#if data.colleges && data.colleges.length > 0}
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
							{#each data.colleges as college}
								<tr class="hover:bg-gray-50">
									<td class="px-6 py-4 text-sm font-medium text-gray-900">{college.name}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{college.address || '-'}</td>
									<td class="px-6 py-4 text-sm text-gray-700">{college.contact || '-'}</td>
									<td class="px-6 py-4 text-center">
										<form method="POST" action="?/deleteCollege" use:enhance>
											<input type="hidden" name="id" value={college.id} />
											<button type="submit" class="text-red-600 hover:text-red-800">
												<Trash2 class="inline-block h-5 w-5" />
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
