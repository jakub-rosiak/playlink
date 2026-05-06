<script lang="ts">
	interface Props {
		variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
		size?: 'sm' | 'md' | 'lg';
		type?: 'button' | 'submit' | 'reset';
		disabled?: boolean;
		loading?: boolean;
		href?: string;
		fullWidth?: boolean;
		onclick?: (e: MouseEvent) => void;
		children?: import('svelte').Snippet;
	}

	let {
		variant = 'secondary',
		size = 'md',
		type = 'button',
		disabled = false,
		loading = false,
		href,
		fullWidth = false,
		onclick,
		children
	}: Props = $props();

	const isDisabled = $derived(disabled || loading);
</script>

{#if href}
	<a
		class="ornate ornate--{variant} ornate--{size}"
		class:full-width={fullWidth}
		class:is-loading={loading}
		class:is-disabled={isDisabled}
		href={isDisabled ? undefined : href}
		role="button"
		aria-disabled={isDisabled || undefined}
		tabindex={isDisabled ? -1 : 0}
		onclick={(e) => {
			if (isDisabled) {
				e.preventDefault();
				return;
			}
			onclick?.(e);
		}}
	>
		<span class="ornate__inner small-caps">
			{#if loading}
				<span class="ornate__loader" aria-hidden="true">
					<span class="dot"></span>
					<span class="dot"></span>
					<span class="dot"></span>
				</span>
			{:else}
				{@render children?.()}
			{/if}
		</span>
	</a>
{:else}
	<button
		{type}
		class="ornate ornate--{variant} ornate--{size}"
		class:full-width={fullWidth}
		class:is-loading={loading}
		disabled={isDisabled}
		{onclick}
	>
		<span class="ornate__inner small-caps">
			{#if loading}
				<span class="ornate__loader" aria-hidden="true">
					<span class="dot"></span>
					<span class="dot"></span>
					<span class="dot"></span>
				</span>
			{:else}
				{@render children?.()}
			{/if}
		</span>
	</button>
{/if}

<style>
	.ornate {
		position: relative;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-family: var(--font-display);
		text-transform: uppercase;
		text-decoration: none;
		letter-spacing: var(--track-loose);
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
		border-radius: 0;
		border: 1px solid var(--stone-6);
		cursor: pointer;
		user-select: none;
		transition:
			box-shadow 140ms ease,
			filter 140ms ease,
			transform 80ms ease,
			color 140ms ease,
			border-color 140ms ease;
		white-space: nowrap;
	}

	.ornate__inner {
		position: relative;
		z-index: 1;
		display: inline-flex;
		align-items: center;
		gap: var(--sp-2);
	}

	.full-width {
		width: 100%;
	}

	/* --- Sizes --- */
	.ornate--sm {
		padding: 0.45rem 0.9rem;
		min-height: 28px;
		font-size: 0.7rem;
	}
	.ornate--md {
		padding: 0.7rem 1.4rem;
		min-height: 36px;
		font-size: 0.78rem;
	}
	.ornate--lg {
		padding: 0.95rem 2rem;
		min-height: 44px;
		font-size: 0.92rem;
	}

	/* --- Primary: gold gradient --- */
	.ornate--primary {
		background: linear-gradient(180deg, var(--gold-lit) 0%, var(--gold-muted) 100%);
		color: var(--stone-0);
		border-color: var(--gold-dark);
		box-shadow:
			inset 0 1px 0 rgba(255, 230, 160, 0.45),
			inset 0 -1px 0 rgba(0, 0, 0, 0.55),
			inset 1px 0 0 rgba(255, 230, 160, 0.18),
			inset -1px 0 0 rgba(0, 0, 0, 0.4),
			0 1px 0 rgba(0, 0, 0, 0.6),
			var(--glow-soft);
		text-shadow: 0 1px 0 rgba(255, 230, 160, 0.35);
	}
	.ornate--primary:hover:not(:disabled):not(.is-disabled) {
		filter: brightness(1.08);
		box-shadow:
			inset 0 1px 0 rgba(255, 230, 160, 0.55),
			inset 0 -1px 0 rgba(0, 0, 0, 0.55),
			inset 1px 0 0 rgba(255, 230, 160, 0.22),
			inset -1px 0 0 rgba(0, 0, 0, 0.4),
			0 1px 0 rgba(0, 0, 0, 0.6),
			var(--glow-strong);
	}

	/* --- Secondary: stone gradient --- */
	.ornate--secondary {
		background: linear-gradient(180deg, var(--stone-4) 0%, var(--stone-2) 100%);
		color: var(--bone);
		border-color: var(--gold-dark);
		box-shadow:
			inset 0 1px 0 rgba(255, 230, 160, 0.12),
			inset 1px 0 0 rgba(227, 188, 116, 0.07),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset -1px 0 0 rgba(0, 0, 0, 0.65),
			0 1px 0 rgba(0, 0, 0, 0.55);
	}
	.ornate--secondary:hover:not(:disabled):not(.is-disabled) {
		filter: brightness(1.08);
		color: var(--bone-bright);
		border-color: var(--gold-muted);
		box-shadow:
			inset 0 1px 0 rgba(255, 230, 160, 0.22),
			inset 1px 0 0 rgba(227, 188, 116, 0.12),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset -1px 0 0 rgba(0, 0, 0, 0.65),
			0 1px 0 rgba(0, 0, 0, 0.55),
			var(--glow-mid);
	}

	/* --- Danger: blood-tinted --- */
	.ornate--danger {
		background: linear-gradient(180deg, var(--blood) 0%, #6a1f1f 100%);
		color: var(--bone-bright);
		border-color: #4a1414;
		box-shadow:
			inset 0 1px 0 rgba(255, 200, 200, 0.18),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset 1px 0 0 rgba(255, 180, 180, 0.08),
			inset -1px 0 0 rgba(0, 0, 0, 0.55),
			0 1px 0 rgba(0, 0, 0, 0.55);
		text-shadow: 0 1px 0 rgba(0, 0, 0, 0.6);
	}
	.ornate--danger:hover:not(:disabled):not(.is-disabled) {
		filter: brightness(1.1);
		color: #ffe8e8;
		box-shadow:
			inset 0 1px 0 rgba(255, 200, 200, 0.28),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset 1px 0 0 rgba(255, 180, 180, 0.12),
			inset -1px 0 0 rgba(0, 0, 0, 0.55),
			0 1px 0 rgba(0, 0, 0, 0.55),
			0 0 22px rgba(211, 88, 88, 0.55);
	}

	/* --- Ghost: transparent --- */
	.ornate--ghost {
		background: transparent;
		color: var(--bone-muted);
		border-color: var(--stone-6);
		box-shadow:
			inset 0 1px 0 rgba(227, 188, 116, 0.05),
			inset 0 -1px 0 rgba(0, 0, 0, 0.5);
	}
	.ornate--ghost:hover:not(:disabled):not(.is-disabled) {
		color: var(--bone-bright);
		border-color: var(--gold-muted);
		box-shadow:
			inset 0 1px 0 rgba(227, 188, 116, 0.12),
			inset 0 -1px 0 rgba(0, 0, 0, 0.5),
			var(--glow-soft);
	}

	/* --- Active / pressed --- */
	.ornate:not(:disabled):not(.is-disabled):active {
		box-shadow: var(--bevel-press);
		transform: translateY(1px);
		filter: brightness(0.96);
	}

	/* --- Disabled --- */
	.ornate:disabled,
	.ornate.is-disabled {
		opacity: 0.35;
		cursor: not-allowed;
		filter: none;
		pointer-events: none;
	}

	/* --- Loading dots --- */
	.ornate.is-loading {
		cursor: progress;
	}

	.ornate__loader {
		display: inline-flex;
		gap: 4px;
		align-items: center;
	}

	.ornate__loader .dot {
		width: 5px;
		height: 5px;
		background: currentColor;
		opacity: 0.4;
		animation: ornatePulse 1s ease-in-out infinite;
	}

	.ornate__loader .dot:nth-child(2) {
		animation-delay: 0.15s;
	}
	.ornate__loader .dot:nth-child(3) {
		animation-delay: 0.3s;
	}

	@keyframes ornatePulse {
		0%,
		100% {
			opacity: 0.3;
			transform: scale(0.85);
		}
		50% {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Keep focus visible for accessibility (no radius). */
	.ornate:focus-visible {
		outline: 1px solid var(--gold-lit);
		outline-offset: 2px;
	}
</style>
