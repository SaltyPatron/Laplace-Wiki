# Sampling

Super-Fibonacci spirals give a fixed-size, evenly spread set of points on the S³, and this page records their construction, their relation to the Hopf fibration and to incremental grids, radical-inverse ordering, and local numeric checks.

This is the background for the point set used by [Placement](Placement.md). The S³ is the unit 3-sphere in R⁴, the set of unit quaternions. See [Space](../Storage/Space.md).

> [!NOTE]
> Numbers marked *measured* come from the local sampling check script (Algorithm 1 with $\varphi = \sqrt2$, $\psi = 1.5337511687552043$; nearest neighbors found with a k-d tree). Distances are Euclidean (chordal) distances in R⁴; at these scales chord and geodesic angle agree closely. All other numbers are from the cited sources.

## Super-Fibonacci spirals

Marc Alexa, CVPR 2022.

### Construction

The paper maps a cylinder onto the S³ with a volume-preserving map (Claim 1, eq. 3):

$$x(h, y) = \left(z \cos h,\ z \sin h,\ y_0,\ y_1\right), \quad z = \sqrt{1 - y^\top y}$$

with $h \in (-\pi, \pi]$ and $y$ in the unit disk. Its Jacobian determinant is 1, so equal volumes on the cylinder are equal volumes on the S³. One-dimensional Fibonacci sampling along the axis and two-dimensional Fibonacci disk sampling, lifted through this map, give Algorithm 1:

```text
for i in 0 .. n-1:
    s = i + 1/2
    t = s / n
    r = sqrt(t),  R = sqrt(1 - t)
    alpha = 2*pi*s / phi,  beta = 2*pi*s / psi
    q[i] = (r sin alpha, r cos alpha, R sin beta, R cos beta)
```

- **Constants (eq. 10–11).** $\varphi = \sqrt2$, and $\psi$ is the positive real root of $\psi^4 = \psi + 4$, $\psi = 1.533751168755204288118041\ldots$
- **How they were chosen.** The first candidate, which gave the method its name, was the golden and supergolden ratios. A search over roots of small integer polynomials (supplement §D) found the pair $(\sqrt2, \psi)$ slightly better. The two constants must be irrational and not rational multiples of each other. They were tuned only up to n ≈ 10⁵; the paper notes that for larger sample sizes different constants may be more suitable.
- **Cost.** O(1) per point: two square roots and two sine–cosine pairs. Each point depends only on (*i*, *n*), so points can be generated independently and in parallel.

### S³ and SO(3)

The algorithm samples all of the S³. For rotations, *q* and −*q* are the same element of SO(3), and the paper measures distance as $\arccos\lvert\langle p, q\rangle\rvert$ (eq. 12). Laplace uses the S³ itself, so no antipodal identification applies: the points are simply n well-spread points on the S³.

### Reported quality

- **Spherical-cap discrepancy (Fig. 2).** Super-Fibonacci and SOI-optimized sets have at least an order of magnitude lower discrepancy than the other methods compared, across all sample sizes. At n ≈ 10⁶ the plot shows about 10⁻³.
- **Radial distribution (Fig. 3).** No pairs at small distances; the variation decays quickly at larger distances.
- **Voronoi volumes (Fig. 4).** A narrow peak: cells are nearly equal in volume, which the paper attributes to the volume-preserving map.
- **Limitations (§5, supplement §C).** The covering radius is worse than SOI-optimized sets and better than Hopf-fibration grids. The largest empty regions are at the start and end of the sequence, where *t* approaches 0 or 1. There is no theory linking the constants to the resulting discrepancy.

### Fixed n

Every coordinate depends on $t = (i + \tfrac12)/n$, so *n* is fixed in advance: point *i* of the *n*-point set is not point *i* of the (*n*+1)-point set. It is a point set, not an incremental sequence. With *n* fixed at 1,114,112, the size of the Unicode codespace, every point is permanent.

> [!WARNING]
> The paper claims that a set of *kn* samples contains the set of *n* samples. The official repository's README retracts this: Super-Fibonacci spirals have no simple refinement property. Measured: for (n, k) = (1000, 2), (1000, 3), and (997, 5), no point of the *n*-point set coincides with a point of the *kn*-point set, and the largest distance to the nearest point is 0.12–0.17.

