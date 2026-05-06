<script lang="ts">
	interface Props {
		value: number;
		total?: number;
		tone?: 'good' | 'mid' | 'bad' | 'auto';
		size?: 'sm' | 'md';
		glow?: boolean;
		label?: string;
	}

	let {
		value,
		total = 3,
		tone = 'auto',
		size = 'md',
		glow = true,
		label
	}: Props = $props();

	const lit = $derived(Math.max(0, Math.min(total, Math.floor(value))));

	const resolvedTone = $derived.by(() => {
		if (tone !== 'auto') return tone;
		if (lit >= 3) return 'good';
		if (lit === 2) return 'mid';
		if (lit === 1) return 'bad';
		return 'good';
	});

	let prevLit = $state(0);
	let justLit = $state<number | null>(null);

	$effect(() => {
		const current = lit;
		if (current > prevLit) {
			justLit = current - 1;
			const t = setTimeout(() => (justLit = null), 260);
			prevLit = current;
			return () => clearTimeout(t);
		}
		prevLit = current;
	});
</script>

<div class="pip-meter pip-meter--{size}" aria-label={label ?? `${lit} of ${total}`}>
	<div class="pips" data-tone={resolvedTone}>
		{#each Array(total) as _, i}
			<span
				class="pip"
				class:is-lit={i < lit}
				class:is-glow={glow && i < lit}
				class:is-just-lit={justLit === i}
				aria-hidden="true"
			></span>
		{/each}
	</div>
	{#if label}
		<span class="pip-label">{label}</span>
	{/if}
</div>

<style>
	.pip-meter {
		display: inline-flex;
		flex-direction: column;
		align-items: center;
		gap: 4px;
	}

	.pips {
		display: inline-flex;
		align-items: center;
	}

	.pip-meter--sm .pips {
		gap: 3px;
	}
	.pip-meter--md .pips {
		gap: 4px;
	}

	.pip {
		display: inline-block;
		background: var(--pip-dim);
		border: 1px solid var(--stone-6);
		border-radius: 0;
		box-shadow:
			inset 0 1px 0 rgba(255, 255, 255, 0.04),
			inset 0 -1px 0 rgba(0, 0, 0, 0.6);
		transition:
			transform 180ms ease,
			background 160ms ease,
			box-shadow 160ms ease;
	}

	.pip-meter--sm .pip {
		width: 6px;
		height: 6px;
	}
	.pip-meter--md .pip {
		width: 9px;
		height: 9px;
	}

	/* Lit colors per tone */
	.pips[data-tone='good'] .pip.is-lit {
		color: var(--pip-good);
		background: linear-gradient(
			180deg,
			color-mix(in srgb, var(--pip-good) 75%, white 25%) 0%,
			var(--pip-good) 55%,
			color-mix(in srgb, var(--pip-good) 70%, black 30%) 100%
		);
		border-color: var(--stone-6);
	}
	.pips[data-tone='mid'] .pip.is-lit {
		color: var(--pip-mid);
		background: linear-gradient(
			180deg,
			color-mix(in srgb, var(--pip-mid) 75%, white 25%) 0%,
			var(--pip-mid) 55%,
			color-mix(in srgb, var(--pip-mid) 70%, black 30%) 100%
		);
		border-color: var(--stone-6);
	}
	.pips[data-tone='bad'] .pip.is-lit {
		color: var(--pip-bad);
		background: linear-gradient(
			180deg,
			color-mix(in srgb, var(--pip-bad) 75%, white 25%) 0%,
			var(--pip-bad) 55%,
			color-mix(in srgb, var(--pip-bad) 70%, black 30%) 100%
		);
		border-color: var(--stone-6);
	}

	.pip.is-lit.is-glow {
		filter: drop-shadow(0 0 4px currentColor);
	}

	@keyframes pipPop {
		0% {
			transform: scale(0);
		}
		60% {
			transform: scale(1.2);
		}
		100% {
			transform: scale(1);
		}
	}

	.pip.is-just-lit {
		animation: pipPop 240ms cubic-bezier(0.16, 1, 0.3, 1) both;
	}

	.pip-label {
		font-family: var(--font-mono);
		font-size: var(--fs-tiny);
		color: var(--bone-muted);
		text-transform: uppercase;
		letter-spacing: var(--track-loose);
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}
</style>
