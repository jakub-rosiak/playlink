<script lang="ts">
	interface Props {
		address: string;
		size?: number;
	}

	let { address, size = 56 }: Props = $props();

	type SigilSpec =
		| { valid: false }
		| {
				valid: true;
				shape: number; // 0..5
				symmetry: 0 | 1 | 2; // 0=v-mirror, 1=4-fold rot, 2=3-fold rot
				cells: boolean[]; // 25 entries (5x5)
				useGold: boolean;
				accent: number; // 0..15 secondary accent ring
		  };

	function parseSpec(addr: string): SigilSpec {
		if (typeof addr !== 'string') return { valid: false };
		let h = addr.toLowerCase();
		if (h.startsWith('0x')) h = h.slice(2);
		if (h.length < 12 || !/^[0-9a-f]+$/.test(h)) return { valid: false };

		// Take 12 hex chars => 6 bytes for the shape header.
		const bytes: number[] = [];
		for (let i = 0; i < h.length && bytes.length < 16; i += 2) {
			bytes.push(parseInt(h.slice(i, i + 2), 16));
		}
		// Pad to at least 16 bytes by reusing already-parsed bytes deterministically.
		while (bytes.length < 16) {
			bytes.push(bytes[bytes.length % Math.max(1, bytes.length)] ?? 0);
		}

		const shape = bytes[0] % 6;
		const symmetry = (bytes[1] % 3) as 0 | 1 | 2;
		const useGold = bytes[10] % 2 === 1;
		const accent = bytes[11] & 0x0f;

		// Build 25 cells deterministically from bytes[2..]. Spec said:
		// "(bytes[2 + i*4] >> (i % 8)) & 1". i is the cell index (0..24).
		// Then we apply symmetry to fold the result.
		const raw: boolean[] = new Array(25).fill(false);
		for (let i = 0; i < 25; i++) {
			const byteIdx = (2 + i * 4) % bytes.length;
			const bit = (bytes[byteIdx] >> (i % 8)) & 1;
			raw[i] = bit === 1;
		}

		const cells = applySymmetry(raw, symmetry);
		return { valid: true, shape, symmetry, cells, useGold, accent };
	}

	function applySymmetry(raw: boolean[], sym: 0 | 1 | 2): boolean[] {
		const grid: boolean[] = new Array(25).fill(false);
		const idx = (r: number, c: number) => r * 5 + c;

		if (sym === 0) {
			// Vertical mirror: build left half (cols 0..2) from raw, mirror to right.
			for (let r = 0; r < 5; r++) {
				for (let c = 0; c < 3; c++) {
					const v = raw[idx(r, c)];
					grid[idx(r, c)] = v;
					grid[idx(r, 4 - c)] = v;
				}
			}
		} else if (sym === 1) {
			// 4-fold rotational symmetry around the center cell (2,2).
			// Source quadrant: r=0..2, c=2..4 (upper-right inclusive of axes).
			for (let r = 0; r < 3; r++) {
				for (let c = 2; c < 5; c++) {
					const v = raw[idx(r, c)];
					// Rotate 90, 180, 270 around (2,2): (r,c) -> (c, 4-r), etc.
					const r1 = r,
						c1 = c;
					const r2 = c1,
						c2 = 4 - r1;
					const r3 = 4 - r1,
						c3 = 4 - c1;
					const r4 = 4 - c1,
						c4 = r1;
					grid[idx(r1, c1)] = v;
					grid[idx(r2, c2)] = v || grid[idx(r2, c2)];
					grid[idx(r3, c3)] = v || grid[idx(r3, c3)];
					grid[idx(r4, c4)] = v || grid[idx(r4, c4)];
				}
			}
		} else {
			// 3-fold rotational symmetry approximated on a 5x5 grid.
			// Build a base sector (top-center triangle) and project to 3 rotations of 120°.
			// Use polar mapping centered at (2,2).
			const cx = 2,
				cy = 2;
			for (let r = 0; r < 5; r++) {
				for (let c = 0; c < 5; c++) {
					const dx = c - cx;
					const dy = r - cy;
					if (dx === 0 && dy === 0) {
						grid[idx(r, c)] = raw[idx(2, 2)];
						continue;
					}
					const angle = Math.atan2(dy, dx);
					const dist = Math.round(Math.sqrt(dx * dx + dy * dy));
					// Snap angle to one of three sectors (each 120°).
					const sector = ((Math.floor(((angle + Math.PI) / (Math.PI * 2)) * 3) % 3) + 3) % 3;
					// Sample raw at a deterministic position based on dist + sector-independent slot.
					const sampleR = Math.min(4, Math.max(0, 2 - dist));
					const sampleC = Math.min(4, Math.max(0, 2));
					const baseV = raw[idx(sampleR, sampleC)];
					// Mix in another raw cell using dist so adjacent rings differ.
					const altV = raw[idx(Math.min(4, dist), Math.min(4, (sector + dist) % 5))];
					grid[idx(r, c)] = baseV !== altV; // XOR for variety, still deterministic
				}
			}
		}

		return grid;
	}

	const spec = $derived(parseSpec(address));
</script>

