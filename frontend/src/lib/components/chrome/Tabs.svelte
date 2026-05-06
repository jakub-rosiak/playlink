<script lang="ts">
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<nav class="tabs" aria-label="Primary">
	<span class="tabs-rule top" aria-hidden="true"></span>
	<div class="tabs-row">
		{@render children?.()}
	</div>
	<span class="tabs-rule bottom" aria-hidden="true"></span>
</nav>

<style>
	.tabs {
		position: relative;
		margin: 0 auto 24px;
		max-width: 1100px;
		width: 100%;
		display: flex;
		flex-direction: column;
	}

	.tabs-row {
		display: grid;
		grid-auto-flow: column;
		grid-auto-columns: 1fr;
		align-items: stretch;
	}

	.tabs-rule {
		display: block;
		height: 1px;
		width: 100%;
		background: linear-gradient(
			90deg,
			transparent 0%,
			rgba(194, 157, 89, 0.6) 18%,
			rgba(194, 157, 89, 0.6) 82%,
			transparent 100%
		);
	}
	.tabs-rule.top {
		margin-bottom: 0;
	}
	.tabs-rule.bottom {
		margin-top: 0;
	}
</style>
