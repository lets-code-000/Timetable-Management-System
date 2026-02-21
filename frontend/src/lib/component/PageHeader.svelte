<script lang="ts">
	import type { ComponentType } from 'svelte';

	export let title: string;
	export let subtitle: string;
	export let icon: ComponentType | null = null;
	export let actions: any[] = [];
</script>

<div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
	<div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
		<div class="flex items-center gap-3">
			{#if icon}
				<div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
					<svelte:component this={icon} class="h-5 w-5 text-white" />
				</div>
			{/if}
			<div>
				<h1 class="text-2xl font-bold text-gray-900">{title}</h1>
				<p class="text-gray-600 mt-1">{subtitle}</p>
			</div>
		</div>

		{#if actions && actions.length > 0}
			<div class="flex items-center gap-3">
				{#each actions as action}
					<button
						class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
						onclick={action.onClick}
					>
						{action.label}
					</button>
				{/each}
			</div>
		{/if}
	</div>
</div>
