<script lang="ts">
	import EntityForm from '$lib/component/EntityForm.svelte';
	import type { EntityFormConfig } from '$lib/types/entity-form';
	import type { ActionData, PageData } from './$types';

	interface Props {
		form: ActionData;
		data: PageData;
	}

	let { form, data }: Props = $props();

	const config: EntityFormConfig = {
		title: 'Create Faculty',
		subtitle: 'Add a new faculty member to the system',
		fields: [
			{
				name: 'name',
				label: 'Faculty Name',
				type: 'text',
				placeholder: 'e.g. Dr. John Smith'
			},
			{
				name: 'department_id',
				label: 'Department',
				type: 'select',
				placeholder: 'Select a department',
				options: (data.departments ?? []).map((d: { id: number; name: string; year: number }) => ({
					value: d.id,
					label: `${d.name} (${d.year})`
				}))
			}
		],
		cancelHref: '/faculty'
	};
</script>

<EntityForm {config} {form} />
