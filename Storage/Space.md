# Space

Laplace places everything in a 4-ball inside a 4-cube, with Unicode projected across the 4-ball's surface, the S³, and compositions forming inside it.

## Terms

- The **4-ball**, B⁴, is the solid ball in four dimensions: every point within distance 1 of the origin.
- Its surface is the **3-sphere**, S³, also called the glome: every point at distance exactly 1.
- The **4-cube**, [−1, 1]⁴, is the box around the 4-ball.

## The surface

Unicode is projected across the surface of the S³. The surface projection of Unicode acts as a perimeter: every codepoint has a point on it. See [Atoms](Atoms.md).

## The interior

[Compositions](Compositions.md) form within the 4-ball, inside the Unicode perimeter.

Tiers layer and form bands. The more complex the tier, the deeper toward the center it sits on average, and the math requires that: a composition's real coordinate is the average of its constituents' coordinates, so by the triangle inequality every composition is at least as deep as the average depth of its own constituents. The two are equal only when every constituent is the same point.

How deep a composition sits measures how concentrated its constituents are, in the sense of directional statistics: the length of the average of points on the S³ is their mean resultant length, 1 when they are all identical and approaching 0 as they spread evenly over the whole S³. Averaging more constituents moves the expected depth toward the concentration of whatever they are drawn from, so the bands of a text in one script settle toward that script's own center. See [Research: Placement](../Research/Placement.md).

## The wall

The part of the 4-cube outside the 4-ball is forbidden space. The codepoints are projected to the surface of the S³ as perfectly as possible, and that Unicode perimeter acts as a barrier, a cosmic wall: the math proves that nothing can ever fall outside it, and that only repeats of a single codepoint, such as `[n,n,n,n,n]`, sit exactly on the surface.

The computer proof has known computer limitations, and they do not invalidate the math. See [Research: Numerics](../Research/Numerics.md).

Knowledge can occupy the same space; matter cannot.

## Four dimensions

Everything in Laplace is 4D. See [Physicality](Physicality.md) for real coordinates and [Identity](Identity.md) for the 3D visualization of the 4D representation.

This creates the structure, shape, and form of knowledge: its physical manifestation within a finite space.
