# Space

Laplace places everything in an S³ "ball in a box", with Unicode projected across its surface and compositions forming inside it.

## The surface

Unicode is projected across the surface of the S³. The surface projection of Unicode acts as a perimeter: every codepoint has a point on it. See [Atoms](Atoms.md).

## The interior

[Compositions](Compositions.md) form within the S³, inside the Unicode perimeter.

Tiers layer and form bands. The more complex the tier, the deeper toward the center it sits on average, and the math requires that: a composition's real coordinate is the average of its constituents' coordinates, so by the triangle inequality every composition is at least as deep as the average depth of its own constituents. The two are equal only when every constituent is the same point.

How deep a composition sits measures how concentrated its constituents are, in the sense of directional statistics: the length of the average of points on the S³ is their mean resultant length, 1 when they are all identical and approaching 0 as they spread evenly over the whole S³. Averaging more constituents moves the expected depth toward the concentration of whatever they are drawn from, so the bands of a text in one script settle toward that script's own center. See [Research: Placement](../Research/Placement.md).

## The wall

The 4D box outside the S³ is forbidden space. The codepoints are projected to the surface of the S³ as perfectly as possible, and that Unicode perimeter acts as a barrier, a cosmic wall: the math proves that nothing can ever fall outside it, and that only repeats of a single codepoint, such as `[n,n,n,n,n]`, sit exactly on the surface.

The computer proof has known computer limitations, and they do not invalidate the math. See [Research: Numerics](../Research/Numerics.md).

Knowledge can occupy the same space; matter cannot.

## Four dimensions

Everything in Laplace is 4D. See [Physicality](Physicality.md) for real coordinates and [Identity](Identity.md) for the 3D visualization of the 4D representation.

This creates the structure, shape, and form of knowledge: its physical manifestation within a finite space.
