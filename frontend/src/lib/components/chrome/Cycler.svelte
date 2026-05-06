<script lang="ts" generics="T">
	interface Props {
		values: T[];
		value?: T;
		label?: string;
		format?: (v: T) => string;
		disabled?: boolean;
		onchange?: (v: T) => void;
	}

	let {
		values,
		value = $bindable(),
		label,
		format,
		disabled = false,
		onchange
	}: Props = $props();

	const currentIndex = $derived.by(() => {
		const i = values.indexOf(value as T);
		return i === -1 ? 0 : i;
	});

	const display = $derived.by(() => {
		const v = (value ?? values[0]) as T;
		if (format) return format(v);
		return String(v ?? '');
	});

	let leftPulse = $state(false);
	let rightPulse = $state(false);

	function go(direction: -1 | 1) {
		if (disabled || values.length === 0) return;
		const len = values.length;
		const next = (currentIndex + direction + len) % len;
		value = values[next];
		onchange?.(value as T);
		if (direction === -1) {
			leftPulse = true;
			setTimeout(() => (leftPulse = false), 120);
		} else {
			rightPulse = true;
			setTimeout(() => (rightPulse = false), 120);
		}
	}

	// Initialize value if undefined
	$effect(() => {
		if (value === undefined && values.length > 0) {
			value = values[0];
		}
	});
</script>

<div class="cycler" class:disabled>
	{#if label}
		<span class="cycler-label small-caps">{label}</span>
	{/if}
	<div class="cycler-row">
		<button
			type="button"
			class="chev left"
			class:pulse={leftPulse}
			{disabled}
			aria-label="Previous"
			onclick={() => go(-1)}
		>
			<span aria-hidden="true">&#9668;</span>
		</button>
		<span class="value small-caps">{display}</span>
		<button
			type="button"
			class="chev right"
			class:pulse={rightPulse}
			{disabled}
			aria-label="Next"
			onclick={() => go(1)}
		>
			<span aria-hidden="true">&#9658;</span>
		</button>
	</div>
</div>

<style>
	.cycler {
		display: inline-flex;
		flex-direction: column;
		gap: var(--sp-1);
		font-family: var(--font-display);
	}

	.cycler.disabled {
		opacity: 0.35;
		cursor: not-allowed;
	}

	.cycler-label {
		color: var(--bone-muted);
		font-size: 0.7rem;
		letter-spacing: var(--track-extra);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}

	.cycler-row {
		display: inline-flex;
		align-items: center;
		gap: var(--sp-3);
	}

	.chev {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		width: 26px;
		height: 26px;
		padding: 0;
		background: transparent;
		border: 0;
		border-radius: 0;
		color: var(--gold-base);
		font-size: 0.85rem;
		line-height: 1;
		cursor: pointer;
		transition:
			color 140ms ease,
			filter 140ms ease,
			transform 120ms ease;
	}

	.chev:not(:disabled):hover {
		color: var(--gold-lit);
		filter: drop-shadow(0 0 6px rgba(241, 207, 143, 0.55));
	}

	.chev:not(:disabled):active {
		filter: drop-shadow(0 0 8px rgba(241, 207, 143, 0.7));
	}

	.chev:disabled {
		cursor: not-allowed;
		color: var(--gold-dark);
	}

	.chev.left.pulse {
		transform: translateX(-2px);
	}
	.chev.right.pulse {
		transform: translateX(2px);
	}

	.chev:focus-visible {
		outline: 1px solid var(--gold-lit);
		outline-offset: 2px;
	}

	.value {
		color: var(--bone-bright);
		font-size: 0.95rem;
		font-family: var(--font-display);
		letter-spacing: var(--track-loose);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
		min-width: 6ch;
		text-align: center;
		text-shadow:
			0 0 14px rgba(241, 233, 205, 0.12),
			0 1px 0 rgba(0, 0, 0, 0.7);
	}
</style>
