# 4. Projection

Every codepoint gets its point on the S³: the DUCET order, the Super-Fibonacci points, the Hilbert order, and rank r to the r-th point.

Laplace places everything in a 4-ball inside a 4-cube, with Unicode projected across the 4-ball's surface, the S³, and compositions forming inside it. Nothing above tier 0 has a coordinate until this exists, because every composition's coordinate is computed up from the codepoint leaves.

## Before this stage

[1. Unicode](Unicode.md): the collation elements, decompositions, and codespace. [3. Builds](Builds.md): the deterministic arithmetic and the correctly rounded `sin` and `cos`.

## The space

- The **4-ball**, B⁴, is the solid ball in four dimensions: every point within distance 1 of the origin.
- Its surface is the **3-sphere**, S³, also called the glome: every point at distance exactly 1.
- The **4-cube**, [−1, 1]⁴, is the box around the 4-ball.

The part of the 4-cube outside the 4-ball is forbidden space. The codepoints are projected to the surface of the S³ as perfectly as possible, and that Unicode perimeter acts as a barrier, a cosmic wall: the math proves that nothing can ever fall outside it, and that only repeats of a single codepoint sit exactly on the surface. See [Space](../Storage/Space.md).

## Operations: the order

### 4.1 Give every codepoint its collation elements

- **In:** `allkeys.txt` and the decompositions from [1. Unicode](Unicode.md).
- **Do:** for each of the 1,114,112 codepoints, one of three:
  - the explicit single entry, for 38,785 codepoints;
  - for the 11,172 Hangul syllables, which have no entries, the NFD decomposition to conjoining jamo, which do;
  - the implicit pair `[.AAAA.0020.0002][.BBBB.0000.0000]` for everything else, by class: Tangut `FB00`, Tangut Components `FB01`, Nushu `FB02`, Khitan Small Script `FB03`, each with `BBBB` counted from the main block's start; Core Han `FB40 + (CP >> 15)`; Other Han `FB80 + (CP >> 15)`; unassigned, private use, noncharacters, and surrogates `FBC0 + (CP >> 15)`; each with `BBBB = (CP & 7FFF) | 8000`. The Tangut, Nushu, and Khitan ranges apply to assigned codepoints only; unassigned codepoints in those blocks take `FBC0` and up. Surrogates get implicit weights as if unassigned and are never ignorable or variable.
