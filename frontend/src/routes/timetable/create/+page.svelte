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
		title: 'Create Timetable',
		subtitle: 'Add a new timetable for a department',
		fields: [
			{
				name: 'department_id',
				label: 'Department',
				type: 'select',
				placeholder: 'Select a department',
				options: (data.departments ?? []).map((d: { id: number; name: string; year: number }) => ({
					value: d.id,
					label: `${d.name} (Year ${d.year})`
				}))
			},
			{
				name: 'class_coordinator_id',
				label: 'Class Coordinator',
				type: 'select',
				placeholder: 'Select a class coordinator',
				options: (data.faculties ?? []).map((f: { id: number; name: string }) => ({
					value: f.id,
					label: f.name
				}))
			},
			{
				name: 'semester',
				label: 'Semester',
				type: 'select',
				placeholder: 'Select a semester',
				options: Array.from({ length: 8 }, (_, i) => ({
					value: i + 1,
					label: `Semester ${i + 1}`
				}))
			},
			{
				name: 'academic_year',
				label: 'Academic Year',
				type: 'text',
				placeholder: 'e.g. 2024-25'
			}
		],
		cancelHref: '/timetable'
	};
</script>

<EntityForm {config} {form} />
