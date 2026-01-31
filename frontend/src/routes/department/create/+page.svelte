<script lang="ts">
	import EntityForm from '$lib/component/EntityForm.svelte';
	import type { EntityFormConfig } from '$lib/types/entity-form';
	import type { ActionData } from './$types';

	interface Props {
		form: ActionData;
	}

	let { form }: Props = $props();

	const config: EntityFormConfig = {
		title: 'Create Department',
		subtitle: 'Add a new department to the system',
		fields: [
			{
				name: 'name',
				label: 'Department Name',
				type: 'text',
				placeholder: 'e.g. Computer Science'
			},
			{
				name: 'year',
				label: 'Year',
				type: 'number',
				placeholder: 'e.g. 2024'
			}
		],
		cancelHref: '/department'
	};
</script>

<EntityForm {config} {form} />
