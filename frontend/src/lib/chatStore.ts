import { browser } from '$app/environment';
import { env } from '$env/dynamic/public';
import { writable, type Readable } from 'svelte/store';

export interface ChatMessage {
	id: number;
	sender_address: string;
	sender_username: string;
	content: string;
	created_at: string;
}

interface HistoryFrame {
	type: 'history';
	messages: ChatMessage[];
}

interface MessageFrame {
	type: 'message';
	message: ChatMessage;
}

type ChatFrame = HistoryFrame | MessageFrame;

function isChatMessage(value: unknown): value is ChatMessage {
	if (typeof value !== 'object' || value === null) return false;
	const m = value as Record<string, unknown>;
	return (
		typeof m.id === 'number' &&
		typeof m.sender_address === 'string' &&
		typeof m.sender_username === 'string' &&
		typeof m.content === 'string' &&
		typeof m.created_at === 'string'
	);
}

function parseFrame(raw: string): ChatFrame | null {
	let data: unknown;
	try {
		data = JSON.parse(raw);
	} catch {
		return null;
	}
	if (typeof data !== 'object' || data === null) return null;
	const f = data as Record<string, unknown>;
	if (f.type === 'history' && Array.isArray(f.messages) && f.messages.every(isChatMessage)) {
		return { type: 'history', messages: f.messages as ChatMessage[] };
	}
	if (f.type === 'message' && isChatMessage(f.message)) {
		return { type: 'message', message: f.message };
	}
	return null;
}

export interface ChatStore extends Readable<ChatMessage[]> {
	send(content: string): void;
	destroy(): void;
}

export function createChatStore(roomName: string, token: string): ChatStore {
	const { subscribe, set, update } = writable<ChatMessage[]>([]);

	let ws: WebSocket | null = null;
	let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
	let reconnectAttempts = 0;
	let isTornDown = false;
	const baseDelayMs = 1000;
	const maxDelayMs = 30000;

	function connect() {
		const wsUrl = env.PUBLIC_WS_URL;
		if (!wsUrl) {
			console.error('Missing PUBLIC_WS_URL');
			return;
		}
		const url =
			`${wsUrl}/ws/rooms/${encodeURIComponent(roomName)}/chat` +
			`?token=${encodeURIComponent(token)}`;
		ws = new WebSocket(url);

		ws.onopen = () => {
			reconnectAttempts = 0;
		};

		ws.onmessage = (event: MessageEvent<string>) => {
			const frame = parseFrame(event.data);
			if (!frame) {
				console.error('Bad chat frame', event.data);
				return;
			}
			if (frame.type === 'history') {
				set(frame.messages);
			} else {
				update((msgs) => [...msgs, frame.message]);
			}
		};

		ws.onclose = () => {
			scheduleReconnect();
		};

		ws.onerror = () => {
			ws?.close();
		};
	}

	function scheduleReconnect() {
		if (isTornDown) return;
		if (reconnectTimeout) clearTimeout(reconnectTimeout);
		const exp = Math.min(maxDelayMs, baseDelayMs * Math.pow(2, reconnectAttempts));
		const jitter = Math.random() * (exp * 0.5);
		reconnectAttempts += 1;
		reconnectTimeout = setTimeout(connect, exp + jitter);
	}

	if (browser) {
		connect();
	}

	return {
		subscribe,
		send(content: string) {
			const trimmed = content.trim();
			if (!trimmed || !ws || ws.readyState !== WebSocket.OPEN) return;
			ws.send(JSON.stringify({ content: trimmed }));
		},
		destroy() {
			isTornDown = true;
			if (reconnectTimeout) clearTimeout(reconnectTimeout);
			if (ws && (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING)) {
				ws.close();
			}
		}
	};
}
