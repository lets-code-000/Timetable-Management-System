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
	import { ArrowLeft } from 'lucide-svelte';

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

<div class="min-h-screen bg-gray-100 p-8">
	<div class="mx-auto max-w-2xl">
		<a
			href={config.cancelHref}
			class="mb-4 inline-flex items-center gap-1 text-sm text-gray-600 hover:text-gray-900"
		>
			<ArrowLeft class="h-4 w-4" />
			Back
		</a>

		<Card>
			<CardHeader>
				<CardTitle class="text-2xl">{config.title}</CardTitle>
				<CardDescription>{config.subtitle}</CardDescription>
			</CardHeader>
			<CardContent>
				{#if form?.error}
					<div class="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">
						{form.error}
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
					<div class="space-y-4">
						{#each config.fields as field}
							<div>
								<label for={field.name} class="mb-1 block text-sm font-medium text-gray-700">
									{field.label}
									{#if field.required !== false}
										<span class="text-red-500">*</span>
									{/if}
								</label>

								{#if field.type === 'select'}
									<select
										id={field.name}
										name={field.name}
										required={field.required !== false}
										class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
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
										class="w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
									/>
								{/if}

								{#if form?.fieldErrors?.[field.name]}
									<p class="mt-1 text-xs text-red-600">{form.fieldErrors[field.name]}</p>
								{/if}
							</div>
						{/each}
					</div>

					<div class="mt-6 flex gap-3">
						<Button type="submit" disabled={submitting}>
							{submitting ? 'Saving...' : 'Save'}
						</Button>
						<Button variant="outline" href={config.cancelHref}>
							Cancel
						</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
