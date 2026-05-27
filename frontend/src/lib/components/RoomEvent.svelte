<script lang="ts">
	import { enhance } from '$app/forms';
	import type { RoomEventState, RsvpEntry, RsvpStatus } from '$lib/chatStore';

	interface Props {
		event: RoomEventState | null;
		isCreator: boolean;
		isMember: boolean;
		viewerAddress: string;
		members: { address: string; username?: string }[];
	}

	let {
		event,
		isCreator,
		isMember,
		viewerAddress,
		members
	}: Props = $props();

	let editing = $state(false);
	let draftStart = $state('');

	const viewerLower = $derived(viewerAddress.toLowerCase());

	const myRsvp: RsvpEntry | undefined = $derived(
		event?.rsvps.find((r) => r.address.toLowerCase() === viewerLower)
	);

	function startEditing() {
		editing = true;
		draftStart = isoToLocalInput(event?.starts_at);
	}

	function cancelEditing() {
		editing = false;
		draftStart = '';
	}

	/**
	 * Convert an ISO timestamp into the value expected by `<input type="datetime-local">`.
	 * The backend stores UTC; the picker speaks the user's local time, so we
	 * format relative to the local zone and strip the seconds.
	 */
	function isoToLocalInput(iso?: string): string {
		if (!iso) {
			const d = new Date(Date.now() + 30 * 60 * 1000);
			return formatLocalForInput(d);
		}
		return formatLocalForInput(new Date(iso));
	}

	function formatLocalForInput(d: Date): string {
		const pad = (n: number) => n.toString().padStart(2, '0');
		return (
			`${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` +
			`T${pad(d.getHours())}:${pad(d.getMinutes())}`
		);
	}

	const startsAtFormatted = $derived.by(() => {
		if (!event) return '';
		try {
			return new Intl.DateTimeFormat(undefined, {
				weekday: 'short',
				day: 'numeric',
				month: 'short',
				year: 'numeric',
				hour: '2-digit',
				minute: '2-digit'
			}).format(new Date(event.starts_at));
		} catch {
			return event.starts_at;
		}
	});

	let now = $state(new Date());

	$effect(() => {
		const id = setInterval(() => {
			now = new Date();
		}, 1000);
		return () => clearInterval(id);
	});

	const countdown = $derived.by(() => {
		if (!event) return '';
		const diff = new Date(event.starts_at).getTime() - now.getTime();
		if (diff <= 0) return 'STARTING NOW';
		const totalSeconds = Math.floor(diff / 1000);
		const days = Math.floor(totalSeconds / 86400);
		const hours = Math.floor((totalSeconds % 86400) / 3600);
		const minutes = Math.floor((totalSeconds % 3600) / 60);
		const seconds = totalSeconds % 60;
		const pad = (n: number) => n.toString().padStart(2, '0');
		if (days > 0) return `${days}d ${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
		return `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
	});

	const rosterEntries = $derived.by(() => {
		const rsvpByAddr: Record<string, RsvpEntry> = {};
		for (const r of event?.rsvps ?? []) {
			rsvpByAddr[r.address.toLowerCase()] = r;
		}
		return members.map((m) => {
			const found = rsvpByAddr[m.address.toLowerCase()];
			return {
				address: m.address,
				username: m.username ?? found?.username ?? shortAddr(m.address),
				status: found?.status ?? null
			};
		});
	});

	function shortAddr(addr: string): string {
		if (addr.length <= 10) return addr;
		return `${addr.slice(0, 6)}…${addr.slice(-4)}`;
	}

	function statusLabel(status: RsvpStatus | null): string {
		if (status === 'present') return 'PRESENT';
		if (status === 'absent') return 'ABSENT';
		if (status === 'maybe') return 'MAYBE';
		return 'NO RESPONSE';
	}
</script>

