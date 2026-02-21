<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Search, Plus, Edit, Trash2, Users } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	let {
		title,
		subtitle,
		data,
		columns,
		createPath = undefined,
		onEdit = undefined,
		onDelete = undefined,
		loading = false
	} = $props<{
		title: string;
		subtitle: string;
		data: any[];
		columns: { key: string; label: string; render?: (item: any) => string }[];
		createPath?: string;
		onEdit?: (item: any) => void;
		onDelete?: (item: any) => void;
		loading?: boolean;
	}>();

	let searchTerm = $state('');
	let filteredData = $derived(() => {
		if (searchTerm) {
			return data.filter(item =>
				Object.values(item).some(value =>
					String(value).toLowerCase().includes(searchTerm.toLowerCase())
				)
			);
		} else {
			return data;
		}
	});
</script>

<div class="space-y-6">
	<!-- Header -->
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div>
			<h1 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
				<Users class="w-6 h-6 text-blue-600" />
				{title}
			</h1>
			<p class="text-gray-600 mt-1">{subtitle}</p>
		</div>
		{#if createPath}
			<Button onclick={() => goto(createPath)} class="bg-blue-600 hover:bg-blue-700">
				<Plus class="w-4 h-4 mr-2" />
				Add New
			</Button>
		{/if}
	</div>

	<!-- Search and Filters -->
	<Card>
		<CardContent class="p-6">
			<div class="flex flex-col sm:flex-row gap-4">
				<div class="relative flex-1">
					<Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
					<input
						bind:value={searchTerm}
						placeholder="Search..."
						class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
̵					/>
				</div>
			</div>
		</CardContent>
	</Card>

	<!-- Data Table -->
	<Card>
		<CardHeader>
			<CardTitle class="flex items-center justify-between">
				<span>Records ({filteredData.length})</span>
			</CardTitle>
		</CardHeader>
		<CardContent>
			{#if loading}
				<div class="flex items-center justify-center py-12">
					<div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
					<span class="ml-2 text-gray-600">Loading...</span>
				</div>
			{:else if filteredData.length === 0}
				<div class="text-center py-12">
					<Users class="w-12 h-12 text-gray-400 mx-auto mb-4" />
					<h3 class="text-lg font-medium text-gray-900 mb-2">No records found</h3>
					<p class="text-gray-600">
						{searchTerm ? 'Try adjusting your search terms.' : 'Get started by adding your first record.'}
					</p>
				</div>
			{:else}
				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b border-gray-200">
								{#each columns as column}
									<th class="text-left py-3 px-4 font-medium text-gray-900">
										{column.label}
									</th>
								{/each}
								{#if onEdit || onDelete}
									<th class="text-left py-3 px-4 font-medium text-gray-900">Actions</th>
								{/if}
							</tr>
						</thead>
						<tbody>
							{#each filteredData as item, index}
								<tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
									{#each columns as column}
										<td class="py-3 px-4 text-gray-700">
											{column.render ? column.render(item) : item[column.key] || '-'}
										</td>
									{/each}
									{#if onEdit || onDelete}
										<td class="py-3 px-4">
											<div class="flex items-center gap-2">
												{#if onEdit}
													<Button
														variant="outline"
														size="sm"
														onclick={() => onEdit(item)}
														class="text-blue-600 border-blue-200 hover:bg-blue-50"
													>
														<Edit class="w-4 h-4" />
													</Button>
												{/if}
												{#if onDelete}
													<Button
														variant="outline"
														size="sm"
														onclick={() => onDelete(item)}
														class="text-red-600 border-red-200 hover:bg-red-50"
													>
														<Trash2 class="w-4 h-4" />
													</Button>
												{/if}
											</div>
										</td>
									{/if}
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</CardContent>
	</Card>
</div>