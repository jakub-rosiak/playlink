<script lang="ts">
	interface Props {
		title: string;
		size?: 'small' | 'normal' | 'large';
		tone?: 'gold' | 'bone' | 'blood';
		children?: import('svelte').Snippet;
	}

	let { title, size = 'normal', tone = 'gold', children }: Props = $props();
</script>

<div class="section-title size-{size} tone-{tone}">
	<h3 class="title small-caps">{title}</h3>
	<span class="rule" aria-hidden="true"></span>
	{#if children}
		<div class="trail">{@render children()}</div>
	{/if}
</div>

<style>
	.section-title {
		display: flex;
		align-items: baseline;
		flex-wrap: wrap;
		gap: 0.5rem 0.9rem;
		margin: 0 0 1rem 0;
	}

	.title {
		font-family: var(--font-display);
		font-weight: normal;
		flex-shrink: 0;
		margin: 0;
	}

	.rule {
		flex: 1;
		min-width: 24px;
		height: 1px;
		background: var(--hair-gold);
		align-self: center;
	}

	.trail {
		font-family: var(--font-mono);
		font-size: var(--fs-tiny);
		letter-spacing: var(--track-loose);
		color: var(--bone-dim);
		text-transform: uppercase;
		flex-shrink: 0;
		max-width: 100%;
	}

	.size-small .title {
		font-size: clamp(0.78rem, 1.1vw, 0.9rem);
		letter-spacing: var(--track-extra);
	}
	.size-normal .title {
		font-size: clamp(1.05rem, 1.6vw, 1.3rem);
		letter-spacing: var(--track-loose);
	}
	.size-large .title {
		font-size: clamp(1.4rem, 2.4vw, 1.85rem);
		letter-spacing: var(--track-loose);
	}

	.tone-gold .title {
		color: var(--gold-base);
		text-shadow:
			0 0 12px rgba(227, 188, 116, 0.22),
			0 1px 0 rgba(0, 0, 0, 0.75);
	}
	.tone-bone .title {
		color: var(--bone-bright);
		text-shadow: 0 1px 0 rgba(0, 0, 0, 0.75);
	}
	.tone-blood .title {
		color: var(--blood-bright);
		text-shadow:
			0 0 12px rgba(181, 54, 54, 0.32),
			0 1px 0 rgba(0, 0, 0, 0.75);
	}
	.tone-blood .rule {
		background: linear-gradient(
			90deg,
			rgba(181, 54, 54, 0.7) 0%,
			rgba(181, 54, 54, 0.4) 60%,
			transparent 100%
		);
	}
</style>
