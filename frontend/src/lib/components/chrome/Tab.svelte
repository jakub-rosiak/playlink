<script lang="ts">
	import { page } from '$app/state';

	interface Props {
		href: string;
		match?: 'exact' | 'prefix';
		label?: string;
		children?: import('svelte').Snippet;
	}

	let { href, match = 'prefix', label, children }: Props = $props();

	const isActive = $derived.by(() => {
		const path = page.url.pathname;
		if (match === 'exact') return path === href;
		return path === href || path.startsWith(href + '/');
	});
</script>

<a
	{href}
	class="tab"
	class:active={isActive}
	aria-current={isActive ? 'page' : undefined}
	data-sveltekit-preload-data="hover"
>
	<span class="tab-text small-caps">
		{#if label}{label}{:else}{@render children?.()}{/if}
	</span>
	{#if isActive}
		<span class="tab-arrow" aria-hidden="true"></span>
	{/if}
</a>

<style>
	.tab {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: 1.1rem 1.6rem 1.3rem;
		color: var(--bone-muted);
		font-family: var(--font-display);
		font-size: 1.05rem;
		letter-spacing: var(--track-extra);
		text-transform: uppercase;
		text-decoration: none;
		transition: color 0.18s ease;
		background: transparent;
	}

	.tab:not(:last-child)::after {
		content: '';
		position: absolute;
		right: 0;
		top: 30%;
		bottom: 30%;
		width: 1px;
		background: linear-gradient(
			180deg,
			transparent 0%,
			rgba(194, 157, 89, 0.35) 50%,
			transparent 100%
		);
	}

	.tab:hover {
		color: var(--gold-lit);
	}

	.tab.active {
		color: var(--bone-bright);
		text-shadow:
			0 0 14px rgba(241, 233, 205, 0.18),
			0 1px 0 rgba(0, 0, 0, 0.75);
	}

	.tab-arrow {
		position: absolute;
		left: 50%;
		bottom: -7px;
		transform: translateX(-50%);
		width: 16px;
		height: 9px;
		background: var(--gold-base);
		clip-path: polygon(0 0, 100% 0, 50% 100%);
		filter: drop-shadow(0 0 6px rgba(227, 188, 116, 0.55));
	}

	.tab-text {
		position: relative;
		z-index: 1;
	}
</style>
