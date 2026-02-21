<script lang="ts">
	import DataTable from '$lib/component/DataTable.svelte';
	import type { PageData } from './$types';

	interface Props {
		data: PageData;
	}

	let { data }: Props = $props();

	const columns = [
		{ key: 'id', label: 'ID' },
		{ key: 'username', label: 'Username' },
		{ key: 'email', label: 'Email' },
		{
			key: 'phone_number',
			label: 'Phone',
			render: (item: any) => item.phone_number || '-'
		},
		{
			key: 'role_id',
			label: 'Role ID',
			render: (item: any) => item.role_id || '-'
		},
		{
			key: 'college_id',
			label: 'College ID',
			render: (item: any) => item.college_id || '-'
		}
	];

	function handleEdit(user: any) {
		// TODO: Implement edit functionality
		console.log('Edit user:', user);
	}

	function handleDelete(user: any) {
		// TODO: Implement delete functionality
		console.log('Delete user:', user);
	}
</script>

{#if data.error}
	<div class="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg">
		<div class="flex items-center">
			<div class="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center mr-3">
				<span class="text-white text-xs">!</span>
			</div>
			<span>Error: {data.error}</span>
		</div>
	</div>
{:else}
	<DataTable
		title="Users"
		subtitle="Manage system users and their permissions"
		data={data.users || []}
		{columns}
		createPath="/user/create"
		onEdit={handleEdit}
		onDelete={handleDelete}
	/>
{/if}  