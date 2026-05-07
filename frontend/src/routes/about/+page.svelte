<script lang="ts">
	import InnerPanel from '$lib/components/chrome/InnerPanel.svelte';
	import SectionTitle from '$lib/components/chrome/SectionTitle.svelte';
	import { getHintsState } from '$lib/hintsContext.svelte';

	const hintsState = getHintsState();

	$effect(() => {
		hintsState?.set([{ key: 'Esc', label: 'Back', tone: 'red' }]);
	});

	const ritual = [
		{
			step: 'I',
			title: 'Forge a Lobby',
			body: 'Pick a game from the catalogue, declare how many can join, give it a name. The lobby goes live the moment you broadcast it.'
		},
		{
			step: 'II',
			title: 'Watch the Hall',
			body: 'Open lobbies stream onto the Game List in real time. Filter by slot count, status, ping. Pick one and the side panel reveals its details.'
		},
		{
			step: 'III',
			title: 'Stand in the Room',
			body: 'Once you join, the lobby gets its own chat. Coordinate the run, swap an IP, settle on a server. When the match is over, leave — or let the timer expire it for you.'
		}
	];
</script>

<svelte:head>
	<title>PlayLink — About</title>
</svelte:head>

<div class="about-page">
	<header class="page-head">
		<SectionTitle title="About Playlink" size="large" tone="gold">
			{#snippet children()}
				<span>A meeting hall for forgotten multiplayer</span>
			{/snippet}
		</SectionTitle>
	</header>

	<div class="column">
		<InnerPanel>
			{#snippet children()}
				<p class="lead">
					Playlink is a place to find people to play <em>old games</em> with — the
					kind of games that no longer have matchmaking, no longer have a healthy
					lobby browser, no longer have anyone waiting on the other side of the
					queue. <em>Quake III. Diablo II. StarCraft. Half-Life. Unreal
						Tournament.</em> The shelf is small and personal on purpose.
				</p>

				<p class="prose">
					You post a lobby. The lobby is a tiny, time-boxed agreement: this game,
					this many players, this long. Everyone connected to the hall sees it
					appear on the Game List the moment you broadcast it. Anyone with the
					right key can walk in. When the run is over, the lobby quietly expires
					and gets out of the way — there is no graveyard of dead servers here.
				</p>

				<SectionTitle title="The Ritual" size="normal" tone="gold" />

				<ol class="ritual" aria-label="How to use Playlink">
					{#each ritual as r (r.step)}
						<li class="step">
							<span class="step-numeral" aria-hidden="true">{r.step}</span>
							<div class="step-body">
								<h3 class="step-title small-caps">{r.title}</h3>
								<p class="step-text">{r.body}</p>
							</div>
						</li>
					{/each}
				</ol>

				<SectionTitle title="On Identity" size="normal" tone="gold" />

				<p class="prose">
					There are no email accounts here. Your identity is a twelve-word
					recovery phrase you generate once and keep. The phrase never leaves
					your machine; the server only ever sees a signature proving you hold
					it. Lose the phrase and you lose the seat — that is the trade.
				</p>

				<p class="prose closing">
					This is a small project. It exists because finding three other people
					who still want to play vanilla Quake on a Tuesday evening shouldn't
					require a Discord raid.
				</p>
			{/snippet}
		</InnerPanel>
	</div>
</div>

<style>
	.about-page {
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		flex: 1;
		padding: 0.5rem 0 4rem;
	}

	.page-head {
		padding: 0 0.5rem;
	}

	.column {
		max-width: 880px;
		width: 100%;
		margin: 0 auto;
	}

	.lead {
		font-family: var(--font-display);
		font-size: clamp(1.05rem, 1.5vw, 1.3rem);
		line-height: 1.55;
		color: var(--bone-bright);
		letter-spacing: var(--track-tight);
		margin: 0 0 1.5rem 0;
	}

	.lead :global(em) {
		color: var(--gold-base);
		font-style: normal;
		text-shadow: 0 0 10px rgba(227, 188, 116, 0.25);
	}

	.prose {
		font-family: var(--font-body);
		font-size: var(--fs-body);
		line-height: 1.75;
		color: var(--bone);
		margin: 0 0 1.5rem 0;
	}

	.prose.closing {
		margin-top: 0.5rem;
		padding-top: 1.25rem;
		border-top: 1px solid var(--stone-5);
		font-style: italic;
		color: var(--bone-muted);
	}

	.ritual {
		list-style: none;
		margin: 0 0 2rem 0;
		padding: 0;
		display: grid;
		gap: 1.4rem;
	}

	.step {
		display: grid;
		grid-template-columns: clamp(48px, 6vw, 72px) 1fr;
		gap: clamp(0.9rem, 2vw, 1.4rem);
		align-items: start;
	}

	.step-numeral {
		font-family: var(--font-display);
		font-size: clamp(2rem, 3.5vw, 2.8rem);
		font-weight: 700;
		text-align: center;
		line-height: 1;
		letter-spacing: 0;
		background: linear-gradient(180deg, var(--gold-hot) 0%, var(--gold-base) 50%, var(--gold-dark) 100%);
		-webkit-background-clip: text;
		background-clip: text;
		-webkit-text-fill-color: transparent;
		text-shadow:
			0 1px 0 rgba(0, 0, 0, 0.85),
			0 0 14px rgba(227, 188, 116, 0.32);
		filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.85));
		padding-top: 0.1em;
		border-right: 1px solid var(--gold-dark);
		padding-right: clamp(0.7rem, 1.5vw, 1.1rem);
	}

	.step-body {
		min-width: 0;
	}

	.step-title {
		font-family: var(--font-display);
		font-size: var(--fs-h3);
		font-weight: 700;
		color: var(--gold-base);
		letter-spacing: var(--track-loose);
		margin: 0 0 0.4rem 0;
		text-shadow:
			0 1px 0 rgba(0, 0, 0, 0.75),
			0 0 12px rgba(227, 188, 116, 0.18);
	}

	.step-text {
		margin: 0;
		font-family: var(--font-body);
		font-size: var(--fs-body);
		line-height: 1.65;
		color: var(--bone);
	}
</style>
