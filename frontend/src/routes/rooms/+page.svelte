<script lang="ts">
	import { onMount } from 'svelte';
	import { roomsStore, type RoomSummary } from '$lib/roomsStore';
	import { env } from '$env/dynamic/public';
	import { enhance } from '$app/forms';
	import { goto } from '$app/navigation';
	import type { PageProps } from './$types';

	import InnerPanel from '$lib/components/chrome/InnerPanel.svelte';
	import SectionTitle from '$lib/components/chrome/SectionTitle.svelte';
	import OrnateButton from '$lib/components/chrome/OrnateButton.svelte';
	import StoneCheckbox from '$lib/components/chrome/StoneCheckbox.svelte';
	import Cycler from '$lib/components/chrome/Cycler.svelte';
	import ListRow from '$lib/components/chrome/ListRow.svelte';
	import PipMeter from '$lib/components/chrome/PipMeter.svelte';
	import ProgressBar from '$lib/components/chrome/ProgressBar.svelte';
	import SystemDialog from '$lib/components/chrome/SystemDialog.svelte';
	import Crest from '$lib/components/chrome/Crest.svelte';

	import { getHintsState } from '$lib/hintsContext.svelte';

	let { data, form }: PageProps = $props();

	// --- Ping ---
	let currentPing = $state<number | string>('...');

	async function measurePing() {
		const start = performance.now();
		try {
			const baseUrl = env.PUBLIC_BACKEND_URL || 'http://localhost:8000';
			await fetch(`${baseUrl}/`);
			const end = performance.now();
			currentPing = Math.round(end - start);
		} catch {
			currentPing = 'ERR';
		}
	}

	$effect(() => {
		measurePing();
		const interval = setInterval(measurePing, 15000);
		return () => clearInterval(interval);
	});

	// --- Time ---
	let currentTime = $state(new Date());
	$effect(() => {
		const interval = setInterval(() => {
			currentTime = new Date();
		}, 1000);
		return () => clearInterval(interval);
	});

	function getRemainingTime(expiresAtIso: string): string {
		const expiry = new Date(expiresAtIso).getTime();
		const diff = expiry - currentTime.getTime();
		if (diff <= 0) return '00:00';
		const minutes = Math.floor(diff / 60000);
		const seconds = Math.floor((diff % 60000) / 1000);
		return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
	}

	function timerLow(room: RoomSummary): boolean {
		return new Date(room.expires_at).getTime() - currentTime.getTime() < 60_000;
	}

	function pipForRoom(_room: RoomSummary): number {
		return 3;
	}

	// --- Active rooms ---
	let activeRooms = $derived($roomsStore.filter((r) => new Date(r.expires_at) > currentTime));

	// --- Filters ---
	interface FilterState {
		name: string;
		slots2: boolean;
		slots4: boolean;
		slots8: boolean;
		slots16: boolean;
		status: 'ANY' | 'OPEN' | 'FULL';
		ping: 'ANY' | 'LOW' | 'MID' | 'HIGH';
	}

	let filters = $state<FilterState>({
		name: '',
		slots2: false,
		slots4: false,
		slots8: false,
		slots16: false,
		status: 'ANY',
		ping: 'ANY'
	});

	function resetFilters() {
		filters.name = '';
		filters.slots2 = false;
		filters.slots4 = false;
		filters.slots8 = false;
		filters.slots16 = false;
		filters.status = 'ANY';
		filters.ping = 'ANY';
	}

	let filteredRooms = $derived.by(() => {
		const anySlot =
			filters.slots2 || filters.slots4 || filters.slots8 || filters.slots16;
		const q = filters.name.trim().toLowerCase();

		return activeRooms.filter((room) => {
			if (q) {
				const hay = `${room.name} ${room.game}`.toLowerCase();
				if (!hay.includes(q)) return false;
			}
			if (anySlot) {
				const m = room.players_max;
				const matched =
					(filters.slots2 && m === 2) ||
					(filters.slots4 && m === 4) ||
					(filters.slots8 && m === 8) ||
					(filters.slots16 && m >= 16);
				if (!matched) return false;
			}
			if (filters.status === 'OPEN' && room.players_active >= room.players_max) return false;
			if (filters.status === 'FULL' && room.players_active < room.players_max) return false;
			return true;
		});
	});

	// --- Selection ---
	let selectedName = $state<string | null>(null);
	let selectedRoom = $derived(
		selectedName ? filteredRooms.find((r) => r.name === selectedName) ?? null : null
	);
	let listColRef = $state<HTMLElement | null>(null);
	let sideColRef = $state<HTMLElement | null>(null);

	$effect(() => {
		// If the selected room disappears (filter or expiry), clear selection.
		if (selectedName && !filteredRooms.some((r) => r.name === selectedName)) {
			selectedName = null;
		}
	});

	// Click outside the list/side panel deselects current room.
	$effect(() => {
		if (!selectedName) return;
		function handler(e: MouseEvent) {
			const t = e.target as Node | null;
			if (!t) return;
			if (sideColRef?.contains(t)) return;
			if (listColRef?.contains(t)) return;
			selectedName = null;
		}
		window.addEventListener('mousedown', handler);
		return () => window.removeEventListener('mousedown', handler);
	});

	// Helper: check whether the current user is a member of the room.
	function isMemberOf(room: RoomSummary): boolean {
		if (!data.isAuthenticated || !data.user) return false;
		return room.member_addresses.includes(data.user.address);
	}

	// --- Updated-at clock for the section title trail ---
	let updatedHHMM = $derived(
		`${currentTime.getHours().toString().padStart(2, '0')}:${currentTime
			.getMinutes()
			.toString()
			.padStart(2, '0')}`
	);

	// --- Toast ---
	let toastMessage = $state<{ text: string; type: 'success' | 'error' } | null>(null);
	let toastTimeout: ReturnType<typeof setTimeout>;

	function showToast(text: string, type: 'success' | 'error') {
		toastMessage = { text, type };
		if (toastTimeout) clearTimeout(toastTimeout);
		toastTimeout = setTimeout(() => {
			toastMessage = null;
		}, 4500);
	}

	$effect(() => {
		if (form) {
			if ('error' in form && form.error) {
				showToast(form.error, 'error');
			} else if ('success' in form && form.success && form.message) {
				showToast(form.message, 'success');
			}
		}
	});

	// --- Create dialog ---
	let createOpen = $state(false);

	// --- Refs ---
	let nameInputRef = $state<HTMLInputElement | null>(null);

	// --- Hints + global keys ---
	const hintsState = getHintsState();

	$effect(() => {
		hintsState?.set([
			{ key: 'Enter', label: 'Open', tone: 'gold' },
			{ key: 'R', label: 'Refresh', tone: 'green' },
			{ key: '/', label: 'Search', tone: 'amber' },
			{ key: 'N', label: 'Create', tone: 'gold' },
			{ key: 'Esc', label: 'Back', tone: 'red' }
		]);
	});

	onMount(() => {
		const handler = (e: KeyboardEvent) => {
			const target = e.target as HTMLElement | null;
			const tag = target?.tagName;
			const isTyping =
				tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || target?.isContentEditable;

			if (e.key === 'Escape') {
				if (createOpen) {
					createOpen = false;
					e.preventDefault();
					return;
				}
				if (selectedName) {
					selectedName = null;
					e.preventDefault();
					return;
				}
				if (!isTyping) {
					history.back();
				}
				return;
			}

			if (isTyping) return;

			if (e.key === '/') {
				e.preventDefault();
				nameInputRef?.focus();
				return;
			}
			if (e.key === 'r' || e.key === 'R') {
				e.preventDefault();
				location.reload();
				return;
			}
			if (e.key === 'n' || e.key === 'N') {
				if (data.isAuthenticated) {
					e.preventDefault();
					createOpen = true;
				}
				return;
			}
			if (e.key === 'Enter' && selectedRoom && data.isAuthenticated && data.user) {
				const isMember = selectedRoom.member_addresses.includes(data.user.address);
				if (isMember) {
					e.preventDefault();
					goto(`/rooms/${encodeURIComponent(selectedRoom.name)}`);
				}
			}
		};

		window.addEventListener('keydown', handler);
		return () => window.removeEventListener('keydown', handler);
	});
