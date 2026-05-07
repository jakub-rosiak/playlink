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
			const t = setTimeout(() => (justLit = null), 320);
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
				class="orb"
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
		gap: 4px;
	}
	.pip-meter--md .pips {
		gap: 5px;
	}

	/* --- Base orb (unlit / dim) --- */
	.orb {
		display: inline-block;
		border-radius: 50%;
		background: radial-gradient(
			circle at 35% 30%,
			var(--orb-dim-hot) 0%,
			var(--orb-dim-base) 45%,
			var(--orb-dim-shadow) 100%
		);
		box-shadow:
			inset 0 -1px 2px rgba(0, 0, 0, 0.85),
			inset 0 1px 1px rgba(255, 255, 255, 0.06),
			0 1px 1px rgba(0, 0, 0, 0.85);
		transition:
			transform 180ms ease,
			background 180ms ease,
			box-shadow 180ms ease;
	}

	.pip-meter--sm .orb {
		width: 11px;
		height: 11px;
	}
	.pip-meter--md .orb {
		width: 14px;
		height: 14px;
	}

	/* --- Lit orb (per-tone CSS vars resolve via [data-tone]) --- */
	.pips[data-tone='good'] .orb.is-lit {
		background: radial-gradient(
			circle at 35% 28%,
			var(--orb-good-hot) 0%,
			var(--orb-good-base) 45%,
			var(--orb-good-shadow) 100%
		);
	}
	.pips[data-tone='mid'] .orb.is-lit {
		background: radial-gradient(
			circle at 35% 28%,
			var(--orb-mid-hot) 0%,
			var(--orb-mid-base) 45%,
			var(--orb-mid-shadow) 100%
		);
	}
	.pips[data-tone='bad'] .orb.is-lit {
		background: radial-gradient(
			circle at 35% 28%,
			var(--orb-bad-hot) 0%,
			var(--orb-bad-base) 45%,
			var(--orb-bad-shadow) 100%
		);
	}

	.orb.is-lit {
		box-shadow:
			inset 0 -1px 2px rgba(0, 0, 0, 0.55),
			inset 0 1px 1px rgba(255, 255, 255, 0.55),
			0 1px 1px rgba(0, 0, 0, 0.85);
	}

	/* Color-matched outer halo when glowing. */
	.pips[data-tone='good'] .orb.is-lit.is-glow {
		box-shadow:
			inset 0 -1px 2px rgba(0, 0, 0, 0.55),
			inset 0 1px 1px rgba(255, 255, 255, 0.55),
			var(--glow-orb-good),
			0 1px 1px rgba(0, 0, 0, 0.85);
	}
	.pips[data-tone='mid'] .orb.is-lit.is-glow {
		box-shadow:
			inset 0 -1px 2px rgba(0, 0, 0, 0.55),
			inset 0 1px 1px rgba(255, 255, 255, 0.55),
			var(--glow-orb-mid),
			0 1px 1px rgba(0, 0, 0, 0.85);
	}
	.pips[data-tone='bad'] .orb.is-lit.is-glow {
		box-shadow:
			inset 0 -1px 2px rgba(0, 0, 0, 0.55),
			inset 0 1px 1px rgba(255, 255, 255, 0.55),
			var(--glow-orb-bad),
			0 1px 1px rgba(0, 0, 0, 0.85);
	}

	@keyframes orbPop {
		0% {
			transform: scale(0.4);
			filter: brightness(2);
		}
		60% {
			transform: scale(1.25);
			filter: brightness(1.4);
		}
		100% {
			transform: scale(1);
			filter: brightness(1);
		}
	}

	.orb.is-just-lit {
		animation: orbPop 300ms cubic-bezier(0.16, 1, 0.3, 1) both;
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
