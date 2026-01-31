<script lang="ts">
	import EntityForm from '$lib/component/EntityForm.svelte';
	import type { EntityFormConfig } from '$lib/types/entity-form';
	import type { ActionData } from './$types';

	interface Props {
		form: ActionData;
	}

	let { form }: Props = $props();

	const config: EntityFormConfig = {
		title: 'Create College',
		subtitle: 'Add a new college to the system',
		fields: [
			{
				name: 'name',
				label: 'College Name',
				type: 'text',
				placeholder: 'e.g. ABC College of Engineering'
			},
			{
				name: 'address',
				label: 'Address',
				type: 'text',
				placeholder: 'e.g. 123 Main Street, City',
				required: false
			},
			{
				name: 'contact',
				label: 'Contact',
				type: 'text',
				placeholder: 'e.g. +91 9876543210',
				required: false
			}
		],
		cancelHref: '/college'
	};
</script>

<EntityForm {config} {form} />
