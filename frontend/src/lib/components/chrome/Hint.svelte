<script lang="ts">
	type Tone = 'gold' | 'green' | 'amber' | 'red' | 'stone' | 'blue';

	interface Props {
		key: string;
		label: string;
		tone?: Tone;
		onclick?: () => void;
	}

	let { key, label, tone = 'stone', onclick }: Props = $props();

	const Tag = $derived(onclick ? 'button' : 'span');
</script>

{#if onclick}
	<button class="hint tone-{tone}" type="button" onclick={onclick}>
		<span class="key">{key}</span>
		<span class="label small-caps">{label}</span>
	</button>
{:else}
	<span class="hint tone-{tone}">
		<span class="key">{key}</span>
		<span class="label small-caps">{label}</span>
	</span>
{/if}

<style>
	.hint {
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
		font-family: var(--font-display);
		background: transparent;
		border: 0;
		padding: 0;
		color: inherit;
	}

	.hint.tone-gold .key {
		--key-bg: linear-gradient(180deg, #f1cf8f 0%, #c29d59 100%);
		--key-text: #1a1405;
		--key-glow: rgba(227, 188, 116, 0.45);
	}
	.hint.tone-green .key {
		--key-bg: linear-gradient(180deg, #9ddc6e 0%, #5a9438 100%);
		--key-text: #0d1d05;
		--key-glow: rgba(127, 191, 92, 0.45);
	}
	.hint.tone-amber .key {
		--key-bg: linear-gradient(180deg, #f0c068 0%, #a87922 100%);
		--key-text: #221606;
		--key-glow: rgba(227, 166, 71, 0.45);
	}
	.hint.tone-red .key {
		--key-bg: linear-gradient(180deg, #d35858 0%, #7a2020 100%);
		--key-text: #200505;
		--key-glow: rgba(181, 54, 54, 0.5);
	}
	.hint.tone-blue .key {
		--key-bg: linear-gradient(180deg, #6cb0d8 0%, #2e5e7a 100%);
		--key-text: #061520;
		--key-glow: rgba(108, 176, 216, 0.4);
	}
	.hint.tone-stone .key {
		--key-bg: linear-gradient(180deg, #585141 0%, #2a251c 100%);
		--key-text: #e4d8b8;
		--key-glow: rgba(0, 0, 0, 0.5);
	}

	.key {
		min-width: 28px;
		height: 24px;
		padding: 0 0.5rem;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		background: var(--key-bg);
		color: var(--key-text);
		font-family: var(--font-mono);
		font-size: 0.62rem;
		font-weight: bold;
		letter-spacing: 0.05em;
		text-transform: uppercase;
		border: 1px solid rgba(0, 0, 0, 0.7);
		box-shadow:
			0 0 8px var(--key-glow),
			inset 0 1px 0 rgba(255, 255, 255, 0.18),
			inset 0 -1px 0 rgba(0, 0, 0, 0.5);
		text-shadow: 0 1px 0 rgba(255, 255, 255, 0.15);
	}

	.label {
		color: var(--bone-muted);
		font-size: 0.72rem;
		letter-spacing: var(--track-loose);
	}

	button.hint {
		cursor: url('/cursor/help.cur'), pointer;
	}
	button.hint:hover .label {
		color: var(--gold-lit);
	}
	button.hint:hover .key {
		border-color: var(--gold-muted);
	}
</style>
