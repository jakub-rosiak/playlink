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

	/* All variants: flat stone face + crisp 1px bevel.
	   Primary = active/highlighted (brighter gold border, lighter stone face,
	   matching the D2R Options "Default" button when focused).
	   Secondary = idle stone slab. Danger = blood-tinted slab. Ghost = no fill. */

	/* --- Primary: highlighted stone slab (D2R "Default") --- */
	.ornate--primary {
		background: var(--stone-5);
		color: var(--gold-lit);
		border-color: var(--gold-base);
		box-shadow:
			inset 0 0 0 1px var(--stone-1),
			inset 0 1px 0 rgba(227, 188, 116, 0.18),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset 1px 0 0 rgba(227, 188, 116, 0.08),
			inset -1px 0 0 rgba(0, 0, 0, 0.65);
	}
	.ornate--primary:hover:not(:disabled):not(.is-disabled) {
		color: var(--gold-hot);
		border-color: var(--gold-lit);
	}

	/* --- Secondary: stone slab --- */
	.ornate--secondary {
		background: var(--stone-4);
		color: var(--bone);
		border-color: var(--gold-dark);
		box-shadow:
			inset 0 1px 0 rgba(227, 188, 116, 0.1),
			inset 1px 0 0 rgba(227, 188, 116, 0.05),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset -1px 0 0 rgba(0, 0, 0, 0.65);
	}
	.ornate--secondary:hover:not(:disabled):not(.is-disabled) {
		color: var(--bone-bright);
		border-color: var(--gold-muted);
	}

	/* --- Danger: blood slab --- */
	.ornate--danger {
		background: #3a1010;
		color: var(--bone-bright);
		border-color: #4a1414;
		box-shadow:
			inset 0 1px 0 rgba(255, 200, 200, 0.12),
			inset 0 -1px 0 rgba(0, 0, 0, 0.85),
			inset 1px 0 0 rgba(255, 180, 180, 0.06),
			inset -1px 0 0 rgba(0, 0, 0, 0.55);
	}
	.ornate--danger:hover:not(:disabled):not(.is-disabled) {
		color: #ffd9d9;
		border-color: var(--blood-bright);
	}

	/* --- Ghost: no fill --- */
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
