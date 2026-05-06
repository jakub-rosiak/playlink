import { getContext, setContext } from 'svelte';

export type HintTone = 'gold' | 'green' | 'amber' | 'red' | 'stone' | 'blue';

export interface HintEntry {
	key: string;
	label: string;
	tone?: HintTone;
	onclick?: () => void;
}

const KEY = Symbol('hints');

export class HintsState {
	hints = $state<HintEntry[]>([]);

	constructor(initial: HintEntry[] = []) {
		this.hints = initial;
	}

	set(entries: HintEntry[]) {
		this.hints = entries;
	}

	clear() {
		this.hints = [];
	}
}

export function provideHints(initial: HintEntry[] = []): HintsState {
	const state = new HintsState(initial);
	setContext(KEY, state);
	return state;
}

export function getHintsState(): HintsState | undefined {
	return getContext<HintsState | undefined>(KEY);
}