## The Hopf fibration

The Hopf map sends the S³ to the S², and each fiber is a great circle; any two fibers are linked once. In quaternion form (Lyons, eq. 1):

$$h(a, b, c, d) = \left(a^2 + b^2 - c^2 - d^2,\ 2(ad + bc),\ 2(bd - ac)\right)$$

Applied to a Super-Fibonacci point $(r \sin\alpha, r\cos\alpha, R\sin\beta, R\cos\beta)$, the first component is $t - (1 - t) = 2t - 1$. Since *t* is uniform in the index, the height on the S² is uniform in [−1, 1], which is uniform on the S² by Archimedes' theorem. The base longitude is $\alpha + \beta$ and the fiber angle is $\alpha - \beta$ (the signs depend on the chosen Hopf map). The Hopf projection of a Super-Fibonacci set is therefore a spherical-Fibonacci-type spiral on the S². This derivation comes from the local research notes, not from a source.

For viewing the S³ in three dimensions:

- **Stereographic projection** $(x_0, x_1, x_2, x_3) \mapsto (x_0, x_1, x_2)/(1 - x_3)$ is conformal and maps great circles to circles. Hopf fibers over a circle of latitude on the S² fill a torus in R³, and the fibers over the whole S² fill R³ as nested tori.
- **Level sets.** Super-Fibonacci level sets *t* = const are the tori $\lvert z_0\rvert^2 = t$, preimages of latitude circles. A contiguous index range fills a solid torus shell, the preimage of a latitude band.
- **The Clifford torus** $x_0^2 + x_1^2 = x_2^2 + x_3^2 = \tfrac12$ is *t* = ½. It is intrinsically flat, and Alexa uses it for aliasing plots.

## Incremental Hopf grids

Yershova, Jain, LaValle, and Mitchell (IJRR 2010) build a deterministic, incremental grid on SO(3) from Hopf coordinates.

- **Hopf coordinates (eq. 4).** θ ∈ [0, π] and φ ∈ [0, 2π) on the base S², ψ on the fiber S¹. With ψ ∈ [0, 2π) they cover half of the S³, which is enough for SO(3); extending ψ to [0, 4π) covers all of the S³.
- **Volume element (eq. 5).** $dV = \tfrac18 \sin\theta\, d\theta\, d\varphi\, d\psi$: equal-area cells on the S² times equal fiber segments give equal volumes.
- **Construction (§5).** A HEALPix grid on the S² (12 base cells, ×4 per level) crossed with a regular grid on the S¹ (6 base cells) gives 72 base cells, ordered by hand. Level *l* has 72 · 8ˡ points. Point *i* goes into base cell *i* mod 72, and its position inside the cell follows a recursive cube ordering of ⌊*i*/72⌋.
- **Properties.** Incremental (the sets of size *n* and *n* + 1 differ by one point), deterministic, with a dispersion bound, O(log *i*) cost for the *i*-th element, and fast grid-neighbor lookup.
- **Comparison.** Alexa reports that the incremental construction costs quality: higher discrepancy than Super-Fibonacci, bimodal Voronoi volumes, and visible aliasing.

## Radical-inverse ordering

The radical inverse in base *b* mirrors the digits of *i* about the radix point: for $i = \sum_k d_k b^k$, $\Phi_b(i) = \sum_k d_k b^{-k-1}$. Base 2 gives the van der Corput sequence 0, ½, ¼, ¾, ⅛, ⅝, ⅜, ⅞, …

- The first 2ᵏ van der Corput values are exactly one per dyadic interval of length 2⁻ᵏ, and each further value fills an empty interval at the next finer level. The star discrepancy is O(log N / N) for every prefix length N.
- On a finite index set of size *n* with $B = \lceil \log_2 n \rceil$, visiting $\mathrm{rev}_B(0), \mathrm{rev}_B(1), \ldots$ and skipping values ≥ *n* spreads every prefix evenly over [0, *n*). For n = 1,114,112, B = 21.
- The Halton sequence combines radical inverses in pairwise coprime bases, one per dimension (PBRT).

