<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Snippet } from 'svelte';

	import { BookOpenText, Hotel, UserRoundPen, GraduationCap, BookMarked, CalendarDays, LogOut, Building2, User, ChevronUp } from 'lucide-svelte';

	interface CurrentUser {
		id: number;
		username: string;
		email: string;
		phone_number: string | null;
		role_id: number | null;
		college_id: number | null;
	}

	let { children, currentUser }: { children?: Snippet; currentUser?: CurrentUser | null } = $props();

	let isMenuOpen = $state(false);

	const menuItems = [
		{ name: 'College', path: '/college', icon: Building2 },
		{ name: 'Classroom', path: '../classroom', icon: BookOpenText },
		{ name: 'Departments', path: '../department', icon: Hotel },
		{ name: 'Users', path: '/user', icon: UserRoundPen },
		{ name: 'Faculty', path: '/faculty', icon: GraduationCap},
		{ name: 'Subjects', path: '/subject', icon: BookMarked},
		{ name: 'Timetable', path: '/timetable', icon: CalendarDays }
	];

	function navigate(path: string) {
		goto(path);
	}

	function toggleMenu() {
		isMenuOpen = !isMenuOpen;
	}

	function logout() {
		document.cookie = 'token=; path=/; max-age=0';
		localStorage.removeItem('token');
		goto('/');
	}

	function goToProfile() {
		isMenuOpen = false;
		goto('/profile');
	}

	function handleLogout() {
		isMenuOpen = false;
		logout();
	}

	function handleClickOutside(event: MouseEvent) {
		const target = event.target as HTMLElement;
		if (isMenuOpen && !target.closest('.user-menu-container')) {
			isMenuOpen = false;
		}
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="flex min-h-screen">
	<!-- Sidebar -->
	<aside
		class="flex w-64 flex-col justify-between p-6 text-white"
		style="background: linear-gradient(to bottom, #6A89A7, #c7d9ffff);"
	>
		<!-- Top Section -->
		<div>
			<h1 class="mb-8 text-center text-3xl font-bold text-black">
				Admin Panel
			</h1>

			{#each menuItems as item}
				{@const Icon = item.icon}
				<button
					class="group mb-3 flex w-full items-center gap-4 rounded-lg px-4 py-3 font-medium text-gray-100
                    shadow-md transition-all duration-300 hover:bg-white hover:text-blue-700"
					onclick={() => navigate(item.path)}
				>
					<Icon class="w-5 h-5 text-black group-hover:text-blue-700 transition-colors" />

					<span>{item.name}</span>
				</button>
			{/each}
		</div>

		<!-- Bottom Section - User Menu -->
		<div class="border-t border-gray-300 pt-4 relative user-menu-container">
			<!-- Dropdown Menu (appears above the button) -->
			{#if isMenuOpen}
				<div class="absolute bottom-full left-0 right-0 mb-2 bg-white rounded-lg shadow-lg overflow-hidden border border-gray-200">
					<button
						class="flex w-full items-center gap-3 px-4 py-3 text-gray-700 hover:bg-gray-100 transition-colors"
						onclick={goToProfile}
					>
						<User class="w-4 h-4" />
						<span class="text-sm font-medium">Profile</span>
					</button>
					<div class="border-t border-gray-100"></div>
					<button
						class="flex w-full items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 transition-colors"
						onclick={handleLogout}
					>
						<LogOut class="w-4 h-4" />
						<span class="text-sm font-medium">Logout</span>
					</button>
				</div>
			{/if}

			<!-- User Button -->
			<button
				class="flex w-full items-center justify-between gap-2 rounded-lg bg-white/90 px-4 py-3 font-semibold text-gray-800
					shadow-md transition-all duration-300 hover:bg-white cursor-pointer border border-gray-200"
				onclick={toggleMenu}
			>
				<div class="flex items-center gap-3">
					<div class="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center text-white text-sm font-bold">
						{currentUser?.username?.charAt(0).toUpperCase() ?? 'U'}
					</div>
					<span class="text-sm">{currentUser?.username ?? 'User'}</span>
				</div>
				<ChevronUp class="w-4 h-4 transition-transform {isMenuOpen ? '' : 'rotate-180'}" />
			</button>
		</div>
	</aside>

	<!-- Main content with background -->
	<main
		class="flex-1 p-8"
		style=" background-size: cover; background-position: center; min-height: 100vh;"
	>
		<div class="bg-opacity-80 min-h-full rounded-xl bg-white p-6 shadow-lg">
			{@render children?.()}
		</div>
	</main>
</div>
