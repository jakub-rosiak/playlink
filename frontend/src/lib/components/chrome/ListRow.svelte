<script lang="ts">
	interface Props {
		selected?: boolean;
		header?: boolean;
		disabled?: boolean;
		onclick?: () => void;
		children?: import('svelte').Snippet;
	}

	let {
		selected = false,
		header = false,
		disabled = false,
		onclick,
		children
	}: Props = $props();

	let pulsing = $state(false);

	const interactive = $derived(!header && !disabled && typeof onclick === 'function');

	function handleClick() {
		if (!interactive) return;
		pulsing = true;
		setTimeout(() => (pulsing = false), 180);
		onclick?.();
	}

	function handleKeydown(e: KeyboardEvent) {
		if (!interactive) return;
		if (e.key === 'Enter' || e.key === ' ') {
			e.preventDefault();
			handleClick();
		}
	}
</script>

<!-- svelte-ignore a11y_no_noninteractive_tabindex -->
<div
	class="row"
	class:is-header={header}
	class:is-selected={selected && !header}
	class:is-disabled={disabled && !header}
	class:is-interactive={interactive}
	class:is-pulsing={pulsing}
	role={interactive ? 'button' : 'row'}
	tabindex={interactive ? 0 : undefined}
	aria-disabled={disabled || undefined}
	aria-selected={!header ? selected || undefined : undefined}
	onclick={handleClick}
	onkeydown={handleKeydown}
>
	{#if selected && !header}
		<span class="pip" aria-hidden="true"></span>
	{/if}
	{@render children?.()}
</div>

<style>
	.row {
		position: relative;
		display: grid;
		grid-template-columns: var(--list-cols, 1fr);
		gap: var(--list-gap, 1.25rem);
		align-items: center;
		font-family: var(--font-display);
		text-transform: uppercase;
		letter-spacing: var(--track-loose);
		color: var(--bone);
		font-size: 0.78rem;
		padding: 0.95rem 1rem;
		border-bottom: 1px solid rgba(42, 37, 28, 0.6);
		border-left: 2px solid transparent;
		background: transparent;
		transition:
			background 140ms ease,
			color 140ms ease,
			border-color 140ms ease,
			box-shadow 160ms ease,
			transform 80ms ease,
			opacity 140ms ease;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
		outline: none;
		border-radius: 0;
	}

	.row.is-interactive {
		cursor: pointer;
	}

	.row.is-header {
		color: var(--bone-dim);
		font-size: 0.7rem;
		letter-spacing: var(--track-extra);
		padding: 0.85rem 1rem;
		border-bottom: 1px solid var(--stone-5);
		cursor: default;
	}

	.row.is-disabled {
		opacity: 0.4;
		cursor: not-allowed;
		pointer-events: none;
	}

	.row.is-interactive:hover {
		color: var(--bone-bright);
		border-left: 2px solid var(--gold-base);
		box-shadow: inset 0 0 24px rgba(227, 188, 116, 0.08);
	}

	.row.is-selected {
		color: var(--bone-bright);
		border: 1px solid var(--gold-muted);
		box-shadow: inset 0 0 32px rgba(227, 188, 116, 0.15);
	}

	.row.is-interactive:focus-visible {
		outline: 1px solid var(--gold-lit);
		outline-offset: -1px;
	}

	.row.is-pulsing {
		transform: translateY(1px);
		opacity: 0.85;
	}

	.pip {
		position: absolute;
		left: -2px;
		top: 50%;
		width: 4px;
		height: 4px;
		margin-top: -2px;
		background: var(--gold-lit);
		box-shadow:
			0 0 6px var(--gold-glow),
			0 0 1px rgba(0, 0, 0, 0.85);
	}
</style>
