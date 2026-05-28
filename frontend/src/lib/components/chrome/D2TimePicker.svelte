<script lang="ts">
	import { onMount, tick } from 'svelte';

	interface Props {
		/** "HH:MM" in 24h. */
		value: string;
		onChange: (value: string) => void;
		/** Minute granularity in the picker. Defaults to 5. */
		step?: 5 | 10 | 15 | 30;
		ariaLabel?: string;
	}

	let { value, onChange, step = 5, ariaLabel = 'Time' }: Props = $props();

	let open = $state(false);
	let rootEl: HTMLDivElement | null = $state(null);
	let hourListEl: HTMLDivElement | null = $state(null);
	let minuteListEl: HTMLDivElement | null = $state(null);

	const parsed = $derived.by(() => {
		const m = /^(\d{1,2}):(\d{2})$/.exec(value || '');
		if (!m) return { h: 18, mi: 0 };
		return {
			h: Math.max(0, Math.min(23, parseInt(m[1], 10))),
			mi: Math.max(0, Math.min(59, parseInt(m[2], 10)))
		};
	});

	const hours = Array.from({ length: 24 }, (_, i) => i);
	const minutes = $derived(Array.from({ length: Math.floor(60 / step) }, (_, i) => i * step));

	function pad(n: number): string {
		return n.toString().padStart(2, '0');
	}

	const display = $derived(`${pad(parsed.h)}:${pad(parsed.mi)}`);

	function emit(h: number, mi: number) {
		onChange(`${pad(h)}:${pad(mi)}`);
	}

	function pickHour(h: number) {
		emit(h, parsed.mi);
	}

	function pickMinute(mi: number) {
		emit(parsed.h, mi);
	}

	function toggle() {
		open = !open;
		if (open) {
			void scrollSelectedIntoView();
		}
	}

	function close() {
		open = false;
	}

	async function scrollSelectedIntoView() {
		await tick();
		const selH = hourListEl?.querySelector<HTMLElement>('.cell.selected');
		const selM = minuteListEl?.querySelector<HTMLElement>('.cell.selected');
		selH?.scrollIntoView({ block: 'center' });
		selM?.scrollIntoView({ block: 'center' });
	}

	onMount(() => {
		function handleOutside(e: MouseEvent) {
			if (!open) return;
			const t = e.target as Node | null;
			if (!t) return;
			if (rootEl?.contains(t)) return;
			close();
		}
		function handleKey(e: KeyboardEvent) {
			if (!open) return;
			if (e.key === 'Escape') {
				e.preventDefault();
				close();
			}
		}
		window.addEventListener('mousedown', handleOutside);
		window.addEventListener('keydown', handleKey);
		return () => {
			window.removeEventListener('mousedown', handleOutside);
			window.removeEventListener('keydown', handleKey);
		};
	});
</script>