</script>

<svelte:head>
	<title>PlayLink — Game List</title>
</svelte:head>

<div class="rooms-page">
	<header class="page-head">
		<SectionTitle title="Game List" size="large" tone="gold">
			{#snippet children()}
				<span>{activeRooms.length} ACTIVE · UPDATED {updatedHHMM}</span>
			{/snippet}
		</SectionTitle>
	</header>

	<div class="split">
		<div class="list-col" bind:this={listColRef}>
			<InnerPanel padded={false}>
				<div class="list">
					<ListRow header>
						{#snippet children()}
							<span>Game Name</span>
							<span class="col-game">Game</span>
							<span>Players</span>
							<span class="col-ping">Ping</span>
							<span class="col-timer">Timer</span>
						{/snippet}
					</ListRow>

					<div class="rows scroll-d2">
						{#each filteredRooms as room (room.name)}
							{@const member = isMemberOf(room)}
							<ListRow
								selected={selectedName === room.name}
								member={member}
								onclick={() => (selectedName = room.name)}
							>
								{#snippet children()}
									<span class="cell-name fw-700" class:is-member={member}>
										{room.name}
										{#if member}
											<span class="member-tag" aria-label="You are a member">JOINED</span>
										{/if}
									</span>
									<span class="cell-game col-game">{room.game}</span>
									<span class="cell-slots mono">
										{room.players_active}/{room.players_max}
									</span>
									<span class="cell-ping col-ping">
										<PipMeter value={pipForRoom(room)} tone="auto" size="md" />
									</span>
									<span class="cell-timer mono col-timer" class:warn={timerLow(room)}>
										{getRemainingTime(room.expires_at)}
									</span>
								{/snippet}
							</ListRow>
						{/each}

						{#if filteredRooms.length === 0}
							<div class="empty">
								<Crest size={64} tone="iron" />
								<p>Awaiting signals…</p>
							</div>
						{/if}
					</div>
				</div>
			</InnerPanel>
		</div>

		<aside class="side-col" bind:this={sideColRef}>
			<InnerPanel>
				{#snippet children()}
					{#if selectedRoom}
						{@const room = selectedRoom}
						{@const isMember =
							data.isAuthenticated &&
							data.user !== null &&
							room.member_addresses.includes(data.user.address)}
						{@const isFull = room.players_active >= room.players_max}

						<SectionTitle title={room.name} size="normal" tone="bone" />

						<dl class="details">
							<dt>Game</dt>
							<dd>{room.game}</dd>
							<dt>Players</dt>
							<dd class="mono">{room.players_active} / {room.players_max}</dd>
							<dt>Expires</dt>
							<dd class="mono" class:warn={timerLow(room)}>
								{getRemainingTime(room.expires_at)}
							</dd>
						</dl>

						<div class="bar-wrap">
							<ProgressBar
								value={room.players_active}
								max={room.players_max}
								ticks
								variant="gold"
							/>
						</div>

						{#if data.isAuthenticated}
							<div class="actions stack">
								<form
									method="POST"
									action="?/join"
									use:enhance
									class="action-form"
								>
									<input type="hidden" name="room_name" value={room.name} />
									<OrnateButton
										variant="primary"
										size="md"
										type="submit"
										fullWidth
										disabled={isMember || isFull}
									>
										{#snippet children()}Join{/snippet}
									</OrnateButton>
								</form>

								<form
									method="POST"
									action="?/leave"
									use:enhance
									class="action-form"
								>
									<input type="hidden" name="room_name" value={room.name} />
									<OrnateButton
										variant="danger"
										size="md"
										type="submit"
										fullWidth
										disabled={!isMember}
									>
										{#snippet children()}Leave{/snippet}
									</OrnateButton>
								</form>

								{#if isMember}
									<OrnateButton
										variant="secondary"
										size="md"
										fullWidth
										href="/rooms/{encodeURIComponent(room.name)}"
									>
										{#snippet children()}Open{/snippet}
									</OrnateButton>
								{/if}

								<OrnateButton
									variant="ghost"
									size="sm"
									fullWidth
									onclick={() => (selectedName = null)}
								>
									{#snippet children()}Back to Filters{/snippet}
								</OrnateButton>
							</div>
						{:else}
							<p class="auth-note">Identity required to join or leave.</p>
							<OrnateButton
								variant="ghost"
								size="sm"
								fullWidth
								onclick={() => (selectedName = null)}
							>
								{#snippet children()}Back to Filters{/snippet}
							</OrnateButton>
						{/if}
					{:else}
						<SectionTitle title="Filters" size="small" tone="gold" />

						<div class="filter-group">
							<span class="filter-label small-caps">Max Slots</span>
							<div class="checks">
								<StoneCheckbox bind:checked={filters.slots2} label="2" size="sm" />
								<StoneCheckbox bind:checked={filters.slots4} label="4" size="sm" />
								<StoneCheckbox bind:checked={filters.slots8} label="8" size="sm" />
								<StoneCheckbox bind:checked={filters.slots16} label="16+" size="sm" />
							</div>
						</div>

						<div class="filter-group">
							<Cycler
								label="Status"
								bind:value={filters.status}
								values={['ANY', 'OPEN', 'FULL']}
							/>
						</div>

						<div class="filter-group">
							<Cycler
								label="Ping"
								bind:value={filters.ping}
								values={['ANY', 'LOW', 'MID', 'HIGH']}
							/>
						</div>

						<div class="filter-actions">
							<OrnateButton
								variant="secondary"
								size="sm"
								fullWidth
								onclick={resetFilters}
							>
								{#snippet children()}Reset Filters{/snippet}
							</OrnateButton>
						</div>

						<SectionTitle title="Name Filter" size="small" tone="gold" />
						<div class="name-filter">
							<input
								class="text-input bevel-in"
								type="text"
								bind:value={filters.name}
								bind:this={nameInputRef}
								placeholder="Filter by name…"
							/>
						</div>

						<SectionTitle title="Status" size="small" tone="gold" />
						<div class="stats">
							<div class="stat">
								<span class="stat-label small-caps">Open</span>
								<span class="stat-value etched-bone">{activeRooms.length}</span>
							</div>
							<div class="stat">
								<span class="stat-label small-caps">Ping</span>
								<span class="stat-value mono">
									{currentPing}
									<small>MS</small>
								</span>
							</div>
						</div>
					{/if}
				{/snippet}
			</InnerPanel>
		</aside>
	</div>
</div>

<div class="create-fab">
	{#if !data.isAuthenticated}
		<span class="auth-warn small-caps">Identity required</span>
	{/if}
	<OrnateButton
		variant="primary"
		size="md"
		disabled={!data.isAuthenticated}
		onclick={() => (createOpen = true)}
	>
		{#snippet children()}+ Create Lobby{/snippet}
	</OrnateButton>
</div>

<SystemDialog
	bind:open={createOpen}
	title="Configure Signal"
	tone="gold"
	modal
	width="480px"
	onclose={() => (createOpen = false)}
>
	{#snippet children()}
		{#if form && 'error' in form && form.error}
			<p class="dialog-error">{form.error}</p>
		{/if}

		<form
			id="create-form"
			method="POST"
			action="?/create"
			use:enhance={() => {
				return async ({ update }) => {
					await update();
					if (!form || !('error' in form) || !form.error) {
						createOpen = false;
					}
				};
			}}
		>
			<div class="form-row">
				<label for="create-name" class="small-caps">Identifier (Lobby Name)</label>
				<input
					id="create-name"
					class="text-input bevel-in"
					type="text"
					name="name"
					required
					placeholder="e.g. My Retro Match"
				/>
			</div>

			<div class="form-row">
				<label for="create-game" class="small-caps">Target Program (Game)</label>
				<select
					id="create-game"
					class="text-input bevel-in"
					name="game"
					required
					disabled={!data.games.length}
				>
					{#if data.games.length > 0}
						{#each data.games as g (g)}
							<option value={g}>{g}</option>
						{/each}
					{:else}
						<option value="" disabled selected>No games available</option>
					{/if}
				</select>
			</div>

			<div class="form-row">
				<label for="create-slots" class="small-caps">Max Connections (Slots)</label>
				<input
					id="create-slots"
					class="text-input bevel-in"
					type="number"
					name="players_max"
					min="2"
					max="64"
					value="4"
					required
				/>
			</div>
		</form>
	{/snippet}

	{#snippet footer()}
		<OrnateButton variant="ghost" size="md" onclick={() => (createOpen = false)}>
			{#snippet children()}Cancel{/snippet}
		</OrnateButton>
		<OrnateButton
			variant="primary"
			size="md"
			onclick={() => {
				const f = document.getElementById('create-form') as HTMLFormElement | null;
				f?.requestSubmit();
			}}
		>
			{#snippet children()}Broadcast{/snippet}
		</OrnateButton>
	{/snippet}
</SystemDialog>

{#if toastMessage}
	{@const toast = toastMessage}
	<SystemDialog
		open={true}
		title={toast.type === 'error' ? 'System Error' : 'System Confirm'}
		tone={toast.type === 'error' ? 'blood' : 'green'}
		position="bottom-right"
		onclose={() => (toastMessage = null)}
	>
		{#snippet children()}
			<p class="toast-text">{toast.text}</p>
		{/snippet}
	</SystemDialog>
{/if}

<style>
	.rooms-page {
		display: flex;
		flex-direction: column;
		gap: 1.25rem;
		min-height: 0;
		flex: 1;
		padding: 0.5rem 0 4rem;
	}

	.page-head {
		padding: 0 0.5rem;
	}

	.split {
		display: grid;
		grid-template-columns: 1fr;
		gap: 1.25rem;
		min-height: 0;
		flex: 1;
	}

	/* Tablet portrait/landscape: keep side panel visible, slightly narrower. */
	@media (min-width: 768px) and (max-width: 1023px) {
		.split {
			grid-template-columns: 6fr 4fr;
		}
		.side-col {
			position: sticky;
			top: 0;
			align-self: start;
			max-height: calc(100vh - 6rem);
			overflow: auto;
		}
	}

	@media (min-width: 1024px) {
		.split {
			grid-template-columns: 7fr 3fr;
			position: relative;
		}

		.side-col {
			position: sticky;
			top: 0;
			align-self: start;
			max-height: calc(100vh - 8rem);
			overflow: auto;
		}
	}

	.list-col {
		display: flex;
		min-height: 0;
	}

	.list-col :global(.inner-panel) {
		display: flex;
		flex-direction: column;
		min-height: 480px;
	}

	.list {
		display: flex;
		flex-direction: column;
		min-height: 0;
		flex: 1;
		/* Default (mobile): 3 visible columns — Name, Players, Ping */
		--list-cols: 1.6fr 0.8fr 0.7fr;
		--list-gap: 0.8rem;
	}

	/* Hide non-essential columns on narrow viewports. */
	.list :global(.col-game),
	.list :global(.col-timer) {
		display: none;
	}

	@media (min-width: 600px) {
		.list {
			/* Add Timer */
			--list-cols: 1.6fr 0.8fr 0.7fr 0.6fr;
			--list-gap: 1rem;
		}
		.list :global(.col-timer) {
			display: inline-flex;
		}
	}

	@media (min-width: 900px) {
		.list {
			/* Add Game column → all 5 visible */
			--list-cols: 1.6fr 1fr 0.7fr 0.8fr 0.6fr;
			--list-gap: 1.2rem;
		}
		.list :global(.col-game) {
			display: inline-flex;
		}
	}

	@media (min-width: 1280px) {
		.list {
			--list-cols: 1.7fr 1fr 0.6fr 0.7fr 0.5fr;
			--list-gap: 1.5rem;
		}
	}

	.rows {
		display: flex;
		flex-direction: column;
		flex: 1;
		min-height: 0;
		max-height: calc(100vh - 16rem);
		overflow-y: auto;
	}

	.empty {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		gap: 1rem;
		padding: 4rem 1rem;
		flex: 1;
	}

	.empty p {
		margin: 0;
		font-style: italic;
		color: var(--bone-muted);
		font-family: var(--font-display);
		letter-spacing: var(--track-loose);
	}

	/* Cells */
	.cell-name {
		color: var(--bone-bright);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		display: inline-flex;
		align-items: center;
		gap: 0.55rem;
	}

	.cell-name.is-member {
		color: var(--gold-lit);
	}

	.member-tag {
		display: inline-block;
		font-family: var(--font-display);
		font-size: 0.62em;
		letter-spacing: var(--track-extra);
		padding: 1px 6px;
		color: var(--gold-hot);
		background: linear-gradient(180deg, rgba(227, 188, 116, 0.18), rgba(138, 108, 58, 0.12));
		border: 1px solid rgba(227, 188, 116, 0.5);
		text-shadow: 0 0 6px rgba(255, 232, 144, 0.45);
		flex-shrink: 0;
	}

	.cell-game {
		color: var(--bone-muted);
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		transition: color 140ms ease;
	}

	:global(.row.is-interactive:hover) .cell-game,
	:global(.row.is-selected) .cell-game,
	:global(.row.is-member) .cell-game {
		color: var(--bone);
	}

	.cell-slots {
		color: var(--bone);
	}

	.cell-timer {
		color: var(--bone);
	}

	.cell-timer.warn {
		color: var(--blood-bright);
	}

	.cell-ping {
		display: inline-flex;
		align-items: center;
	}

	.fw-700 {
		font-weight: 700;
	}

	.mono {
		font-family: var(--font-mono);
		letter-spacing: 0.04em;
		font-feature-settings: normal;
		text-transform: none;
	}

	/* Side panel */
	.details {
		display: grid;
		grid-template-columns: auto 1fr;
		gap: 0.4rem 1rem;
		margin: 0 0 1rem 0;
		padding: 0.5rem 0 1rem;
		border-bottom: 1px solid var(--stone-5);
	}

	.details dt {
		font-family: var(--font-display);
		font-size: 0.7rem;
		letter-spacing: var(--track-extra);
		text-transform: uppercase;
		color: var(--bone-muted);
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}

	.details dd {
		margin: 0;
		color: var(--bone-bright);
		font-family: var(--font-display);
		font-size: 0.85rem;
		letter-spacing: var(--track-loose);
		text-transform: uppercase;
	}

	.details dd.mono {
		font-family: var(--font-mono);
		text-transform: none;
		letter-spacing: 0.04em;
	}

	.details dd.warn {
		color: var(--blood-bright);
	}

	.bar-wrap {
		margin-bottom: 1.25rem;
	}

	.actions.stack {
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
	}

	.action-form {
		display: contents;
	}

	.auth-note {
		font-family: var(--font-display);
		font-size: 0.78rem;
		letter-spacing: var(--track-loose);
		color: var(--blood-bright);
		text-transform: uppercase;
		margin: 0 0 1rem 0;
	}

	.filter-group {
		margin-bottom: 1.1rem;
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.filter-label {
		font-family: var(--font-display);
		font-size: 0.7rem;
		letter-spacing: var(--track-extra);
		color: var(--bone-muted);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}

	.checks {
		display: flex;
		flex-wrap: wrap;
		gap: 0.75rem 1rem;
	}

	.filter-actions {
		margin-bottom: 1.25rem;
	}

	.name-filter {
		margin-bottom: 1.25rem;
	}

	.text-input {
		width: 100%;
		background: linear-gradient(180deg, #060503 0%, #0a0907 100%);
		border: 1px solid var(--stone-5);
		border-radius: 0;
		color: var(--bone-bright);
		padding: 0.65rem 0.8rem;
		font-family: var(--font-mono);
		font-size: 0.85rem;
		letter-spacing: 0.03em;
	}

	.text-input::placeholder {
		color: var(--bone-dim);
		font-style: italic;
	}

	.text-input:focus {
		outline: none;
		border-color: var(--gold-muted);
		box-shadow:
			inset 0 1px 2px rgba(0, 0, 0, 0.85),
			var(--glow-soft);
	}

	.stats {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 0.75rem;
		padding-top: 0.5rem;
	}

	.stat {
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
		padding: 0.6rem 0.75rem;
		border: 1px solid var(--stone-5);
		background: linear-gradient(180deg, #0a0907 0%, #060503 100%);
	}

	.stat-label {
		font-family: var(--font-display);
		font-size: 0.65rem;
		letter-spacing: var(--track-extra);
		color: var(--bone-muted);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}

	.stat-value {
		font-family: var(--font-display);
		font-size: 1.4rem;
		color: var(--bone-bright);
		letter-spacing: var(--track-loose);
	}

	.stat-value.mono {
		font-family: var(--font-mono);
		font-size: 1.05rem;
		letter-spacing: 0.04em;
		text-transform: none;
	}

	.stat-value small {
		font-size: 0.6rem;
		color: var(--bone-muted);
		margin-left: 0.2rem;
		font-family: var(--font-display);
		letter-spacing: var(--track-loose);
		text-transform: uppercase;
	}

	/* Floating create button — fixed only on desktop (≥1024px).
	   On smaller screens the side panel stacks below the list and the FAB
	   would overlap it, so it flows into normal document order at the bottom. */
	.create-fab {
		display: flex;
		align-items: center;
		justify-content: flex-end;
		gap: 0.75rem;
		flex-wrap: wrap;
		margin: 1.5rem 0.5rem 1.25rem;
	}

	@media (min-width: 1024px) {
		.create-fab {
			position: fixed;
			right: 2rem;
			bottom: 5.5rem;
			margin: 0;
			justify-content: flex-end;
			z-index: 50;
		}
	}

	.auth-warn {
		font-family: var(--font-mono);
		font-size: 0.7rem;
		letter-spacing: var(--track-loose);
		color: var(--blood-bright);
		text-transform: uppercase;
		padding: 0.45rem 0.7rem;
		background: linear-gradient(180deg, #0a0907 0%, #060503 100%);
		border: 1px solid #4a1414;
	}

	.dialog-error {
		font-family: var(--font-mono);
		font-size: 0.8rem;
		color: var(--blood-bright);
		margin: 0 0 1rem 0;
		padding: 0.6rem 0.8rem;
		border: 1px solid #4a1414;
		background: rgba(181, 54, 54, 0.08);
	}

	.toast-text {
		margin: 0;
		font-family: var(--font-display);
		font-size: 0.9rem;
		color: var(--bone-bright);
		letter-spacing: var(--track-loose);
	}

	/* Create dialog form rows */
	.form-row {
		margin-bottom: 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.form-row label {
		font-family: var(--font-display);
		font-size: 0.7rem;
		letter-spacing: var(--track-extra);
		color: var(--bone-muted);
		text-transform: uppercase;
		font-feature-settings:
			'smcp' 1,
			'c2sc' 1;
	}
</style>
