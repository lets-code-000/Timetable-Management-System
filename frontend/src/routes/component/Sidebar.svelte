<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Snippet } from 'svelte';

	import { BookOpenText, Hotel, UserRoundPen, GraduationCap, BookMarked, CalendarDays, LogOut, Building2, User, ChevronUp, Menu, X } from 'lucide-svelte';

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
	let isMobileMenuOpen = $state(false);

	const menuItems = [
		{ name: 'Dashboard', path: '/dashboard', icon: CalendarDays },
		{ name: 'College', path: '/college', icon: Building2 },
		{ name: 'Classroom', path: '/classroom', icon: BookOpenText },
		{ name: 'Departments', path: '/department', icon: Hotel },
		{ name: 'Users', path: '/user', icon: UserRoundPen },
		{ name: 'Faculty', path: '/faculty', icon: GraduationCap},
		{ name: 'Subjects', path: '/subject', icon: BookMarked},
		{ name: 'Timetable', path: '/timetable', icon: CalendarDays }
	];

	function navigate(path: string) {
		goto(path);
		isMobileMenuOpen = false; // Close mobile menu on navigation
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
		if (isMobileMenuOpen && !target.closest('.mobile-menu-container')) {
			isMobileMenuOpen = false;
		}
	}

	function toggleMobileMenu() {
		isMobileMenuOpen = !isMobileMenuOpen;
	}
</script>

<svelte:window onclick={handleClickOutside} />

<div class="flex min-h-screen bg-gray-50">
	<!-- Mobile menu overlay -->
	{#if isMobileMenuOpen}
		<div class="fixed inset-0 z-40 lg:hidden">
		<div class="fixed inset-0 bg-black bg-opacity-50" onclick={toggleMobileMenu} onkeydown={(e) => { if (e.key === 'Escape') toggleMobileMenu(); }} role="button" tabindex="0" aria-label="Close mobile menu"></div>
			<div class="fixed left-0 top-0 bottom-0 w-64 bg-white shadow-xl mobile-menu-container">
				<div class="flex items-center justify-between p-4 border-b border-gray-200">
					<h1 class="text-xl font-bold text-gray-900">TimetableIQ</h1>
					<button onclick={toggleMobileMenu} class="p-2 rounded-lg hover:bg-gray-100">
						<X class="w-5 h-5" />
					</button>
				</div>

				<div class="p-4">
					{#each menuItems as item}
						{@const Icon = item.icon}
						<button
							class="group mb-2 flex w-full items-center gap-3 rounded-lg px-3 py-3 font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-all duration-200"
							onclick={() => navigate(item.path)}
						>
							<Icon class="w-5 h-5 text-gray-500 group-hover:text-blue-700 transition-colors" />
							<span>{item.name}</span>
						</button>
					{/each}
				</div>

				<!-- Mobile user menu -->
				<div class="absolute bottom-0 left-0 right-0 border-t border-gray-200 p-4">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							<div class="w-10 h-10 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-white font-semibold">
								{currentUser?.username?.charAt(0).toUpperCase() ?? 'U'}
							</div>
							<div>
								<p class="font-medium text-gray-900">{currentUser?.username ?? 'User'}</p>
								<p class="text-sm text-gray-500">{currentUser?.email ?? ''}</p>
							</div>
						</div>
					</div>
					<div class="mt-4 space-y-2">
						<button
							class="flex w-full items-center gap-3 px-3 py-2 text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
							onclick={goToProfile}
						>
							<User class="w-4 h-4" />
							<span class="text-sm font-medium">Profile</span>
						</button>
						<button
							class="flex w-full items-center gap-3 px-3 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
							onclick={handleLogout}
						>
							<LogOut class="w-4 h-4" />
							<span class="text-sm font-medium">Logout</span>
						</button>
					</div>
				</div>
			</div>
		</div>
	{/if}

	<!-- Desktop Sidebar -->
	<aside class="hidden lg:flex lg:w-64 lg:flex-col bg-white border-r border-gray-200 shadow-sm">
		<!-- Header -->
		<div class="flex items-center justify-center h-16 px-6 border-b border-gray-200">
			<h1 class="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
				TimetableIQ
			</h1>
		</div>

		<!-- Navigation -->
		<div class="flex-1 px-4 py-6">
			<nav class="space-y-2">
				{#each menuItems as item}
					{@const Icon = item.icon}
					<button
						class="group flex w-full items-center gap-3 rounded-lg px-3 py-3 font-medium text-gray-700 hover:bg-blue-50 hover:text-blue-700 transition-all duration-200"
						onclick={() => navigate(item.path)}
					>
						<Icon class="w-5 h-5 text-gray-500 group-hover:text-blue-700 transition-colors" />
						<span>{item.name}</span>
					</button>
				{/each}
			</nav>
		</div>

		<!-- User Menu -->
		<div class="border-t border-gray-200 p-4 user-menu-container relative">
			<!-- Dropdown Menu -->
			{#if isMenuOpen}
				<div class="absolute bottom-full left-4 w-56 mb-2 bg-white rounded-lg shadow-lg border border-gray-200 overflow-hidden z-50">
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
				class="flex w-full items-center justify-between gap-3 rounded-lg bg-gray-50 px-4 py-3 font-medium text-gray-800 hover:bg-gray-100 transition-all duration-200 border border-gray-200 cursor-pointer"
				onclick={toggleMenu}
			>
				<div class="flex items-center gap-3 min-w-0 flex-1">
					<div class="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
						{currentUser?.username?.charAt(0).toUpperCase() ?? 'U'}
					</div>
					<div class="text-left min-w-0 flex-1">
						<p class="text-sm font-medium text-gray-900 truncate">{currentUser?.username ?? 'User'}</p>
						<p class="text-xs text-gray-500 truncate">{currentUser?.email ?? ''}</p>
					</div>
				</div>
				<ChevronUp class="w-4 h-4 transition-transform duration-200 flex-shrink-0 {isMenuOpen ? '' : 'rotate-180'}" />
			</button>
		</div>
	</aside>

	<!-- Mobile Header -->
	<div class="lg:hidden flex items-center justify-between h-16 px-4 bg-white border-b border-gray-200 shadow-sm">
		<button onclick={toggleMobileMenu} class="p-2 rounded-lg hover:bg-gray-100">
			<Menu class="w-5 h-5" />
		</button>
		<h1 class="text-lg font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
			TimetableIQ
		</h1>
		<div class="w-9"></div> <!-- Spacer for centering -->
	</div>

	<!-- Main content -->
	<main class="flex-1 overflow-auto">
		<div class="p-6">
			{@render children?.()}
		</div>
	</main>
</div>