<div class="d2-time-picker" class:open bind:this={rootEl}>
	<button
		type="button"
		class="trigger bevel-in"
		aria-label={ariaLabel}
		aria-haspopup="dialog"
		aria-expanded={open}
		onclick={toggle}
	>
		<span class="trigger-text">{display}</span>
		<span class="chevron" aria-hidden="true">▾</span>
	</button>

	{#if open}
		<div class="popover anim-popover" role="dialog" aria-label="Choose time">
			<span class="rivet rivet--tl" aria-hidden="true"></span>
			<span class="rivet rivet--tr" aria-hidden="true"></span>
			<span class="rivet rivet--bl" aria-hidden="true"></span>
			<span class="rivet rivet--br" aria-hidden="true"></span>

			<div class="cols">
				<div class="col">
					<div class="col-label small-caps">Hour</div>
					<div class="col-list scroll-d2" bind:this={hourListEl}>
						{#each hours as h (h)}
							<button
								type="button"
								class="cell"
								class:selected={h === parsed.h}
								onclick={() => pickHour(h)}
							>
								{pad(h)}
							</button>
						{/each}
					</div>
				</div>

				<div class="col">
					<div class="col-label small-caps">Min</div>
					<div class="col-list scroll-d2" bind:this={minuteListEl}>
						{#each minutes as mi (mi)}
							<button
								type="button"
								class="cell"
								class:selected={mi === parsed.mi}
								onclick={() => pickMinute(mi)}
							>
								{pad(mi)}
							</button>
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>

<style>
	.d2-time-picker {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.trigger {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 0.5rem;
		padding: 0.6rem 0.8rem;
		background: #080604;
		border: 1px solid var(--stone-5);
		color: var(--bone-bright);
		font-family: var(--font-mono);
		font-size: 0.95rem;
		letter-spacing: 0.05em;
		cursor: pointer;
		transition:
			border-color 140ms ease,
			color 140ms ease;
	}

	.trigger:hover {
		border-color: var(--gold-muted);
	}

	.d2-time-picker.open .trigger,
	.trigger:focus {
		outline: none;
		border-color: var(--gold-muted);
		box-shadow:
			var(--bevel-in),
			0 0 0 1px var(--gold-muted);
	}

	.trigger-text {
		flex: 1;
		text-align: left;
	}

	.chevron {
		color: var(--gold-base);
		font-size: 0.75rem;
		line-height: 1;
		transition: transform 160ms ease;
	}

	.d2-time-picker.open .chevron {
		transform: rotate(180deg);
	}

	.popover {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		z-index: 50;
		min-width: 200px;
		padding: 0.85rem 0.9rem;
		background: linear-gradient(180deg, var(--stone-3) 0%, var(--stone-2) 100%);
		border: 1px solid var(--stone-6);
		box-shadow:
			var(--bevel-out),
			0 14px 38px rgba(0, 0, 0, 0.85),
			0 0 0 1px rgba(0, 0, 0, 0.6);
	}

	.anim-popover {
		animation: popover-in 140ms cubic-bezier(0.2, 0.7, 0.3, 1) both;
	}

	@keyframes popover-in {
		from {
			opacity: 0;
			transform: translateY(-4px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	.rivet {
		position: absolute;
		width: 7px;
		height: 7px;
		border-radius: 50%;
		background: radial-gradient(
			circle at 35% 30%,
			var(--gold-lit) 0%,
			var(--gold-base) 35%,
			var(--gold-deep) 70%,
			#1a120a 100%
		);
		box-shadow:
			0 0 0 1px rgba(0, 0, 0, 0.7),
			0 1px 0 rgba(0, 0, 0, 0.5);
	}

	.rivet--tl {
		top: 5px;
		left: 5px;
	}
	.rivet--tr {
		top: 5px;
		right: 5px;
	}
	.rivet--bl {
		bottom: 5px;
		left: 5px;
	}
	.rivet--br {
		bottom: 5px;
		right: 5px;
	}

	.cols {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.6rem;
	}

	.col {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
		min-width: 0;
	}

	.col-label {
		font-family: var(--font-display);
		font-size: 0.65rem;
		color: var(--bone-dim);
		letter-spacing: var(--track-loose);
		text-align: center;
		padding: 0.15rem 0 0.3rem;
		border-bottom: 1px solid var(--stone-5);
	}

	.col-list {
		max-height: 200px;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		gap: 1px;
		padding: 0.15rem;
		background: rgba(0, 0, 0, 0.35);
		border: 1px solid var(--stone-5);
		box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.7);
	}

	.cell {
		appearance: none;
		background: transparent;
		border: 1px solid transparent;
		color: var(--bone);
		font-family: var(--font-mono);
		font-size: 0.85rem;
		letter-spacing: 0.05em;
		padding: 0.42rem 0.4rem;
		cursor: pointer;
		transition:
			background 120ms ease,
			color 120ms ease,
			border-color 120ms ease;
		text-align: center;
	}

	.cell:hover {
		background: rgba(227, 188, 116, 0.08);
		color: var(--gold-lit);
		border-color: var(--stone-6);
	}

	.cell.selected {
		background: linear-gradient(180deg, var(--gold-lit) 0%, var(--gold-muted) 100%);
		color: #1a1405;
		border-color: var(--gold-base);
		font-weight: 700;
		box-shadow:
			inset 0 1px 0 rgba(255, 255, 255, 0.25),
			0 0 8px var(--gold-glow);
	}

	.cell.selected:hover {
		background: linear-gradient(180deg, var(--gold-hot) 0%, var(--gold-lit) 100%);
		color: #1a1405;
	}
</style>
