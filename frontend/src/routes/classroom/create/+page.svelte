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
		title: 'Create Classroom',
		subtitle: 'Add a new classroom to the system',
		fields: [
			{
				name: 'building_name',
				label: 'Building Name',
				type: 'text',
				placeholder: 'e.g. Main Building'
			},
			{
				name: 'room_no',
				label: 'Room Number',
				type: 'text',
				placeholder: 'e.g. 101'
			},
			{
				name: 'capacity',
				label: 'Capacity',
				type: 'number',
				placeholder: 'e.g. 60'
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
		cancelHref: '/classroom'
	};
</script>

<EntityForm {config} {form} />