<section class="event-panel">
	<div class="event-header">
		<span class="eyebrow">— SCHEDULED EVENT</span>
	</div>

	{#if !event && !editing}
		<div class="empty">
			{#if isCreator}
				<p class="empty-text">No event scheduled. Pick a moment for the warband.</p>
				<button type="button" class="btn btn-primary" onclick={startEditing}>
					[ SCHEDULE EVENT ]
				</button>
			{:else}
				<p class="empty-text">No event scheduled yet. The room creator can pick a time.</p>
			{/if}
		</div>
	{/if}

	{#if event && !editing}
		<div class="event-meta">
			<div class="event-time">
				<span class="time-value">{startsAtFormatted}</span>
				<span class="countdown">{countdown}</span>
			</div>
			{#if isCreator}
				<div class="creator-actions">
					<button type="button" class="btn btn-secondary" onclick={startEditing}>
						[ RESCHEDULE ]
					</button>
					<form
						method="POST"
						action="?/cancelEvent"
						use:enhance
						style="display: contents;"
					>
						<button type="submit" class="btn btn-danger">[ CANCEL EVENT ]</button>
					</form>
				</div>
			{/if}
		</div>

		{#if isMember}
			<div class="rsvp-controls">
				<span class="rsvp-label">YOUR RSVP</span>
				<div class="rsvp-buttons">
					{#each ['present', 'maybe', 'absent'] as status (status)}
						<form method="POST" action="?/setRsvp" use:enhance>
							<input type="hidden" name="status" value={status} />
							<button
								type="submit"
								class="rsvp-btn"
								class:active={myRsvp?.status === status}
								data-status={status}
							>
								[ {statusLabel(status as RsvpStatus)} ]
							</button>
						</form>
					{/each}
				</div>
			</div>
		{/if}

		<div class="roster">
			<span class="roster-label">RSVP ROSTER</span>
			{#if rosterEntries.length === 0}
				<p class="empty-text">No members yet.</p>
			{:else}
				<ul class="roster-list">
					{#each rosterEntries as entry (entry.address)}
						<li class="roster-row" data-status={entry.status ?? 'none'}>
							<span class="roster-name">{entry.username}</span>
							<span class="roster-status">{statusLabel(entry.status)}</span>
						</li>
					{/each}
				</ul>
			{/if}
		</div>
	{/if}

	{#if editing}
		<form
			method="POST"
			action="?/scheduleEvent"
			class="schedule-form"
			use:enhance={() => {
				return async ({ update }) => {
					await update();
					editing = false;
				};
			}}
		>
			<label class="schedule-label">
				<span class="rsvp-label">EVENT START (LOCAL TIME)</span>
				<input
					type="datetime-local"
					name="starts_at"
					bind:value={draftStart}
					required
				/>
			</label>
			<div class="schedule-actions">
				<button type="submit" class="btn btn-primary">[ SAVE ]</button>
				<button type="button" class="btn btn-secondary" onclick={cancelEditing}>
					[ CANCEL ]
				</button>
			</div>
		</form>
	{/if}
</section>

<style>
	.event-panel {
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(227, 188, 116, 0.2);
		border-radius: 12px;
		padding: 1rem 1.2rem;
		display: flex;
		flex-direction: column;
		gap: 0.9rem;
	}

	.event-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.eyebrow,
	.rsvp-label,
	.roster-label {
		font-family: ui-monospace, SFMono-Regular, monospace;
		font-size: 0.7rem;
		letter-spacing: 0.18em;
		color: #8c877a;
		text-transform: uppercase;
	}

	.empty {
		border: 1px dashed rgba(227, 188, 116, 0.3);
		border-radius: 8px;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 0.6rem;
		align-items: flex-start;
	}

	.empty-text {
		margin: 0;
		color: rgba(244, 236, 216, 0.6);
		font-size: 0.9rem;
	}

	.event-meta {
		display: flex;
		justify-content: space-between;
		align-items: center;
		flex-wrap: wrap;
		gap: 0.7rem;
	}

	.event-time {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
	}

	.time-value {
		font-family: 'Exocet', serif;
		font-size: 1.4rem;
		color: #f1e9cd;
		letter-spacing: 0.02em;
	}

	.countdown {
		font-family: ui-monospace, monospace;
		font-size: 0.85rem;
		color: #e3bc74;
	}

	.creator-actions {
		display: flex;
		gap: 0.5rem;
	}

	.rsvp-controls {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	.rsvp-buttons {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
	}

	.rsvp-btn {
		flex: 1;
		min-width: 110px;
		background: transparent;
		border: 1px solid #28251e;
		color: #8c877a;
		padding: 0.55rem 0.8rem;
		font-family: ui-monospace, monospace;
		font-size: 0.7rem;
		letter-spacing: 0.15em;
		cursor: pointer;
		border-radius: 4px;
		transition:
			border-color 0.2s,
			color 0.2s,
			background 0.2s;
	}

	.rsvp-btn:hover {
		border-color: #e3bc74;
		color: #e3bc74;
	}

	.rsvp-btn.active[data-status='present'] {
		border-color: #a4ce82;
		color: #1a1405;
		background: #a4ce82;
	}
	.rsvp-btn.active[data-status='maybe'] {
		border-color: #e3bc74;
		color: #1a1405;
		background: #e3bc74;
	}
	.rsvp-btn.active[data-status='absent'] {
		border-color: #ff6b6b;
		color: #1a1405;
		background: #ff6b6b;
	}

	.roster {
		display: flex;
		flex-direction: column;
		gap: 0.4rem;
	}

	.roster-list {
		list-style: none;
		margin: 0;
		padding: 0;
		display: flex;
		flex-direction: column;
		gap: 0.25rem;
	}

	.roster-row {
		display: flex;
		justify-content: space-between;
		padding: 0.45rem 0.7rem;
		background: rgba(0, 0, 0, 0.25);
		border-radius: 4px;
		font-family: ui-monospace, monospace;
		font-size: 0.8rem;
	}

	.roster-name {
		color: #f1e9cd;
	}

	.roster-status {
		letter-spacing: 0.12em;
	}

	.roster-row[data-status='present'] .roster-status {
		color: #a4ce82;
	}
	.roster-row[data-status='maybe'] .roster-status {
		color: #e3bc74;
	}
	.roster-row[data-status='absent'] .roster-status {
		color: #ff6b6b;
	}
	.roster-row[data-status='none'] .roster-status {
		color: rgba(244, 236, 216, 0.4);
	}

	.schedule-form {
		display: flex;
		flex-direction: column;
		gap: 0.7rem;
	}

	.schedule-label {
		display: flex;
		flex-direction: column;
		gap: 0.35rem;
	}

	.schedule-form input[type='datetime-local'] {
		background: #141415;
		border: 1px solid #28251e;
		color: #f1e9cd;
		padding: 0.6rem;
		border-radius: 4px;
		font-family: ui-monospace, monospace;
		font-size: 0.9rem;
	}

	.schedule-form input[type='datetime-local']:focus {
		outline: none;
		border-color: #e3bc74;
	}

	.schedule-actions {
		display: flex;
		gap: 0.5rem;
	}

	.btn {
		font-family: ui-monospace, monospace;
		font-size: 0.7rem;
		letter-spacing: 0.15em;
		padding: 0.55rem 0.9rem;
		border-radius: 4px;
		cursor: pointer;
		text-transform: uppercase;
		transition: all 0.2s;
	}

	.btn-primary {
		background: #e3bc74;
		color: #1a1405;
		border: none;
		font-weight: 600;
	}

	.btn-primary:hover {
		background: #f1cf8f;
	}

	.btn-secondary {
		background: transparent;
		color: #a39c8c;
		border: 1px solid #3d3930;
	}

	.btn-secondary:hover {
		border-color: #e3bc74;
		color: #e3bc74;
	}

	.btn-danger {
		background: transparent;
		color: #ff6b6b;
		border: 1px solid rgba(255, 107, 107, 0.5);
	}

	.btn-danger:hover {
		background: rgba(255, 107, 107, 0.1);
		border-color: #ff6b6b;
	}
</style>
