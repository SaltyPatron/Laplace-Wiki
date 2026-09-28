# Placement

Codepoints are placed on the S³ by taking Marc Alexa's Super-Fibonacci points for n = 1,114,112 in the order of their 4D Hilbert value and giving DUCET rank *r* the *r*-th point, which puts collation neighbors next to each other in space.

This page records the measurements behind the placement described in [Atoms](../Storage/Atoms.md#placement). The point set is described in [Sampling](Sampling.md), and the DUCET order in [Unicode](Unicode.md#the-deterministic-total-order).

> [!NOTE]
> Every number on this page marked *measured* was produced by the local placement research scripts against the Unicode 17.0.0 data. Distances are Euclidean (chordal) distances in R⁴ between unit vectors. Two random points on the S³ are on average about 1.36 apart; the largest possible distance is 2.0.

## Inputs

- **The codespace.** All 1,114,112 codepoints, U+0000 to U+10FFFF, are placed, including unassigned, private-use, surrogate, and noncharacter codepoints. The scope is never reduced to the assigned repertoire.
- **The order.** The deterministic DUCET total order of all 1,114,112 codepoints, built from the Unicode 17.0.0 `allkeys.txt`: explicit entries, Hangul syllables through their jamo, `@implicitweights`, and the catch-all implicit weights; the sort key is L1, L2, L3 with non-ignorable variable weighting, and ties are broken by codepoint. See [Unicode](Unicode.md#the-deterministic-total-order).
- **The points.** One Super-Fibonacci set with n = 1,114,112, fixed once. See [Sampling](Sampling.md#super-fibonacci-spirals).

## The placement

1. Generate the 1,114,112 Super-Fibonacci points.
2. Compute each point's Hilbert value: the Hilbert curve fills the 4-cube $[-1, 1]^4$, and the points on the S³ are that curve filtered to the S³. The measured runs quantize each axis to 16 bits and use Skilling's transpose algorithm.
3. Sort the points by Hilbert value. The sorted list is a walk over the S³ along the Hilbert curve.
4. Give DUCET rank *r* the *r*-th point of that walk.

Rank and point are both fixed by the Unicode version, and IDs are not derived from either. Between Unicode versions only the points move; the IDs do not. See [Atoms](../Storage/Atoms.md#unicode-versions).

## Why the spiral index scatters

Super-Fibonacci point *i* has $s = i + \tfrac12$, $t = s/n$, and the two angles $\alpha = 2\pi s/\varphi$ and $\beta = 2\pi s/\psi$, with $\varphi = \sqrt2$ and $\psi \approx 1.5337511688$. Each step from index *i* to *i* + 1 therefore advances $\alpha$ by $360°/\sqrt2 \approx 254.6°$ and $\beta$ by $360°/\psi \approx 234.7°$, while *t* barely changes. Those are large irrational rotations: consecutive indices land on nearly opposite sides of both circles.

Measured over the full set, the median distance between consecutive Super-Fibonacci indices is 1.686, farther apart than two random points (about 1.36). Placing DUCET rank *r* at spiral index *r* therefore sends collation neighbors far apart. The spiral index is what makes the set well spread; it carries no spatial locality.

## Why Hilbert order fixes it

A Hilbert curve is a space-filling curve: points that are close along the curve are close in space. Sorting the Super-Fibonacci points by Hilbert value replaces the spiral's visiting order with the curve's, so consecutive positions in the sorted list are spatial neighbors, while the points themselves remain the evenly spread Super-Fibonacci set.

DUCET rank then maps onto that list. Ranks that are adjacent in collation are adjacent along the curve, and so adjacent on the S³. Measured, the median distance between consecutive DUCET ranks is 0.026 under H1, against 1.686 under the plain spiral index. For scale, the measured mean nearest-neighbor distance of the full 1,114,112-point set is 0.0199 (see [Sampling](Sampling.md#numeric-checks)).

## DUCET neighbors of `a`

The DUCET order around `a`, measured from the Unicode 17.0.0 data:

| Rank | Codepoint | Character | Name |
| --- | --- | --- | --- |
| 12142 | U+0061 | a | LATIN SMALL LETTER A |
| 12143 | U+FF41 | ａ | FULLWIDTH LATIN SMALL LETTER A |
| 12144 | U+0363 | ◌ͣ | COMBINING LATIN SMALL LETTER A |
| 12145 | U+1D41A | 𝐚 | MATHEMATICAL BOLD SMALL A |
| 12146–12157 | U+1D44E … U+1D68A | 𝑎 𝒂 𝒶 𝓪 𝔞 𝕒 𝖆 𝖺 𝗮 𝘢 𝙖 𝚊 | the other mathematical small a |
| 12158 | U+24D0 | ⓐ | CIRCLED LATIN SMALL LETTER A |
| 12159 | U+0041 | A | LATIN CAPITAL LETTER A |
| 12160 | U+FF21 | Ａ | FULLWIDTH LATIN CAPITAL LETTER A |

Case, width, and style variants of one letter are consecutive ranks. Under H1 they are consecutive points along the Hilbert curve.

## Variants compared

All five variants place the same 1,114,112 Super-Fibonacci points in the same DUCET order; they differ only in how rank maps to a point. All values are measured.

| Placement | Consecutive ranks (median) | A-family mean | k–K | king–King | king–ring |
| --- | --- | --- | --- | --- | --- |
| Rank → spiral index, bit-reversed | 1.686 | 1.366 | 1.956 | 0.489 | 0.337 |
| Rank → spiral index, no reversal | 1.764 | 1.152 | 0.518 | 0.130 | 0.372 |
| DUCET primary-weight groups, clustered | – | 0.004 | 0.003 | 0.001 | 0.432 |
| **H1: points in 4D Hilbert order, rank *r* → *r*-th point** | **0.026** | **0.086** | **0.093** | **0.023** | **0.049** |
| H2: as H1, first 159,866 ranks spread along the whole curve | 0.059 | 0.236 | 0.099 | 0.025 | 0.074 |

- **A-family** is the mean pairwise distance within `A a ä á à â å ã ā`. Under H1 its maximum is 0.142.
- **Word distances** are distances between word centroids: the unweighted mean of the letters' points.
- **Rank → spiral index, bit-reversed** visits the spiral in base-2 radical-inverse order (21-bit reversal, skipping values ≥ n). See [Sampling](Sampling.md#radical-inverse-ordering).
- **Rank → spiral index, no reversal** uses the rank directly as the spiral index.
- **Primary-weight groups** give each distinct DUCET primary weight one Super-Fibonacci center, in radical-inverse order, and pack the group's members on a small sphere around it. Case and accent variants almost coincide, but different base letters are no closer than random.
- **H2** is H1 with the first 159,866 DUCET ranks placed at evenly spaced positions along the whole curve and the remaining ranks filling the gaps.

Measured nearest-neighbor spacing of the first 159,866 DUCET ranks: H1 min 0.01273, mean 0.0201; H2 min 0.01274, mean 0.0315. A fresh Super-Fibonacci set of that size has mean about 0.042.

## Words under H1

Measured, with each word at its centroid.

A chain of one-letter edits:

| Step | Distance |
| --- | --- |
| King → king | 0.023 |
| king → ding | 0.105 |
| ding → dong | 0.079 |
| dong → kong | 0.105 |

Distance from `king`:

| Word | Distance |
| --- | --- |
| ring | 0.049 |
| sing | 0.049 |
| dong | 0.070 |
| kong | 0.079 |
| Kong | 0.090 |
| ding | 0.105 |
| zebu | 0.148 |
| tree | 0.162 |
| кошка | 0.186 |
| cat | 0.238 |
| 猫 | 0.651 |

For scale, 3,000 pairs of random four-letter lowercase words have a measured mean distance of 0.163, with a 5th percentile of 0.051.

## Sources

- Marc Alexa, [Super-Fibonacci Spirals: Fast, Low-Discrepancy Sampling of SO(3)](https://openaccess.thecvf.com/content/CVPR2022/papers/Alexa_Super-Fibonacci_Spirals_Fast_Low-Discrepancy_Sampling_of_SO3_CVPR_2022_paper.pdf), CVPR 2022, and the [reference implementation](https://github.com/marcalexa/superfibonacci).
- John Skilling, [Programming the Hilbert curve](https://doi.org/10.1063/1.1751381), AIP Conference Proceedings 707, 2004.
- Unicode Technical Standard #10, [Unicode Collation Algorithm](https://www.unicode.org/reports/tr10/tr10-53.html), revision 53, Unicode 17.0.0.
- [Wikipedia: Van der Corput sequence](https://en.wikipedia.org/wiki/Van_der_Corput_sequence), for the radical inverse.
