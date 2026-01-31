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
		title: 'Create Subject',
		subtitle: 'Add a new subject to the system',
		fields: [
			{
				name: 'name',
				label: 'Subject Name',
				type: 'text',
				placeholder: 'e.g. Data Structures'
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
			},
			{
				name: 'faculty_id',
				label: 'Faculty',
				type: 'select',
				placeholder: 'Select a faculty',
				options: (data.faculties ?? []).map((f: { id: number; name: string }) => ({
					value: f.id,
					label: f.name
				}))
			}
		],
		cancelHref: '/subject'
	};
</script>

<EntityForm {config} {form} />
