<script lang="ts">
	import { onMount, untrack } from 'svelte';

	interface Props {
		value: Date | null;
		onChange: (d: Date) => void;
		min?: Date | null;
		placeholder?: string;
		ariaLabel?: string;
	}

	let {
		value,
		onChange,
		min = null,
		placeholder = 'Pick a date',
		ariaLabel = 'Date'
	}: Props = $props();

	let open = $state(false);
	let rootEl: HTMLDivElement | null = $state(null);
	let popoverEl: HTMLDivElement | null = $state(null);
	let placement = $state<'below' | 'above'>('below');

	const today = new Date();
	const todayKey = dateKey(today);

	let viewYear = $state(untrack(() => (value ? value.getFullYear() : today.getFullYear())));
	let viewMonth = $state(untrack(() => (value ? value.getMonth() : today.getMonth())));

	$effect(() => {
		if (value) {
			viewYear = value.getFullYear();
			viewMonth = value.getMonth();
		}
	});

	const monthLabel = $derived(
		new Intl.DateTimeFormat(undefined, {
			month: 'long',
			year: 'numeric'
		}).format(new Date(viewYear, viewMonth, 1))
	);

	// Weekday header (Mon-first). Use a reference week then re-order.
	const weekdays = $derived.by(() => {
		const fmt = new Intl.DateTimeFormat(undefined, { weekday: 'short' });
		const out: string[] = [];
		for (let i = 0; i < 7; i++) {
			// Jan 1, 2024 = Monday.
			out.push(fmt.format(new Date(2024, 0, 1 + i)).slice(0, 2));
		}
		return out;
	});

	interface Cell {
		date: Date;
		day: number;
		inMonth: boolean;
		isToday: boolean;
		isSelected: boolean;
		disabled: boolean;
		key: string;
	}

	const cells = $derived.by<Cell[]>(() => {
		const firstOfMonth = new Date(viewYear, viewMonth, 1);
		// JS getDay(): 0=Sun..6=Sat. We want Mon-first, so shift.
		const leadingBlanks = (firstOfMonth.getDay() + 6) % 7;

		const selectedKey = value ? dateKey(value) : null;
		const minKey = min ? dateKey(min) : null;

		const out: Cell[] = [];
		// 6 rows × 7 cols = 42 cells covers all month layouts.
		for (let i = 0; i < 42; i++) {
			const d = new Date(viewYear, viewMonth, 1 - leadingBlanks + i);
			const k = dateKey(d);
			out.push({
				date: d,
				day: d.getDate(),
				inMonth: d.getMonth() === viewMonth,
				isToday: k === todayKey,
				isSelected: selectedKey !== null && k === selectedKey,
				disabled: minKey !== null && k < minKey,
				key: k
			});
		}
		return out;
	});

	function dateKey(d: Date): string {
		const pad = (n: number) => n.toString().padStart(2, '0');
		return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
	}

	const displayValue = $derived(
		value
			? new Intl.DateTimeFormat(undefined, {
					weekday: 'short',
					day: 'numeric',
					month: 'short',
					year: 'numeric'
				}).format(value)
			: placeholder
	);

	function toggle() {
		open = !open;
		if (open) updatePlacement();
	}

	function close() {
		open = false;
	}

	function prevMonth() {
		if (viewMonth === 0) {
			viewMonth = 11;
			viewYear -= 1;
		} else {
			viewMonth -= 1;
		}
	}

	function nextMonth() {
		if (viewMonth === 11) {
			viewMonth = 0;
			viewYear += 1;
		} else {
			viewMonth += 1;
		}
	}

	function pick(d: Date) {
		// Preserve any existing time-of-day so callers using full Date keep it.
		const h = value ? value.getHours() : 0;
		const mi = value ? value.getMinutes() : 0;
		onChange(new Date(d.getFullYear(), d.getMonth(), d.getDate(), h, mi, 0, 0));
		close();
	}

	function jumpToday() {
		viewYear = today.getFullYear();
		viewMonth = today.getMonth();
	}

	function updatePlacement() {
		if (!rootEl) return;
		const rect = rootEl.getBoundingClientRect();
		const popoverHeight = 320; // approximate
		const spaceBelow = window.innerHeight - rect.bottom;
		placement = spaceBelow < popoverHeight && rect.top > popoverHeight ? 'above' : 'below';
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

<div class="d2-date-picker" class:open bind:this={rootEl}>
	<button
		type="button"
		class="trigger bevel-in"
		class:placeholder={!value}
		aria-label={ariaLabel}
		aria-haspopup="dialog"
		aria-expanded={open}
		onclick={toggle}
	>
		<span class="trigger-text">{displayValue}</span>
		<span class="chevron" aria-hidden="true">▾</span>
	</button>

	{#if open}
		<div
			class="popover anim-popover"
			class:above={placement === 'above'}
			role="dialog"
			aria-label="Choose date"
			bind:this={popoverEl}
		>
			<!-- 4 bronze rivets, matching InnerPanel. -->
			<span class="rivet rivet--tl" aria-hidden="true"></span>
			<span class="rivet rivet--tr" aria-hidden="true"></span>
			<span class="rivet rivet--bl" aria-hidden="true"></span>
			<span class="rivet rivet--br" aria-hidden="true"></span>

			<header class="cal-head">
				<button type="button" class="nav-btn" onclick={prevMonth} aria-label="Previous month">
					◄
				</button>
				<button
					type="button"
					class="month-label small-caps"
					onclick={jumpToday}
					aria-label="Jump to today"
					title="Jump to today"
				>
					{monthLabel}
				</button>
				<button type="button" class="nav-btn" onclick={nextMonth} aria-label="Next month">
					►
				</button>
			</header>

			<div class="weekdays" aria-hidden="true">
				{#each weekdays as wd, i (i)}
					<span class="weekday small-caps">{wd}</span>
				{/each}
			</div>

			<div class="days" role="grid">
				{#each cells as cell (cell.key)}
					<button
						type="button"
						role="gridcell"
						class="day"
						class:other-month={!cell.inMonth}
						class:today={cell.isToday}
						class:selected={cell.isSelected}
						class:disabled={cell.disabled}
						disabled={cell.disabled}
						aria-current={cell.isToday ? 'date' : undefined}
						aria-selected={cell.isSelected}
						onclick={() => pick(cell.date)}
					>
						{cell.day}
					</button>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.d2-date-picker {
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
		font-size: 0.85rem;
		letter-spacing: 0.03em;
		cursor: pointer;
		transition:
			border-color 140ms ease,
			color 140ms ease;
	}

	.trigger:hover {
		border-color: var(--gold-muted);
	}

	.d2-date-picker.open .trigger,
	.trigger:focus {
		outline: none;
		border-color: var(--gold-muted);
		box-shadow:
			var(--bevel-in),
			0 0 0 1px var(--gold-muted);
	}

	.trigger.placeholder .trigger-text {
		color: var(--bone-dim);
		font-style: italic;
	}

	.trigger-text {
		flex: 1;
		text-align: left;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.chevron {
		color: var(--gold-base);
		font-size: 0.75rem;
		line-height: 1;
		transition: transform 160ms ease;
	}

	.d2-date-picker.open .chevron {
		transform: rotate(180deg);
	}

	/* --- Popover --- */

	.popover {
		position: absolute;
		top: calc(100% + 6px);
		left: 0;
		z-index: 50;
		min-width: 280px;
		padding: 0.85rem 0.9rem 0.95rem;
		background: linear-gradient(180deg, var(--stone-3) 0%, var(--stone-2) 100%);
		border: 1px solid var(--stone-6);
		box-shadow:
			var(--bevel-out),
			0 14px 38px rgba(0, 0, 0, 0.85),
			0 0 0 1px rgba(0, 0, 0, 0.6);
	}

	.popover.above {
		top: auto;
		bottom: calc(100% + 6px);
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

	/* Bronze rivets, exactly matching InnerPanel pattern. */
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

	.cal-head {
		display: grid;
		grid-template-columns: auto 1fr auto;
		align-items: center;
		gap: 0.5rem;
		margin-bottom: 0.6rem;
		padding: 0 0.3rem;
	}

	.nav-btn {
		background: transparent;
		border: 1px solid var(--stone-5);
		color: var(--bone-muted);
		font-family: var(--font-mono);
		font-size: 0.7rem;
		padding: 0.3rem 0.55rem;
		cursor: pointer;
		transition:
			border-color 140ms ease,
			color 140ms ease,
			background 140ms ease;
	}

	.nav-btn:hover {
		border-color: var(--gold-muted);
		color: var(--gold-lit);
		background: rgba(227, 188, 116, 0.04);
	}

	.month-label {
		background: transparent;
		border: 0;
		color: var(--bone-bright);
		font-family: var(--font-display);
		font-size: 0.85rem;
		font-weight: 600;
		letter-spacing: var(--track-loose);
		text-align: center;
		cursor: pointer;
		padding: 0.3rem 0.4rem;
		transition: color 140ms ease;
	}

	.month-label:hover {
		color: var(--gold-lit);
	}

	.weekdays {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 2px;
		padding: 0 0.15rem 0.35rem;
		border-bottom: 1px solid var(--stone-5);
		margin-bottom: 0.35rem;
	}

	.weekday {
		font-family: var(--font-display);
		font-size: 0.65rem;
		color: var(--bone-dim);
		letter-spacing: var(--track-loose);
		text-align: center;
		padding: 0.25rem 0;
	}

	.days {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: 2px;
		padding: 0 0.15rem;
	}

	.day {
		appearance: none;
		background: transparent;
		border: 1px solid transparent;
		color: var(--bone);
		font-family: var(--font-mono);
		font-size: 0.78rem;
		padding: 0.42rem 0;
		cursor: pointer;
		transition:
			background 120ms ease,
			color 120ms ease,
			border-color 120ms ease;
	}

	.day:hover:not(:disabled) {
		background: rgba(227, 188, 116, 0.08);
		color: var(--gold-lit);
		border-color: var(--stone-6);
	}

	.day.other-month {
		color: var(--bone-faint);
		opacity: 0.55;
	}

	.day.today {
		border-color: var(--gold-deep);
		color: var(--gold-lit);
	}

	.day.selected {
		background: linear-gradient(180deg, var(--gold-lit) 0%, var(--gold-muted) 100%);
		color: #1a1405;
		border-color: var(--gold-base);
		font-weight: 700;
		box-shadow:
			inset 0 1px 0 rgba(255, 255, 255, 0.25),
			0 0 10px var(--gold-glow);
	}

	.day.selected:hover {
		background: linear-gradient(180deg, var(--gold-hot) 0%, var(--gold-lit) 100%);
		color: #1a1405;
	}

	.day.disabled {
		color: var(--stone-7);
		cursor: not-allowed;
		text-decoration: line-through;
		opacity: 0.4;
	}
</style>
