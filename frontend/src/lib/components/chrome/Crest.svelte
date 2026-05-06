<script lang="ts">
	interface Props {
		size?: number;
		tone?: 'gold' | 'bone' | 'iron';
	}

	let { size = 96, tone = 'gold' }: Props = $props();
</script>

<span
	class="crest tone-{tone}"
	style="--crest-size: {size}px;"
	aria-hidden="true"
	role="presentation"
>
	<svg
		viewBox="0 0 100 100"
		width={size}
		height={size}
		xmlns="http://www.w3.org/2000/svg"
		preserveAspectRatio="xMidYMid meet"
	>
		<g stroke="currentColor" stroke-width="1.4" fill="none" stroke-linejoin="miter" stroke-linecap="square">
			<!-- Outer shield silhouette: sharp polygons, no curves. -->
			<path d="M 18 14 L 82 14 L 82 50 L 78 64 L 50 92 L 22 64 L 18 50 Z" />

			<!-- Inner shield border (6px inset). -->
			<path d="M 24 20 L 76 20 L 76 50 L 72.5 61 L 50 84 L 27.5 61 L 24 50 Z" />

			<!-- Top stud rivets (3 across the top edge). -->
			<circle cx="26" cy="17" r="1.2" fill="currentColor" />
			<circle cx="50" cy="17" r="1.2" fill="currentColor" />
			<circle cx="74" cy="17" r="1.2" fill="currentColor" />

			<!-- Side stud rivets at hip points. -->
			<circle cx="20" cy="50" r="1" fill="currentColor" />
			<circle cx="80" cy="50" r="1" fill="currentColor" />

			<!-- Top hairline divider just under the rivets. -->
			<path d="M 28 24 L 72 24" stroke-width="0.8" />

			<!-- Celtic 4-fold knotwork in the center. Square framework, lines weave. -->
			<!-- Outer knot diamond. -->
			<path d="M 50 32 L 64 46 L 50 60 L 36 46 Z" />
			<!-- Inner small diamond. -->
			<path d="M 50 38 L 58 46 L 50 54 L 42 46 Z" />

			<!-- Knot weave arms (4-fold). Top arm. -->
			<path d="M 50 32 L 50 38" />
			<!-- Bottom arm. -->
			<path d="M 50 54 L 50 60" />
			<!-- Left arm. -->
			<path d="M 36 46 L 42 46" />
			<!-- Right arm. -->
			<path d="M 58 46 L 64 46" />

			<!-- Diagonal interlace strokes (X) inside the inner diamond, breaks at center for weave look. -->
			<path d="M 44 40 L 48 44" />
			<path d="M 52 44 L 56 40" />
			<path d="M 44 52 L 48 48" />
			<path d="M 52 48 L 56 52" />

			<!-- Center 4-pointed compass star pip. -->
			<path d="M 50 44 L 51 46 L 53 47 L 51 48 L 50 50 L 49 48 L 47 47 L 49 46 Z" fill="currentColor" />

			<!-- Lower decorative chevron above the tip. -->
			<path d="M 38 70 L 50 76 L 62 70" stroke-width="1.1" />
			<path d="M 42 66 L 50 70 L 58 66" stroke-width="0.8" />

			<!-- Hairline arcs framing the upper field (kept as straight chords, no curves). -->
			<path d="M 30 30 L 36 26 L 64 26 L 70 30" stroke-width="0.8" />
		</g>
	</svg>
</span>

<style>
	.crest {
		display: inline-block;
		width: var(--crest-size);
		height: var(--crest-size);
		line-height: 0;
	}

	.crest svg {
		display: block;
	}

	.tone-gold {
		color: var(--gold-base);
		filter: drop-shadow(0 0 6px rgba(227, 188, 116, 0.45))
			drop-shadow(0 1px 0 rgba(0, 0, 0, 0.7));
	}

	.tone-bone {
		color: var(--bone-muted);
		filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.7));
	}

	.tone-iron {
		color: var(--stone-7);
		filter: drop-shadow(0 1px 0 rgba(0, 0, 0, 0.85));
	}
</style>
