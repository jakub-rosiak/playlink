<script lang="ts">
	interface Props {
		title?: string;
		padded?: boolean;
		children?: import('svelte').Snippet;
		actions?: import('svelte').Snippet;
	}

	let { title, padded = true, children, actions }: Props = $props();
</script>

<section class="inner-panel anim-panel-in" class:padded>
	<div class="panel-back" aria-hidden="true">
		<div class="noise-overlay-soft"></div>
	</div>

	{#if title || actions}
		<header class="panel-head">
			{#if title}
				<h2 class="panel-title etched-gold small-caps">{title}</h2>
				<span class="panel-rule"></span>
			{/if}
			{#if actions}
				<div class="panel-actions">{@render actions()}</div>
			{/if}
		</header>
	{/if}

	<div class="panel-body">
		{@render children?.()}
	</div>
</section>

<style>
	.inner-panel {
		position: relative;
		background: linear-gradient(180deg, #0c0a08 0%, #060503 100%);
		border: 1px solid var(--stone-5);
		box-shadow:
			inset 0 1px 0 rgba(227, 188, 116, 0.08),
			inset 0 -1px 0 rgba(0, 0, 0, 0.95),
			inset 1px 0 0 rgba(0, 0, 0, 0.7),
			inset -1px 0 0 rgba(0, 0, 0, 0.7),
			0 18px 50px rgba(0, 0, 0, 0.75);
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.panel-back {
		position: absolute;
		inset: 0;
		pointer-events: none;
	}

	.padded {
		padding: 0;
	}
	.padded .panel-body {
		padding: clamp(20px, 2vw, 32px);
	}
	.padded .panel-head {
		padding: clamp(16px, 1.4vw, 24px) clamp(20px, 2vw, 32px) 0;
	}

	.panel-head {
		position: relative;
		z-index: 2;
		display: flex;
		align-items: baseline;
		gap: 1.25rem;
	}

	.panel-title {
		font-size: var(--fs-h2);
		margin: 0;
		letter-spacing: var(--track-loose);
		color: var(--gold-base);
		flex-shrink: 0;
	}

	.panel-rule {
		flex: 1;
		height: 1px;
		background: var(--hair-gold);
		align-self: center;
		margin-bottom: 0.25rem;
	}

	.panel-actions {
		flex-shrink: 0;
		display: flex;
		gap: 0.75rem;
	}

	.panel-body {
		position: relative;
		z-index: 2;
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}
</style>
