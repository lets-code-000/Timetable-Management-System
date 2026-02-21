<script lang="ts">
	import { enhance } from '$app/forms';
	import { Button } from '$lib/components/ui/button';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import type { EntityFormConfig } from '$lib/types/entity-form';
	import { ArrowLeft, Save, X } from 'lucide-svelte';

	interface Props {
		config: EntityFormConfig;
		form: {
			error?: string;
			fieldErrors?: Record<string, string>;
			values?: Record<string, string>;
		} | null;
	}

	let { config, form }: Props = $props();
	let submitting = $state(false);
</script>

<div class="min-h-screen bg-gray-50 p-6">
	<div class="mx-auto max-w-2xl">
		<!-- Back Button -->
		<a
			href={config.cancelHref}
			class="inline-flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors mb-6"
		>
			<ArrowLeft class="h-4 w-4" />
			Back
		</a>

		<Card class="shadow-sm border border-gray-200">
			<CardHeader class="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-gray-100">
				<CardTitle class="text-2xl font-bold text-gray-900 flex items-center gap-2">
					<div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
						<Save class="h-4 w-4 text-white" />
					</div>
					{config.title}
				</CardTitle>
				<CardDescription class="text-gray-600">{config.subtitle}</CardDescription>
			</CardHeader>
			<CardContent class="p-6">
				{#if form?.error}
					<div class="bg-red-50 border border-red-200 text-red-700 p-4 mb-6 rounded-xl flex items-center space-x-2">
						<div class="w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
							<span class="text-white text-xs">!</span>
						</div>
						<span class="text-sm">{form.error}</span>
					</div>
				{/if}

				<form
					method="POST"
					use:enhance={() => {
						submitting = true;
						return async ({ update }) => {
							submitting = false;
							await update();
						};
					}}
				>
					<div class="space-y-6">
						{#each config.fields as field}
							<div>
								<label for={field.name} class="block text-sm font-semibold text-gray-900 mb-2">
									{field.label}
									{#if field.required !== false}
										<span class="text-red-500 ml-1">*</span>
									{/if}
								</label>

								{#if field.type === 'select'}
									<select
										id={field.name}
										name={field.name}
										required={field.required !== false}
										class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 bg-white"
									>
										<option value="">{field.placeholder ?? 'Select...'}</option>
										{#each field.options ?? [] as opt}
											<option
												value={opt.value}
												selected={form?.values?.[field.name] === String(opt.value)}
											>
												{opt.label}
											</option>
										{/each}
									</select>
								{:else}
									<input
										id={field.name}
										name={field.name}
										type={field.type}
										placeholder={field.placeholder ?? ''}
										required={field.required !== false}
										value={form?.values?.[field.name] ?? ''}
										class="w-full px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
									/>
								{/if}

								{#if form?.fieldErrors?.[field.name]}
									<p class="mt-2 text-sm text-red-600 flex items-center gap-1">
										<span class="w-4 h-4 bg-red-500 rounded-full flex items-center justify-center">
											<span class="text-white text-xs">!</span>
										</span>
										{form.fieldErrors[field.name]}
									</p>
								{/if}
							</div>
						{/each}
					</div>

					<div class="mt-8 flex gap-3">
						<Button
							type="submit"
							disabled={submitting}
							class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-6 py-3 rounded-xl font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
						>
							{#if submitting}
								<div class="flex items-center gap-2">
									<div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
									Saving...
								</div>
							{:else}
								<Save class="w-4 h-4 mr-2" />
								Save
							{/if}
						</Button>
						<Button
							variant="outline"
							href={config.cancelHref}
							class="px-6 py-3 rounded-xl border-gray-300 text-gray-700 hover:bg-gray-50 font-medium transition-all duration-200"
						>
							<X class="w-4 h-4 mr-2" />
							Cancel
						</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
