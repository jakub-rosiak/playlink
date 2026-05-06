<script lang="ts">
	interface Props {
		value: number;
		max?: number;
		height?: number;
		ticks?: boolean;
		variant?: 'gold' | 'blood' | 'green';
		label?: string;
	}

	let {
		value,
		max = 100,
		height = 6,
		ticks = false,
		variant = 'gold',
		label
	}: Props = $props();

	const safeMax = $derived(max <= 0 ? 1 : max);
	const clamped = $derived(Math.max(0, Math.min(safeMax, value)));
	const pct = $derived((clamped / safeMax) * 100);
</script>

<div class="progress" style="--pb-height: {height}px;">
	{#if label}
		<div class="progress-label">
			<span class="lbl">{label}</span>
			<span class="num">{Math.round(clamped)}<span class="sep">/</span>{safeMax}</span>
		</div>
	{/if}
	<div
		class="track"
		role="progressbar"
		aria-valuemin={0}
		aria-valuemax={safeMax}
		aria-valuenow={clamped}
		aria-label={label ?? 'progress'}
	>
		<div class="fill fill--{variant}" style="width: {pct}%;"></div>
		{#if ticks}
			<span class="tick" style="left: 25%;" aria-hidden="true"></span>
			<span class="tick" style="left: 50%;" aria-hidden="true"></span>
			<span class="tick" style="left: 75%;" aria-hidden="true"></span>
		{/if}
	</div>
</div>

<style>
	.progress {
		display: flex;
		flex-direction: column;
		gap: 4px;
		width: 100%;
	}

	.progress-label {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		font-family: var(--font-mono);
		font-size: var(--fs-tiny);
		color: var(--bone-muted);
		text-transform: uppercase;
		letter-spacing: var(--track-loose);
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}

	.progress-label .num {
		font-family: var(--font-mono);
		color: var(--bone);
		letter-spacing: 0.04em;
	}

	.progress-label .sep {
		color: var(--bone-dim);
		margin: 0 2px;
	}

	.track {
		position: relative;
		width: 100%;
		height: var(--pb-height, 6px);
		background: var(--stone-2);
		border: 1px solid var(--stone-5);
		border-radius: 0;
		box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.85);
		overflow: hidden;
	}

	.fill {
		position: relative;
		height: 100%;
		width: 0;
		border-radius: 0;
		transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
		box-shadow:
			inset 0 1px 0 rgba(255, 255, 255, 0.18),
			inset 0 -1px 0 rgba(0, 0, 0, 0.45);
	}

	.fill--gold {
		background: linear-gradient(
			180deg,
			var(--gold-lit) 0%,
			var(--gold-muted) 60%,
			var(--gold-dark) 100%
		);
	}

	.fill--blood {
		background: linear-gradient(
			180deg,
			var(--blood-bright) 0%,
			var(--blood) 60%,
			#5a1717 100%
		);
	}

	.fill--green {
		background: linear-gradient(
			180deg,
			color-mix(in srgb, var(--pip-good) 80%, white 20%) 0%,
			var(--pip-good) 60%,
			color-mix(in srgb, var(--pip-good) 70%, black 30%) 100%
		);
	}

	.tick {
		position: absolute;
		top: 0;
		bottom: 0;
		width: 1px;
		background: var(--stone-5);
		opacity: 0.7;
		pointer-events: none;
	}
</style>
