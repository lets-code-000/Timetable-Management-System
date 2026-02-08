<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import * as Card from '$lib/components/ui/card/index.js';
	import { PUBLIC_API_BASE_URL } from '$env/static/public';
	import { invalidateAll } from '$app/navigation';
	import { Pencil, Save, X, ArrowLeft } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	let { data } = $props();

	let isEditing = $state(false);
	let isSaving = $state(false);
	let errorMessage = $state('');
	let successMessage = $state('');

	let editForm = $state({
		username: data.user?.username ?? '',
		email: data.user?.email ?? '',
		phone_number: data.user?.phone_number ?? ''
	});

	function startEditing() {
		editForm = {
			username: data.user?.username ?? '',
			email: data.user?.email ?? '',
			phone_number: data.user?.phone_number ?? ''
		};
		isEditing = true;
		errorMessage = '';
		successMessage = '';
	}

	function cancelEditing() {
		isEditing = false;
		errorMessage = '';
	}

	async function saveChanges() {
		isSaving = true;
		errorMessage = '';
		successMessage = '';

		try {
			const token = document.cookie
				.split('; ')
				.find(row => row.startsWith('token='))
				?.split('=')[1];

			if (!token) {
				errorMessage = 'Not authenticated';
				return;
			}

			const response = await fetch(`${PUBLIC_API_BASE_URL}/user/me`, {
				method: 'PATCH',
				headers: {
					'Authorization': `Bearer ${token}`,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username: editForm.username,
					email: editForm.email,
					phone_number: editForm.phone_number || null
				})
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
				errorMessage = errorData.detail || 'Failed to update profile';
				return;
			}

			successMessage = 'Profile updated successfully';
			isEditing = false;
			await invalidateAll();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Failed to update profile';
		} finally {
			isSaving = false;
		}
	}

	function goBack() {
		goto('/college');
	}
</script>

<div class="max-w-2xl mx-auto">
	<!-- Header with Back Button and Edit Button -->
	<div class="flex items-center justify-between mb-6">
		<div class="flex items-center gap-4">
			<button
				onclick={goBack}
				class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
				title="Go back"
			>
				<ArrowLeft class="w-5 h-5 text-gray-600" />
			</button>
			<h1 class="text-2xl font-bold text-gray-800">My Profile</h1>
		</div>

		{#if data.user && !isEditing}
			<Button onclick={startEditing} size="sm">
				<Pencil class="w-4 h-4 mr-2" />
				Edit
			</Button>
		{/if}
	</div>

	{#if data.error}
		<div class="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded mb-4">
			{data.error}
		</div>
	{/if}

	{#if errorMessage}
		<div class="bg-red-50 border-l-4 border-red-500 text-red-700 px-4 py-3 rounded mb-4">
			{errorMessage}
		</div>
	{/if}

	{#if successMessage}
		<div class="bg-green-50 border-l-4 border-green-500 text-green-700 px-4 py-3 rounded mb-4">
			{successMessage}
		</div>
	{/if}

	{#if data.user}
		<Card.Root class="shadow-sm">
			<Card.Header class="pb-4">
				<!-- User Avatar and Name -->
				<div class="flex items-center gap-4">
					<div class="w-16 h-16 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center text-white text-2xl font-bold shadow-md">
						{data.user.username?.charAt(0).toUpperCase() ?? 'U'}
					</div>
					<div>
						<Card.Title class="text-xl">{data.user.username}</Card.Title>
						<Card.Description class="text-gray-500">{data.user.email}</Card.Description>
					</div>
				</div>
			</Card.Header>
			<Card.Content>
				{#if isEditing}
					<div class="space-y-5">
						<div>
							<label for="username" class="block text-sm font-medium text-gray-700 mb-2">
								Username
							</label>
							<input
								type="text"
								id="username"
								bind:value={editForm.username}
								class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
							/>
						</div>
						<div>
							<label for="email" class="block text-sm font-medium text-gray-700 mb-2">
								Email
							</label>
							<input
								type="email"
								id="email"
								bind:value={editForm.email}
								class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
							/>
						</div>
						<div>
							<label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
								Phone Number
							</label>
							<input
								type="tel"
								id="phone"
								bind:value={editForm.phone_number}
								class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
								placeholder="Enter phone number"
							/>
						</div>

						<!-- Action Buttons -->
						<div class="flex gap-3 pt-4 border-t">
							<Button onclick={saveChanges} disabled={isSaving} class="flex-1">
								<Save class="w-4 h-4 mr-2" />
								{isSaving ? 'Saving...' : 'Save Changes'}
							</Button>
							<Button variant="outline" onclick={cancelEditing} disabled={isSaving}>
								<X class="w-4 h-4 mr-2" />
								Cancel
							</Button>
						</div>
					</div>
				{:else}
					<div class="space-y-1">
						<div class="flex items-center py-3 border-b border-gray-100">
							<span class="text-sm font-medium text-gray-500 w-32">Username</span>
							<span class="text-sm text-gray-900">{data.user.username}</span>
						</div>
						<div class="flex items-center py-3 border-b border-gray-100">
							<span class="text-sm font-medium text-gray-500 w-32">Email</span>
							<span class="text-sm text-gray-900">{data.user.email}</span>
						</div>
						<div class="flex items-center py-3">
							<span class="text-sm font-medium text-gray-500 w-32">Phone</span>
							<span class="text-sm text-gray-900">{data.user.phone_number ?? 'Not provided'}</span>
						</div>
					</div>
				{/if}
			</Card.Content>
		</Card.Root>
	{:else}
		<div class="text-center py-12 text-gray-500">
			<div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gray-100 flex items-center justify-center">
				<X class="w-8 h-8 text-gray-400" />
			</div>
			<p>Unable to load user information.</p>
		</div>
	{/if}
</div>
