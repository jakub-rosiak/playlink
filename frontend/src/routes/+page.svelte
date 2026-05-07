<script lang="ts">
	import Crest from '$lib/components/chrome/Crest.svelte';
	import OrnateButton from '$lib/components/chrome/OrnateButton.svelte';
	import { getHintsState } from '$lib/hintsContext.svelte';

	const hintsState = getHintsState();

	$effect(() => {
		hintsState?.set([{ key: 'Enter', label: 'Enter Realm', tone: 'gold' }]);
	});

	$effect(() => {
		function handler(e: KeyboardEvent) {
			if (e.key === 'Enter') {
				window.location.href = '/auth';
			}
		}
		window.addEventListener('keydown', handler);
		return () => window.removeEventListener('keydown', handler);
	});
</script>

<svelte:head><title>PlayLink</title></svelte:head>

<div class="splash">
	<div class="splash-glow" aria-hidden="true"></div>

	<div class="content anim-content-in">
		<div class="rivets" aria-hidden="true">◆ ◆ ◆</div>

		<div class="crest-wrap"><Crest size={104} tone="gold" /></div>

		<span class="hairline" aria-hidden="true"></span>

		<h1 class="title etched-gold" style="animation-delay: 600ms;">PLAYLINK</h1>

		<span class="hairline" aria-hidden="true"></span>

		<p class="subtitle small-caps">Lobbies · Rooms · Kin</p>

		<div class="cta" style="animation-delay: 1000ms;">
			<OrnateButton variant="primary" size="lg" href="/auth">Enter Realm</OrnateButton>
		</div>

		<span class="hairline narrow" aria-hidden="true"></span>

		<footer class="version">v0.1 · Non-Custodial</footer>
	</div>
</div>

<style>
	.splash {
		position: relative;
		min-height: calc(100vh - 200px);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 4rem 1rem;
		text-align: center;
	}

	.splash-glow {
		position: absolute;
		inset: 0;
		background: radial-gradient(
			ellipse at 50% 28%,
			rgba(227, 188, 116, 0.07) 0%,
			transparent 55%
		);
		pointer-events: none;
		z-index: 0;
	}

	.content {
		position: relative;
		z-index: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1.5rem;
		max-width: 720px;
		width: 100%;
	}

	.rivets {
		color: var(--gold-muted);
		letter-spacing: 1.6em;
		font-size: 0.65rem;
		padding-left: 1.6em;
	}

	.crest-wrap {
		filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.7));
	}

	.hairline {
		display: block;
		width: 220px;
		height: 1px;
		background: var(--hair-gold);
	}

	.hairline.narrow {
		width: 80px;
		opacity: 0.5;
	}

	.title {
		font-family: var(--font-display);
		font-size: clamp(3rem, 8vw, 7rem);
		letter-spacing: 0.08em;
		margin: 0.4rem 0;
		text-shadow: 0 1px 0 rgba(0, 0, 0, 0.85);
		animation-fill-mode: both;
	}

	.subtitle {
		color: var(--bone-muted);
		font-family: var(--font-display);
		letter-spacing: var(--track-extra);
		font-size: 0.85rem;
		margin: 0;
	}

	.cta {
		margin-top: 1.5rem;
	}

	.version {
		margin-top: 2rem;
		font-family: var(--font-mono);
		font-size: 0.62rem;
		color: var(--bone-faint);
		letter-spacing: var(--track-loose);
	}
</style>
