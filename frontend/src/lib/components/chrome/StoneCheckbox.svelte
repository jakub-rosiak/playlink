<script lang="ts">
	interface Props {
		checked?: boolean;
		label?: string;
		disabled?: boolean;
		size?: 'sm' | 'md';
		onchange?: (checked: boolean) => void;
	}

	let {
		checked = $bindable(false),
		label,
		disabled = false,
		size = 'md',
		onchange
	}: Props = $props();

	function handleChange(e: Event) {
		const target = e.currentTarget as HTMLInputElement;
		checked = target.checked;
		onchange?.(checked);
	}
</script>

<label class="stone-check size-{size}" class:disabled class:checked>
	<input
		type="checkbox"
		class="sr-only"
		{checked}
		{disabled}
		onchange={handleChange}
	/>
	<span class="box" aria-hidden="true">
		<svg
			class="check-mark"
			viewBox="0 0 24 24"
			xmlns="http://www.w3.org/2000/svg"
			fill="none"
		>
			<path
				d="M4 12.5 L10 18 L20 6"
				stroke="currentColor"
				stroke-width="3.2"
				stroke-linecap="square"
				stroke-linejoin="miter"
			/>
		</svg>
	</span>
	{#if label}
		<span class="label-text small-caps">{label}</span>
	{/if}
</label>

<style>
	.stone-check {
		display: inline-flex;
		align-items: center;
		gap: var(--sp-2);
		cursor: pointer;
		user-select: none;
		font-family: var(--font-display);
		line-height: 1;
	}

	.stone-check.disabled {
		opacity: 0.35;
		cursor: not-allowed;
	}

	.sr-only {
		position: absolute;
		width: 1px;
		height: 1px;
		padding: 0;
		margin: -1px;
		overflow: hidden;
		clip: rect(0, 0, 0, 0);
		white-space: nowrap;
		border: 0;
	}

	.box {
		position: relative;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		flex-shrink: 0;
		background: var(--stone-1);
		border: 1px solid var(--stone-5);
		border-radius: 0;
		box-shadow: var(--bevel-in);
		transition:
			border-color 140ms ease,
			box-shadow 140ms ease,
			background 140ms ease;
	}

	.size-md .box {
		width: 22px;
		height: 22px;
	}
	.size-sm .box {
		width: 16px;
		height: 16px;
	}

	.check-mark {
		width: 75%;
		height: 75%;
		color: var(--gold-base);
		transform: scale(0);
		transform-origin: center;
		transition: transform 140ms cubic-bezier(0.34, 1.56, 0.64, 1);
		pointer-events: none;
	}

	.stone-check.checked .check-mark {
		transform: scale(1);
	}

	.label-text {
		color: var(--bone-muted);
		font-size: 0.78rem;
		letter-spacing: var(--track-loose);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
		transition: color 140ms ease;
	}

	.stone-check.checked .label-text {
		color: var(--bone-bright);
	}

	.stone-check:not(.disabled):hover .box {
		border-color: var(--gold-muted);
	}

	.stone-check:not(.disabled):hover .label-text {
		color: var(--bone);
	}

	.sr-only:focus-visible + .box {
		outline: 1px solid var(--gold-lit);
		outline-offset: 2px;
	}
</style>
