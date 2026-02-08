<script lang="ts">
	import { MoreVertical } from 'lucide-svelte';
	import { onMount, onDestroy } from 'svelte';

	interface Props {
		onEdit?: () => void;
		onDelete: () => void;
	}

	let { onEdit, onDelete }: Props = $props();

	let isOpen = $state(false);
	let menuPosition = $state({ top: 0, left: 0 });
	let buttonRef: HTMLButtonElement;
	const menuId = Math.random().toString(36).substr(2, 9);

	function toggleMenu(event: MouseEvent) {
		event.stopPropagation();
		event.preventDefault();

		// Close all other menus first
		window.dispatchEvent(new CustomEvent('closeAllMenus', { detail: { except: menuId } }));

		if (!isOpen && buttonRef) {
			const rect = buttonRef.getBoundingClientRect();
			menuPosition = {
				top: rect.bottom + 4,
				left: rect.right - 120
			};
		}
		isOpen = !isOpen;
	}

	function handleEdit(event: MouseEvent) {
		event.stopPropagation();
		event.preventDefault();
		isOpen = false;
		onEdit?.();
	}

	function handleDelete(event: MouseEvent) {
		event.stopPropagation();
		event.preventDefault();
		isOpen = false;
		onDelete();
	}

	function closeMenu() {
		isOpen = false;
	}

	function handleCloseAllMenus(event: CustomEvent<{ except: string }>) {
		if (event.detail.except !== menuId) {
			isOpen = false;
		}
	}

	function handleClickOutside(event: MouseEvent) {
		if (!isOpen) return;
		const target = event.target as Node;
		if (buttonRef && !buttonRef.contains(target)) {
			isOpen = false;
		}
	}

	onMount(() => {
		window.addEventListener('closeAllMenus', handleCloseAllMenus as EventListener);
	});

	onDestroy(() => {
		window.removeEventListener('closeAllMenus', handleCloseAllMenus as EventListener);
	});
</script>

<svelte:window onclick={handleClickOutside} onscroll={closeMenu} />

<div class="inline-flex items-center justify-center">
	<button
		bind:this={buttonRef}
		type="button"
		class="p-1.5 rounded text-gray-400 hover:bg-gray-100 hover:text-gray-600 transition-colors"
		onclick={toggleMenu}
		title="Actions"
	>
		<MoreVertical class="w-4 h-4" />
	</button>
</div>

{#if isOpen}
	<div
		class="fixed bg-white rounded-md shadow-lg border border-gray-200 py-1"
		style="top: {menuPosition.top}px; left: {menuPosition.left}px; z-index: 9999; min-width: 120px;"
	>
		<button
			type="button"
			class="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
			onclick={handleEdit}
		>
			Edit
		</button>
		<button
			type="button"
			class="flex w-full items-center px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
			onclick={handleDelete}
		>
			Delete
		</button>
	</div>
{/if}