Applied to Super-Fibonacci indices, the radical inverse makes *t* low-discrepancy for every prefix, while the angles remain irrational rotations. No published bound or paper was found for Super-Fibonacci subsets taken in radical-inverse order; the measurements below are the only evidence.

Related work that was found:

- Marques et al. 2013: closed-form spherical Fibonacci point sets on the S², $\theta_j = \arccos(1 - 2j/N)$, $\varphi_j = 2\pi j/\Phi$ with $\Phi$ the golden ratio.
- Marques et al., *Extensible Spherical Fibonacci Grids*, IEEE TVCG 2021: extensible Fibonacci-type sets on the S² only. Paywalled; not read.
- Keinert et al., *Spherical Fibonacci Mapping*, ACM TOG 2015: an O(1) inverse map from a point on the S² to its nearest spherical-Fibonacci index. Paywalled; not read. No S³ analogue is known.

## Numeric checks

All values in this section are measured. The ideal radius is that of a geodesic ball of volume $2\pi^2/n$, $r = (3\pi/(2n))^{1/3}$ (Alexa, eq. 17). NN is the distance to the nearest other point.

### Full sets

| n | Ideal r | Min NN | Mean NN | Median NN | Max NN | CV |
| --- | --- | --- | --- | --- | --- | --- |
| 1,114,112 | 0.01617 | 0.012734 | 0.019937 | 0.019248 | 0.026053 | 0.149 |
| 159,866 | 0.03089 | 0.028512 | 0.041915 | 0.042199 | 0.049476 | 0.073 |

- For comparison, 159,866 independent uniform random points have min NN 0.00046, mean 0.0276, and CV 0.365. The Super-Fibonacci minimum is about 60 times larger.
- With *q* and −*q* identified, as for SO(3), NN distances are smaller because the antipodal images interleave: min 0.009007, mean 0.017928 at n = 1,114,112.
- All norms equal 1 to within 2.2 × 10⁻¹⁶, and the centroid of the full set has norm about 10⁻⁶.

### Consecutive indices

