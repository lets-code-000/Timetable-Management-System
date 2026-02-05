<script lang="ts">
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<div class="doc-container">
	<h1 class="doc-title">{data.title}</h1>

	<div class="doc-content">
		{@html data.content}
	</div>
</div>

<style>
	.doc-container {
		max-width: 900px;
		margin: 0 auto;
		padding: 40px 32px;
		font-family: "Inter", "Segoe UI", Arial, sans-serif;
		color: #1f2937;
	}

	.doc-title {
		font-size: 28px;
		font-weight: 600;
		margin-bottom: 20px;
		border-bottom: 2px solid #e5e7eb;
		padding-bottom: 10px;
	}


	:global(.doc-content p) {
		margin-bottom: 16px;
		line-height: 1.7;
		color: #374151;
	}

	:global(.doc-content h2) {
		font-size: 18px;
		font-weight: 600;
		margin: 28px 0 12px;
		color: #111827;
	}

	:global(.doc-content ul) {
		padding-left: 20px;
		margin-bottom: 20px;
	}

	:global(.doc-content li) {
		margin-bottom: 8px;
		color: #374151;
	}

	:global(.doc-content a) {
		color: #2563eb;
		text-decoration: none;
	}

	:global(.doc-content a:hover) {
		text-decoration: underline;
	}
</style>
