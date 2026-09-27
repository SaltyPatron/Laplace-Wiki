# Numerics

Research on the floating-point limits of Laplace's coordinates and ID points, the cost of colliding its IDs, and how trajectory distance measures treat noise and repetition.

> [!NOTE]
> Numbers marked **measured** were produced by the local research scripts `exp1_norm_guarantee.py`, `exp2_id_packing.py`, `exp3_collision_economics.py`, and `exp4_trajectory_metrics.py`. Every other number comes from the cited sources or follows from the stated formula.

## Norm at most one

The [wall](../Storage/Space.md#the-wall) is a theorem about real numbers: nothing falls outside the Unicode perimeter, and only pure repeats of one codepoint sit exactly on the S³. A computer stores the coordinates as IEEE-754 binary64 doubles, and each rounding can move a point by a fraction of an ulp in either direction. This section measures that bounded deviation and a procedure that removes it.

### What the doubles do

The codepoint points were generated with Alexa's Super-Fibonacci algorithm (see [Atoms](../Storage/Atoms.md#placement)) for N = 1,114,112, using numpy and glibc libm. **Measured:**

| Test | Points |
| --- | --- |
| Float `‖p‖ > 1` (`np.linalg.norm`) | 2,106 |
| Float `p·p > 1` (no square root) | 138,658 |
| Exact `p·p > 1` (rational arithmetic) | 557,263 (50.0%) |
| Exact `p·p == 1` | 0 |
| Exact `p·p < 1` | 556,849 |

The float norm test understates the deviation, because the final square root rounds most small overshoots back to exactly 1.0. In exact arithmetic, half the stored points lie outside the unit ball, by at most about 4.4 × 10⁻¹⁶, and none lies exactly on it.

### Floating-point tools

- **Correct rounding.** IEEE-754 `+`, `−`, `×`, `÷`, `sqrt`, and `fma` are computed exactly and rounded once, with an error of at most ½ ulp. The sign of the error is not guaranteed, which is how round-to-nearest pushes ‖p‖ above 1.
- **Directed rounding.** C99 `<fenv.h>` provides `fesetround(FE_TOWARDZERO)`. It needs `#pragma STDC FENV_ACCESS ON` and `-frounding-math` in GCC and Clang, or the compiler may fold or reorder the code. libm and BLAS ignore the mode or are not validated under it. Rounding toward zero never increases |x|. numpy and Python cannot set the mode, so the scripts emulate it with `math.nextafter`.
- **Kahan and Neumaier summation** reduce the error but leave its sign unknown.
- **`math.fsum`** (Shewchuk's algorithm) rounds a sum correctly, but the division by k that follows rounds again.
- **Shewchuk (1997)** gives exact sums and products as non-overlapping expansions (`TWO-SUM`, `FAST-TWO-SUM`, `TWO-PRODUCT`) and adaptive predicates. It yields the exact sign of `p·p − 1`: FMA splits each x² exactly into h + l, and the eight terms and −1 are summed as an expansion.
- **Ogita, Rump, and Oishi (2005)** `Sum2`, `Dot2`, and `SumK` compute as if in K-fold precision and then round. They cost about 2–3× a naive sum and are not exact, so they serve as a fast filter ahead of an exact check.
- **Neal (2015) superaccumulators** sum any number of doubles exactly and independently of order, with a 67-chunk small accumulator and a 4096-chunk large one.

## The fixed-point grid

Two procedures were designed and tested. Both enforce exact norm ≤ 1 for every stored point and every centroid.

**P1, float points with an exact fix:**

1. While the exact `p·p > 1`, move the component with the largest magnitude one ulp toward zero.
2. Compute a centroid as the exact rational Σp / k, and round each component toward zero to a double.

**P2, fixed-point grid:**

1. Store every coordinate as m · 2⁻⁵³ with integer |m| ≤ 2⁵³. Such values are exact doubles, so the columns stay `float8`. Truncate toward zero, then decrement the largest |m| while Σm² > 2¹⁰⁶; that test is exact in 128-bit integers.
2. Compute a centroid as `c_j = trunc((Σ m_j) / k)` in integer arithmetic. The sum fits a 128-bit integer for k < 2⁷⁴.

**Why both hold.** After step 1 every point has exact norm ≤ 1. By convexity, the exact centroid of such points has norm ≤ 1. Rounding each component toward zero never increases any |c_j|, so it never increases the norm. For a pure repeat, Σ = k·p exactly, so Σ / k = p, and rounding a representable value is the identity: `[n,n,…,n]` lands bit for bit on n's point.

**Measured** over 3,000 random repeats with k from 2 to 12,345, 500 repeats of points that were outside the ball, and 3,000 random compositions with k ≤ 200:

| Method | Repeats with exact norm > 1 | Repeats not equal to their own point | Compositions with norm > 1 |
| --- | --- | --- | --- |
| Naive mean (numpy, Python) | 1,501 / 3,000 | 2,185 / 3,000 | 0 |
| Kahan, Neumaier, or `fsum`, then ÷ k | 1,494 / 3,000 | 1,066 / 3,000 | 0 |
| P1, exact then round toward zero | 0 | 0 | 0 |
| P2, integer grid | 0 | 0 | 0 |

Compensated summation did not reduce the repeats outside the ball, because the input points were already outside it.

**Measured** effect of step 1 on the 1,114,112 codepoint points:

- No coordinate moved more than 4.44 × 10⁻¹⁶ (2 ulp at 1).
- P1 ulp steps per point: 0 steps for 556,849 points, 1 for 501,210, 2 for 55,477, 3 for 574, 4 for 2.
- After the fix, 1 − ‖p‖² lies between 0 and 4.4 × 10⁻¹⁶; for P2 its mean is 1.1 × 10⁻¹⁶.

**Cost.** P2 costs one 64-bit integer add per coordinate per constituent and one 128-bit integer division per coordinate, with no dependence on the platform beyond the libm used to generate the points. P1 in C needs an exact accumulator (a Shewchuk expansion or a Neal superaccumulator), then q = RZ(approx / k), then an exact residual check Σ − k·q through FMA or an expansion, with a ±1 ulp adjustment. The fix over all codepoints is a one-time step: about 23 s in pure Python.

## Deterministic builds

libm `sin` and `cos` are not required to be correctly rounded. glibc, musl, MSVC, CUDA, and others differ in the last bits, so the same codepoint can get different points on different machines. CORE-MATH provides correctly rounded functions, and its binary64 `sin` and `cos` hard-to-round cases have been fully solved. The complete codepoint table is 1,114,112 × 4 × 8 B = 35.6 MB.

Bit-for-bit identical results across hardware and operating systems require a specific build configuration:

| Setting | Why |
| --- | --- |
| Strict IEEE-754 semantics | every operation rounds exactly as specified |
| No fast-math | no reassociation, reciprocal approximation, or flushing |
| No FP contraction (`-ffp-contract=off`) | `a*b + c` is not silently fused into one rounding |
| SSE2 floating point | binary64 throughout, no x87 80-bit intermediates |
| Correctly rounded libm | `sin`, `cos`, and `sqrt` give the same bits everywhere |

## The wall is structural

For a composition `[a]*(k−1) + [b]`, where b is a's nearest neighbour (chord 0.0209), the exact gap is 1 − ‖c‖² ≈ d²(k − 1) / k². **Measured** with P2 arithmetic, for a = 12345 and b = 15049:

| k | 10³ | 10⁶ | 10⁹ | 10¹² | 10¹⁵ |
| --- | --- | --- | --- | --- | --- |
| 1 − ‖c‖² | 4.4 × 10⁻⁷ | 4.4 × 10⁻¹⁰ | 4.4 × 10⁻¹³ | 8.2 × 10⁻¹⁶ | 4.7 × 10⁻¹⁶ |

a's own point has 1 − ‖p‖² = 2.5 × 10⁻¹⁶, and across all points the value ranges from 0 to 4.4 × 10⁻¹⁶. From about k = 10¹² on, the norms of near-repeats overlap those of pure-repeat points. Whether a node sits on the wall is therefore a structural fact: a single distinct constituent, or a centroid equal bit for bit to the codepoint's point. P2 makes that bit equality exact for every true repeat.

## ID point exponent ranges

The [ID point](../Storage/Identity.md#the-id-point) fixes the exponent of X, Y, and Z. Two exponent choices were tested:

| Scheme | Sign | Biased exponent | Payload per axis | Total bits | ‖(X, Y, Z)‖ |
| --- | --- | --- | --- | --- | --- |
| A | 0 | 1023, values in [1, 2) | 43 / 43 / 42 | 128 | [√3, 2√3) = [1.732, 3.464) |
| B | 0 | 1021, values in [0.25, 0.5) | 52 | 156 | [√3/4, √3/2) = [0.433, 0.866) |
| B with sign | payload | 1021, values in ±[0.25, 0.5) | 53 | 159 | [0.433, 0.866) |

**Measured** with 200,005 BLAKE3-derived IDs plus all-zero, all-one, and alternating extremes:

- Every scheme round-trips bit for bit through `struct`, numpy `float64` arrays, and `repr()` → `float()` text.
- No scheme produced NaN, infinity, a subnormal, zero, or −0. With the sign as payload and a zero mantissa, the value is −0.25, not −0.
- Scheme A places every ID point outside the unit ball, disjoint from every real coordinate. Scheme B places ID points in the 0.433–0.866 shell, which real centroids also occupy.

Scheme A is the layout in [Identity](../Storage/Identity.md#the-id-point), with 28 bits spare.

**Measured** over 60,000 ID coordinates, arithmetic destroys the payload:

| Operation | Values changed |
| --- | --- |
| `(x * 3) / 3` | 16.9% |
| `(x + 1) − 1` | 62.6% |
| Cast to `float32` | 100% (29 bits lost) |

The same applies to PostGIS transforms, `ST_SnapToGrid`, and text output with fewer than 17 significant digits.

## Collision economics

Truncating a hash to λ bits gives λ/2 bits of collision strength (NIST SP 800-107r1 §5.1): 64 bits at 128, 78 at 156, 79.5 at 159. The full 256-bit BLAKE3 output gives 128 bits.

Generic collision search takes √(π/2 · 2ⁿ) hash evaluations. The van Oorschot–Wiener parallel search needs negligible memory, speeds up linearly with processors, and finds collisions between two chosen families of variants for about twice the work.

Inputs to the cost estimate:

- The Bitcoin network runs at about 926 EH/s (9.26 × 10²⁰ SHA-256d per second, 25 September 2026), or 2⁹⁴·⁶ hashes a year.
- hashcat on eight RTX 4090s reaches 172.1 GH/s for SHA2-256 and 100.6 GH/s for BLAKE2b. From that, about 2 × 10¹⁰ short-input BLAKE3 hashes per second per GPU is **assumed**, not measured.
- A GPU hour is **assumed** to cost $0.40.

**Computed** by `exp3_collision_economics.py`:

| ID bits | log₂ work | Bitcoin-network time | 1,000 GPUs | Cost at $0.40 per GPU hour |
| --- | --- | --- | --- | --- |
| 128 | 64.3 | 0.025 s | 13 days | about $130k |
| 156 | 78.3 | 6.8 min | 600 years | about $2B |
| 159 | 79.8 | 19 min | 1,700 years | about $6B |
| 256 | 128.3 | 1.5 × 10¹⁰ years | — | — |

Published attacks at a similar scale: SHAttered (SHA-1, 2017) took about 2⁶³·¹ SHA-1 computations, and SHA-1 is a Shambles (2020) reports a chosen-prefix collision for about US$45k of GPU rental. NIST SP 800-57 Part 1 Rev. 5 sets 112 bits as its minimum security strength, which corresponds to at least 224 bits of hash output.

Accidental collisions, from the same script:

| Stored nodes | 128 bits | 156 bits | 256 bits |
| --- | --- | --- | --- |
| 10⁹ | 1.47 × 10⁻²¹ | 5.47 × 10⁻³⁰ | 4.32 × 10⁻⁶⁰ |
| 10¹² | 1.47 × 10⁻¹⁵ | 5.47 × 10⁻²⁴ | 4.32 × 10⁻⁵⁴ |
| 10¹⁵ | 1.47 × 10⁻⁹ | 5.47 × 10⁻¹⁸ | 4.32 × 10⁻⁴⁸ |

In a content-addressed store, one ID names one content. If two different contents share an ID, whichever was recorded first is the one every later reference resolves to, and the parent hashes above it still verify.

## Trajectory measures

### Measures

| Measure | Aggregation | Cost | One outlier vertex | Repetition |
| --- | --- | --- | --- | --- |
| Continuous Fréchet (Alt–Godau) | max | O(nm log nm); no O((nm)^(1−δ)) under SETH | sets the distance | invariant to reparametrisation |
| Discrete Fréchet (Eiter–Mannila) | max | O(nm) | sets the distance | invariant to duplicated vertices |
| Weak Fréchet | max, non-monotone | O(nm log nm) | sets the distance | also allows backtracking |
| k-outlier Fréchet | max over the kept part | polynomial for fixed k | ignored, up to k vertices | — |
| Shortcut Fréchet | max, shortcuts allowed | NP-hard; approximations exist | shortcut across it | — |
| DTW | sum | O(nm) | adds its distance once | absorbed |
| EDR (Chen, Özsu, Oria) | count of ε-mismatches | O(nm) | costs one edit | costs one edit |
| LCSS (Vlachos et al.) | count of ε-matches | O(nm) | left unmatched | insertions are free |

Fréchet, continuous and discrete, is a metric; EDR is one only in a restricted sense; DTW and LCSS violate the triangle inequality, which matters for metric indexes. Work on search and indexing includes exact subtrajectory search in O(mn) for DTW, Fréchet, and others; a trit-array trie for discrete Fréchet at scale; the N-tree metric index for exact kNN and range queries; and translation-invariant subtrajectory Fréchet queries. Reviews of elastic measures compare these and others.

### Experiment

Trajectory A is 60 random codepoint points on the S³, with a median consecutive chord of 1.30. The ground distance is the R⁴ chord, and ε = 0.1 for EDR and LCSS. In the jittered case every vertex moves about 0.04, as log lines do when they differ only in timestamps or IDs. **Measured:**

| B compared with A | cFr | dFr | weak | 1-outlier dFr | DTW | DTW / length | EDR | 1 − LCSS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Identical | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| One outlier vertex | 1.01 | 1.39 | 1.03 | 0.00 | 1.90 | 0.032 | 0.017 | 0.017 |
| Five outliers | 1.21 | 1.47 | 1.38 | 1.28 | 7.25 | 0.121 | 0.083 | 0.083 |
| Stutter (one vertex twice) | 0 | 0 | 0 | 0 | 0 | 0 | 0.016 | 0 |
| Repeated 10-vertex segment | 1.24 | 1.47 | 1.33 | 1.39 | 11.5 | 0.165 | 0.143 | 0 |
| Every vertex jittered | 0.087 | 0.087 | 0.087 | 0.076 | 2.47 | 0.041 | 0 | 0 |
| Unrelated sequence | 1.72 | 1.72 | 1.72 | 1.72 | 69.8 | 1.03 | 1.00 | 1.00 |

Observations:

- Max-based Fréchet puts one bad vertex close to an unrelated sequence: 1.39 against 1.72, discrete.
- Every Fréchet and DTW variant gives 0 for stutter: `[a,b,b,c]` and `[a,b,c]` are equal to them. Only EDR registers the repeat. In Laplace the repeat is still in the ID, because the hash covers the full child list ([Hashing](Hashing.md#the-cve-2012-2459-lesson)).
- LCSS gives 0 for an inserted repeated segment; EDR and DTW register it.
- Under jitter, Fréchet reports the noise amplitude (0.087), and EDR and LCSS with ε above the noise give 0.
- The 1-outlier Fréchet removes a single outlier entirely (0.00).

[Geometry](Geometry.md) covers Fréchet in 4D and in PostGIS.

## Sources

- [Shewchuk, "Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates", CMU-CS-96-140](http://www.cs.cmu.edu/afs/cs/project/quake/public/papers/robust-arithmetic.ps); published version in [Discrete & Computational Geometry 18](https://link.springer.com/article/10.1007/PL00009321).
- [Ogita, Rump, Oishi, "Accurate Sum and Dot Product", SISC 26(6)](https://www.tuhh.de/ti3/paper/rump/OgRuOi05.pdf).
- [Neal, "Fast exact summation using small and large superaccumulators", arXiv:1505.05571](https://arxiv.org/abs/1505.05571).
- [CORE-MATH](https://core-math.gitlabpages.inria.fr/).
- [BLAKE3 specification](https://github.com/BLAKE3-team/BLAKE3-specs/raw/master/blake3.pdf).
- [NIST SP 800-107 Rev. 1, hash truncation](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-107r1.pdf).
- [NIST SP 800-57 Part 1 Rev. 5](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf).
- [van Oorschot and Wiener, "Parallel Collision Search with Cryptanalytic Applications", J. Cryptology 12](https://people.scs.carleton.ca/~paulv/papers/JoC97.pdf).
- [Stevens et al., "The first collision for full SHA-1" (SHAttered)](https://www.shattered.io/static/shattered.pdf).
- [Leurent and Peyrin, "SHA-1 is a Shambles"](https://eprint.iacr.org/2020/014.pdf).
- [CoinWarz Bitcoin hashrate](https://www.coinwarz.com/bitcoin-hashrate) and [Cryptolexicon, September 2026 difficulty](https://cryptolexicon.org/en/blog/bitcoin-difficulty-rise-hashprice-jump-september-2026/).
- [hashcat benchmark, NVIDIA RTX 4090](https://www.onlinehashcrack.com/tools-benchmark-hashcat-nvidia-rtx-4090.php).
- [Bringmann, "Why walking the dog takes time", arXiv:1404.1448](https://arxiv.org/abs/1404.1448).
- [k-outlier Fréchet distance, arXiv:2202.12824](https://arxiv.org/abs/2202.12824).
- [Driemel and Har-Peled, "Jaywalking your dog", arXiv:1107.1720](https://arxiv.org/abs/1107.1720).
- [Shortcut Fréchet distance is NP-hard, arXiv:1307.2097](https://arxiv.org/abs/1307.2097).
- [Chen, Özsu, Oria, "Robust and Fast Similarity Search for Moving Object Trajectories", SIGMOD 2005](https://dl.acm.org/doi/10.1145/1066157.1066213).
- [Non-learning subtrajectory search, arXiv:2307.10082](https://arxiv.org/abs/2307.10082).
- [Trit-array trie for discrete Fréchet, arXiv:2005.10917](https://arxiv.org/abs/2005.10917).
- [N-tree exact trajectory search, arXiv:2408.07650](https://arxiv.org/abs/2408.07650).
- [Translation-invariant subtrajectory Fréchet queries, arXiv:2102.05844](https://arxiv.org/abs/2102.05844).
- [Time-series similarity evaluation, arXiv:1401.3973](https://arxiv.org/abs/1401.3973).
- [Review of elastic distances, arXiv:2205.15181](https://arxiv.org/abs/2205.15181).
