<script lang="ts">
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<footer class="hint-bar anim-hints-in" aria-label="Keyboard hints">
	<span class="hint-rule" aria-hidden="true"></span>
	<div class="hint-row">
		{@render children?.()}
	</div>
</footer>

<style>
	.hint-bar {
		position: relative;
		margin-top: 24px;
		padding: 14px 18px 4px;
		display: flex;
		flex-direction: column;
	}

	.hint-rule {
		display: block;
		height: 1px;
		width: 100%;
		background: linear-gradient(
			90deg,
			transparent 0%,
			rgba(194, 157, 89, 0.55) 12%,
			rgba(194, 157, 89, 0.55) 88%,
			transparent 100%
		);
		margin-bottom: 14px;
	}

	.hint-row {
		display: flex;
		flex-wrap: wrap;
		gap: clamp(0.6rem, 1.6vw, 1.6rem);
		align-items: center;
		justify-content: center;
		font-family: var(--font-display);
	}

	/* Touch devices have no keyboard — hide the hint bar entirely. */
	@media (hover: none) and (pointer: coarse) {
		.hint-bar {
			display: none;
		}
	}
</style>