<div class="sigil-frame bevel-out" style="--sigil-size: {size}px;" aria-hidden="true">
	<div class="sigil-inner">
		{#if !spec.valid}
			<svg viewBox="0 0 100 100" width={size} height={size} xmlns="http://www.w3.org/2000/svg">
				<g
					stroke="var(--bone-muted)"
					stroke-width="1.4"
					fill="none"
					stroke-linejoin="miter"
					stroke-linecap="square"
				>
					<path d="M 22 18 L 78 18 L 78 52 L 74 64 L 50 88 L 26 64 L 22 52 Z" />
					<path d="M 50 34 L 60 46 L 50 58 L 40 46 Z" />
					<path
						d="M 50 42 L 51 45 L 54 46 L 51 47 L 50 50 L 49 47 L 46 46 L 49 45 Z"
						fill="var(--bone-muted)"
					/>
				</g>
			</svg>
		{:else}
			<svg
				viewBox="0 0 100 100"
				width={size}
				height={size}
				xmlns="http://www.w3.org/2000/svg"
				preserveAspectRatio="xMidYMid meet"
			>
				<rect
					x="0"
					y="0"
					width="100"
					height="100"
					fill="var(--stone-1)"
				/>

				{#each spec.cells as filled, i}
					{#if filled}
						{@const r = Math.floor(i / 5)}
						{@const c = i % 5}
						{#if spec.shape === 0}
							<!-- triangle -->
							<polygon
								points="{c * 18 + 8},{r * 18 + 22} {c * 18 + 18},{r * 18 + 22} {c * 18 +
									13},{r * 18 + 11}"
								fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}
							/>
						{:else if spec.shape === 1}
							<!-- hexagon -->
							<polygon
								points="{c * 18 + 8},{r * 18 + 16} {c * 18 + 11},{r * 18 + 11} {c * 18 +
									15},{r * 18 + 11} {c * 18 + 18},{r * 18 + 16} {c * 18 + 15},{r * 18 +
									21} {c * 18 + 11},{r * 18 + 21}"
								fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}
							/>
						{:else if spec.shape === 2}
							<!-- lozenge -->
							<polygon
								points="{c * 18 + 13},{r * 18 + 10} {c * 18 + 19},{r * 18 + 16} {c * 18 +
									13},{r * 18 + 22} {c * 18 + 7},{r * 18 + 16}"
								fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}
							/>
						{:else if spec.shape === 3}
							<!-- cross -->
							<g fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}>
								<rect x={c * 18 + 11} y={r * 18 + 10} width="4" height="12" />
								<rect x={c * 18 + 7} y={r * 18 + 14} width="12" height="4" />
							</g>
						{:else if spec.shape === 4}
							<!-- 4-point star -->
							<polygon
								points="{c * 18 + 13},{r * 18 + 9} {c * 18 + 15},{r * 18 + 15} {c * 18 +
									20},{r * 18 + 16} {c * 18 + 15},{r * 18 + 17} {c * 18 + 13},{r * 18 +
									23} {c * 18 + 11},{r * 18 + 17} {c * 18 + 6},{r * 18 + 16} {c * 18 +
									11},{r * 18 + 15}"
								fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}
							/>
						{:else}
							<!-- crescent: outer circle minus inner circle, approximated with two rects + a square gap -->
							<g fill={spec.useGold ? 'var(--gold-base)' : 'var(--bone-muted)'}>
								<rect x={c * 18 + 7} y={r * 18 + 11} width="11" height="11" />
								<rect
									x={c * 18 + 10}
									y={r * 18 + 11}
									width="9"
									height="9"
									fill="var(--stone-1)"
								/>
							</g>
						{/if}
					{/if}
				{/each}

				<!-- Subtle accent diagonal hairlines based on accent byte for added uniqueness. -->
				{#if (spec.accent & 1) === 1}
					<line
						x1="0"
						y1="0"
						x2="100"
						y2="100"
						stroke="var(--gold-faint)"
						stroke-width="0.5"
					/>
				{/if}
				{#if (spec.accent & 2) === 2}
					<line
						x1="100"
						y1="0"
						x2="0"
						y2="100"
						stroke="var(--gold-faint)"
						stroke-width="0.5"
					/>
				{/if}
				{#if (spec.accent & 4) === 4}
					<line x1="50" y1="0" x2="50" y2="100" stroke="var(--gold-faint)" stroke-width="0.5" />
				{/if}
				{#if (spec.accent & 8) === 8}
					<line x1="0" y1="50" x2="100" y2="50" stroke="var(--gold-faint)" stroke-width="0.5" />
				{/if}
			</svg>
		{/if}
	</div>
</div>

<style>
	.sigil-frame {
		display: inline-block;
		width: var(--sigil-size);
		height: var(--sigil-size);
		padding: 0;
		border-radius: 0;
		position: relative;
		line-height: 0;
		/* Inner gold glow overlay applied via box-shadow below the .bevel-out atom. */
	}

	.sigil-frame::after {
		content: '';
		position: absolute;
		inset: 0;
		pointer-events: none;
		border: 1px solid var(--stone-6);
		border-radius: 0;
		z-index: 2;
	}

	.sigil-inner {
		position: relative;
		width: 100%;
		height: 100%;
		overflow: hidden;
	}

	.sigil-inner svg {
		display: block;
		width: 100%;
		height: 100%;
	}
</style>