- **Out:** collation elements for all 1,114,112 codepoints.
- **Check:** the counts: 38,785 explicit, 11,172 Hangul, 7,925 Tangut/Nushu/Khitan, 20,992 Core Han, 80,992 Other Han, 954,246 `FBC0` and up. A supplement block shares its base `AAAA` with the main block and counts `BBBB` from the main block's start, so Tangut Supplement sorts after all of Tangut; counting from the supplement's own start is the bug the prototype had until the collation conformance test exposed it.
- **Mechanism:** `laplace tier0`: the explicit entries of `allkeys.txt`, Hangul by NFD, implicit weights by block ([CLI: laplace tier0](../Reference/CLI.md#laplace-tier0)). Status: **built**.
- **From:** [Research: Unicode: Implicit weights](../Research/Unicode.md#implicit-weights), [Research: Unicode: How every codepoint gets weights](../Research/Unicode.md#how-every-codepoint-gets-weights).

### 4.2 Form the sort key

- **In:** the collation elements of 4.1.
- **Do:** use non-ignorable variable weighting: `*` weights are used as-is. Under the default shifted setting the 8,496 variable characters would collapse at levels 1–3. Form the UCA sort key L1 | L2 | L3 from the non-zero weights.
- **Out:** one sort key per codepoint.
- **Check:** 1,109,207 distinct sort keys; 1,419 tie groups covering 6,324 codepoints remain, the largest being the 962 completely ignorable codepoints.
- **Mechanism:** `laplace tier0`: `qsort` over the non-ignorable L1, L2, L3 key ([CLI: laplace tier0](../Reference/CLI.md#laplace-tier0)). Status: **built**.
- **From:** [Research: Unicode: The deterministic total order](../Research/Unicode.md#the-deterministic-total-order).

### 4.3 Break the ties

- **In:** the sort keys of 4.2 and the decompositions of [1. Unicode](Unicode.md).
- **Do:** break ties first by the identical level, the codepoint's canonical decomposition, then by codepoint, the deterministic comparison of UTS #10 Appendix A. The identical level alone is not enough for single codepoints, because canonical singletons such as U+212B and U+00C5 still tie. Skipping it misorders pairs such as U+2001 EM QUAD, whose NFD is U+2003, against U+2002 EN SPACE.
- **Out:** one deterministic total order of all 1,114,112 codepoints, and each codepoint's rank in it.
- **Check:** U+0000 is rank 0; the first non-ignorable codepoint is at rank 1,640; U+0020 at 1,648; `a` at 12,142; `A` at 12,159; U+AC00 at 25,261; U+4E00 at 56,415; U+D800 at 161,100; U+E000 at 163,148; U+FFFE at 169,681; U+10FFFF at 1,114,110; the last codepoint is U+FFFD, whose fixed primary sorts above all implicit weights. The SHA-256 of the order, written as 3-byte big-endian codepoints, is `31548536a65d75e4f4e3f866d4bb5315ddbfe803edb7d0a018eebfb5c89257e0`. An earlier order without the identical level and with the Tangut supplement bug hashed to `85474f71…` and is superseded.
- **Mechanism:** `laplace tier0`: ties by NFD, then by codepoint; the rank goes into the record's `rank` field ([Formats: The tier-0 record](../Reference/Formats.md#the-tier-0-record)). Status: **built**.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Unicode: The deterministic total order](../Research/Unicode.md#the-deterministic-total-order).

## Operations: the points

### 4.4 Generate the Super-Fibonacci points

- **In:** n = 1,114,112.
- **Do:** Marc Alexa's Super-Fibonacci spiral, Algorithm 1, with φ = √2 and ψ the positive real root of ψ⁴ = ψ + 4, ψ = 1.533751168755204288118041…:

  ```text
  for i in 0 .. n-1:
      s = i + 1/2
      t = s / n
      r = sqrt(t),  R = sqrt(1 - t)
      alpha = 2*pi*s / phi,  beta = 2*pi*s / psi
      q[i] = (r sin alpha, r cos alpha, R sin beta, R cos beta)
  ```

  Every coordinate depends on t = (i + ½)/n, so n is fixed in advance: point *i* of the *n*-point set is not point *i* of any other set. The official repository retracts the paper's refinement claim: measured, no point of an *n*-point set coincides with a point of a *kn*-point set. With n fixed at the size of the codespace, every point is permanent. Each point depends only on (*i*, *n*), so points are generated independently and in parallel, with the correctly rounded `sin` and `cos` of [2. Toolchain](Toolchain.md).
- **Out:** 1,114,112 points on the S³.
- **Check:** all norms equal 1 to within 2.2 × 10⁻¹⁶; the centroid of the full set has norm about 10⁻⁶; minimum nearest-neighbor distance 0.012734, mean 0.019937, maximum 0.026053; that many independent random points would have a minimum about 60 times smaller.
- **Mechanism:** `laplace tier0`: Algorithm 1 in the reference's operation order with `cr_sin` and `cr_cos` from `lp_crmath` ([CLI: laplace tier0](../Reference/CLI.md#laplace-tier0), [Build: Targets](../Reference/Build.md#targets)). Status: **built**.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Sampling: Super-Fibonacci spirals](../Research/Sampling.md#super-fibonacci-spirals), [Research: Sampling: Numeric checks](../Research/Sampling.md#numeric-checks).

### 4.5 Compute each point's Hilbert value

- **In:** the points of 4.4.
- **Do:** the Hilbert curve fills the 4-cube [−1, 1]⁴, and the points on the S³ are that curve filtered to the S³. Quantize each axis to 16 bits and compute the value with Skilling's transpose algorithm: one Gray code over all n·p bits and a single undo pass, in O(n·p) time with no tables. Once branches became masks and the bit interleave became `pdep`, the native kernel fell from 227 ns to 83 ns per value.
- **Out:** one Hilbert value per point.
- **Mechanism:** `lp_hilbert4`: 16-bit grid, Skilling's transpose, `pdep` on x86-64-v3 ([Formats: The Hilbert value](../Reference/Formats.md#the-hilbert-value), [Native: Coordinates](../Reference/Native.md#coordinates-coordc)). Status: **built**.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Placement: The placement](../Research/Placement.md#the-placement), [Research: Geometry: Hilbert curves](../Research/Geometry.md#hilbert-curves), [Research: Engine Measurements: Native operations](../Research/Engine.md#native-operations).

### 4.6 Sort the points by Hilbert value

- **In:** the points and values of 4.5.
- **Do:** sort. The sorted list is a walk over the S³ along the Hilbert curve. A Hilbert curve is a space-filling curve: points that are close along the curve are close in space. This replaces the spiral's visiting order, which carries no locality, with the curve's, while the points themselves remain the evenly spread Super-Fibonacci set. The spiral index scatters because each step from index *i* to *i* + 1 turns α by 360°/√2 ≈ 254.6° and β by 360°/ψ ≈ 234.7°, so consecutive indices land on nearly opposite sides of both circles, a median 1.686 apart, farther than two random points at about 1.36.
- **Out:** the points in Hilbert order.
- **Mechanism:** `laplace tier0` walks the points in Hilbert order ([CLI: laplace tier0](../Reference/CLI.md#laplace-tier0)). Status: **built**.
- **From:** [Research: Placement: Why the spiral index scatters](../Research/Placement.md#why-the-spiral-index-scatters), [Research: Placement: Why Hilbert order fixes it](../Research/Placement.md#why-hilbert-order-fixes-it).

### 4.7 Give rank r the r-th point

- **In:** the order of 4.3 and the sorted points of 4.6.
- **Do:** DUCET rank *r* takes the *r*-th point of the walk. Rank and point are both fixed by the Unicode version, and IDs are not derived from either.
- **Out:** one point on the S³ for every codepoint. The monorepo states the placement as the open radical-inverse law with no fixed n; that difference is [30. Conflicts](Conflicts.md) P1.
- **Check:** collation neighbors are spatial neighbors. The median distance between consecutive DUCET ranks is 0.026, against 1.686 under the plain spiral index; the mean nearest-neighbor distance of the full set is 0.0199. Case, width, and style variants of one letter are consecutive ranks, so `a`, `ａ`, `𝐚`, `ⓐ`, and `A` are consecutive points; the mean pairwise distance within `A a ä á à â å ã ā` is 0.086, at most 0.142. Word centroids inherit it: `King` to `king` 0.023, `king` to `ding` 0.105, `ding` to `dong` 0.079, `dong` to `kong` 0.105; from `king`: `ring` 0.049, `sing` 0.049, `kong` 0.079, `cat` 0.238, `猫` 0.651. The placement is not exact, but it is predictable and recordable.
- **Mechanism:** `laplace tier0` writes rank *r*'s point into codepoint's record; `rank` and `m[4]` in the record ([Formats: The tier-0 record](../Reference/Formats.md#the-tier-0-record)). Status: **built**.
- **From:** [Atoms: Placement](../Storage/Atoms.md#placement), [Research: Placement: Variants compared](../Research/Placement.md#variants-compared), [Research: Placement: Words under H1](../Research/Placement.md#words-under-h1).

## What the interior will do with these points

Compositions form within the 4-ball, inside the Unicode perimeter. Tiers layer and form bands. The more complex the tier, the deeper toward the center it sits on average, and the math requires that: a composition's real coordinate is the average of its constituents' coordinates, so by the triangle inequality every composition is at least as deep as the average depth of its own constituents. The two are equal only when every constituent is the same point. How deep a composition sits measures how concentrated its constituents are: the length of the average of points on the S³ is their mean resultant length, 1 when they are all identical and approaching 0 as they spread evenly. For *k* independent uniform points the RMS centroid norm is 1/√*k*; for *k* spatial nearest neighbors in this set the mean norm stays above 0.998 up to *k* = 100. See [Space: The interior](../Storage/Space.md#the-interior) and [Research: Sampling: Centroids](../Research/Sampling.md#centroids).

## What this stage leaves behind

One point on the S³ for every codepoint, the same on every install that started from the same Unicode version, and the wall around everything that will ever be composed. Between Unicode versions only the points move; the IDs do not.

## Without this stage

There is no surface, no wall, and no place for a composition to fall inward from. Every coordinate above tier 0 is computed from these.