The median distance between points *i* and *i* + 1 is 1.686 (minimum 1.591) for both sizes, larger than the mean distance between two random points, 1.358. Each step turns α by $360°/\sqrt2 \approx 254.6°$ and β by $360°/\psi \approx 234.7°$. The spiral index carries no spatial locality; [Placement](Placement.md#why-hilbert-order-fixes-it) records how Hilbert ordering supplies it.

### Subsets of 159,866 points

Different ways of choosing k = 159,866 of the 1,114,112 points:

| Subset | Min NN | Mean NN | Median NN | Max NN | CV |
| --- | --- | --- | --- | --- | --- |
| Plain prefix, indices 0 … k−1 | 0.014755 | 0.016377 | 0.015832 | 0.024051 | 0.113 |
| Radical-inverse order (21-bit, skip ≥ n) | 0.012734 | 0.040149 | 0.040575 | 0.073084 | 0.182 |
| Uniform stride round(*i* · n/k) | 0.012736 | 0.036104 | 0.038641 | 0.058907 | 0.201 |
| Random subset of indices | 0.012734 | 0.028819 | 0.026993 | 0.066680 | 0.315 |
| Fresh Super-Fibonacci set, n = k | 0.028512 | 0.041915 | 0.042199 | 0.049476 | 0.073 |

- The plain prefix covers only *t* ∈ [0, 0.1435]: a thin solid torus around the circle $x_0 = x_1 = 0$, densely packed, with the rest of the S³ empty.
- Radical-inverse order brings the mean NN within 4% of the fresh set. Its minimum NN is the parent set's minimum, because some close pair survives into the subset.

Radical-inverse prefixes of other sizes, as NN divided by the ideal radius:

| k | Min / ideal | Mean / ideal | Plain prefix, mean / ideal |
| --- | --- | --- | --- |
| 1,000 | 0.83 | 1.21 | 0.13 |
| 10,000 | 0.54 | 1.19 | 0.28 |
| 50,000 | 0.28 | 1.06 | 0.39 |
| 159,866 | 0.41 | 1.30 | 0.53 |
| 500,000 | 0.60 | 1.01 | 0.83 |

A fresh set has mean / ideal of about 1.36 at k = 159,866 and about 1.23 at n = 1,114,112.

## Centroids

The centroid of *k* points on the S³ lies inside the ball. For independent zero-mean unit vectors the cross terms vanish, so $E\lVert c\rVert^2 = 1/k$ exactly and the RMS centroid norm is $1/\sqrt{k}$; the mean is slightly lower by Jensen's inequality.

Measured over 20,000 trials of *k* independent uniform points:

| k | Mean ‖c‖ | Median ‖c‖ | RMS ‖c‖ | 1/√k |
| --- | --- | --- | --- | --- |
| 2 | 0.6776 | 0.7038 | 0.7058 | 0.7071 |
| 3 | 0.5508 | 0.5516 | 0.5773 | 0.5774 |
| 5 | 0.4231 | 0.4187 | 0.4465 | 0.4472 |
| 10 | 0.2987 | 0.2928 | 0.3164 | 0.3162 |
| 100 | 0.0941 | 0.0918 | 0.1001 | 0.1000 |

The norm depends on how spread out the points are, not only on how many there are. Measured in the 1,114,112-point set:

| k | *k* spatial nearest neighbors, mean ‖c‖ | *k* consecutive indices, mean ‖c‖ |
| --- | --- | --- |
| 2 | 0.99995 | 0.54 |
| 3 | 0.99986 | 0.11 |
| 5 | 0.99981 | 0.21 |
| 10 | 0.99968 | 0.079 |
| 100 | 0.99832 | 0.0084 |

Centroids are not injective: the same multiset of points has the same centroid in any order. See [Physicality](../Storage/Physicality.md#centroids).

## Sources

- Marc Alexa, [Super-Fibonacci Spirals: Fast, Low-Discrepancy Sampling of SO(3)](https://openaccess.thecvf.com/content/CVPR2022/papers/Alexa_Super-Fibonacci_Spirals_Fast_Low-Discrepancy_Sampling_of_SO3_CVPR_2022_paper.pdf), CVPR 2022, pp. 8291–8300; [supplementary material](https://openaccess.thecvf.com/content/CVPR2022/supplemental/Alexa_Super-Fibonacci_Spirals_Fast_CVPR_2022_supplemental.pdf); [reference implementation and README erratum](https://github.com/marcalexa/superfibonacci); [project page](https://marcalexa.github.io/superfibonacci/).
- Anna Yershova, Swati Jain, Steven M. LaValle, Julie C. Mitchell, [Generating Uniform Incremental Grids on SO(3) Using the Hopf Fibration](https://msl.cs.illinois.edu/~lavalle/papers/YerJaiLavMit10.pdf), International Journal of Robotics Research 29(7):801–812, 2010.
- Ricardo Marques, Christian Bouville, Mickaël Ribardière, Luís Paulo Santos, Kadi Bouatouch, [Spherical Fibonacci Point Sets for Illumination Integrals](https://people.irisa.fr/Mickael.Ribardiere/articles/2013/CGF_SF.pdf), Computer Graphics Forum 32(8), 2013.
- Ricardo Marques et al., [Extensible Spherical Fibonacci Grids](https://doi.org/10.1109/TVCG.2019.2952131), IEEE TVCG 27(4):2341–2354, 2021.
- Benjamin Keinert et al., [Spherical Fibonacci Mapping](https://doi.org/10.1145/2816795.2818131), ACM Transactions on Graphics 34(6), 2015.
- David W. Lyons, [An Elementary Introduction to the Hopf Fibration](https://nilesjohnson.net/hopf-articles/Lyons_Elem-intro-Hopf-fibration.pdf), Mathematics Magazine 76(2), 2003.
- Matt Pharr, Wenzel Jakob, Greg Humphreys, [Physically Based Rendering, 4th edition: Halton Sampler](https://pbr-book.org/4ed/Sampling_and_Reconstruction/Halton_Sampler).
- [Wikipedia: Van der Corput sequence](https://en.wikipedia.org/wiki/Van_der_Corput_sequence).
- [Wikipedia: Hopf fibration](https://en.wikipedia.org/wiki/Hopf_fibration).
