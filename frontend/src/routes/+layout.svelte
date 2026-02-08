<script lang="ts">
	import '../app.css';

	import favicon from '$lib/assets/favicon.svg';
	import Sidebar from './component/Sidebar.svelte';
	import { getFlash } from 'sveltekit-flash-message';
	import { page } from '$app/state';

	let { children, data } = $props();
	const flash = getFlash(page);
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

{#if $flash}
	<div class="fixed top-4 right-4 z-50">
		<div
			class="flex items-center gap-3 rounded-lg px-4 py-3 shadow-lg {$flash.type === 'success'
				? 'bg-green-600 text-white'
				: 'bg-red-600 text-white'}"
		>
			<span class="text-sm font-medium">{$flash.message}</span>
			<button onclick={() => ($flash = undefined)} class="ml-2 text-white/80 hover:text-white">
				✕
			</button>
		</div>
	</div>
{/if}

{#if data.isAuthenticated && !data.isLoginPage}
	<Sidebar currentUser={data.currentUser}>
		{@render children?.()}
	</Sidebar>
{:else}
	{@render children?.()}
{/if}
