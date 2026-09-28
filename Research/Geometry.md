# Geometry

Research on how PostgreSQL and PostGIS store, index, and compute on four-dimensional geometry, and on the 4D distance, centroid, and curve tools that Laplace builds on them.

> [!NOTE]
> Numbers marked **measured** were produced by the local research script `frechet4d_check.py`. The PostGIS findings were read from the PostGIS 3.6.4 SQL installed with PostgreSQL 18.6 and from the PostGIS `stable-3.6` source; they were not exercised against a running server.

## Storage

PostGIS stores a geometry as GSERIALIZED:

| Field | Size |
| --- | --- |
| varlena size | 4 B |
| SRID | 3 B |
| flags (HasZ `0x01`, HasM `0x02`, HasBBox `0x04`, …) | 1 B |
| extended flags, optional | 8 B |
| bounding box, optional | `2 × ndims × sizeof(float)`, float32 |
| geometry | type number, point count, raw `double` ordinate arrays |

The ordinate arrays are kept double-aligned "to allow coordinate access without memcpy". A POINT ZM is four `float8` values, stored as they came in; nothing is quantized.

The binary paths are exact. The `geometry` type's default text output (`geometry_out`) is hex EWKB, and `ST_AsBinary`, `ST_AsEWKB`, and binary COPY carry raw IEEE-754 doubles. All of them round-trip bit for bit, Z and M included.

The geometry `=` operator and the default btree operator class (`btree_geometry_ops`) use `gserialized_cmp`. It reports equality only when SRID, HasZ, and HasM match and the bytes after the header match exactly (`memcmp`); otherwise it orders by a 2D Hilbert key of the bounding-box centre. `=` is therefore byte equality: −0.0 and 0.0 are unequal, and NaNs compare by their bytes.

## Text output

`ST_AsText` and `ST_AsEWKT` default to `OUT_DEFAULT_DECIMAL_DIGITS = 15`, which counts decimal places after the point, not significant digits. The printer is a shortest-representation (Ryu-based) printer with `OUT_MAX_DIGITS` of 17 + 8.

**Measured:** printing random S³ coordinates at 15 decimal places and parsing them back changed the double in 93.5% of cases. Printing 17 significant digits (Python `repr`) round-tripped exactly.

[ID points](../Storage/Identity.md#the-id-in-geometry) carry BLAKE3 bits in their mantissas, so they move through EWKB and binary COPY, not through WKT, EWKT, or GeoJSON, KML, and GML at default precision. [Hashing](Hashing.md#text-round-trips) has the same test on packed IDs.

## Dimensionality

PostGIS stores four dimensions exactly. Its metric operations compute in two or three, and it treats M as a measure, not a coordinate.

| Function or operator | Z | M | Notes |
| --- | --- | --- | --- |
| `ST_3DDistance`, `ST_3DLength`, `ST_3DClosestPoint`, `ST_3DDWithin`, `ST_3DIntersects` | used | ignored | 3D metric |
| `ST_Force3D`, `ST_Force4D`, `ST_MakeLine`, `ST_DumpPoints` | kept | kept | construct and decompose |
| `ST_AddMeasure`, `ST_LocateAlong`, `ST_InterpolatePoint` | — | measure | M as a linear-referencing measure |
| `ST_LineInterpolatePoint` | interpolated | interpolated | |
| `ST_Centroid` | not a 3D centroid | dropped | GEOS `GEOSGetCentroid`, XY; length-weighted for lines |
| `ST_FrechetDistance` | ignored | ignored | GEOS `DiscreteFrechetDistance` on vertices, 2D Euclidean, optional `densifyFrac` (PostGIS ≥ 2.4, GEOS ≥ 3.7) |
| `ST_HausdorffDistance` | ignored | ignored | GEOS, 2D |
| `&&` | ignored | ignored | 2D box overlap |
| `&&&` | used | used | n-D box overlap, for Z, M, and ZM |
| `<<->>` | used | used | n-D distance between box centres, for KNN (`geometry_distance_centroid_nd`) |
| `\|=\|` | used | time | closest point of approach |

There is no 4D distance: no PostGIS function uses M as a coordinate in a metric. `LWGEOM2GEOS` copies Z and M into the GEOS coordinate sequence, but GEOS algorithms compute in XY. Laplace-postgres therefore supplies its own 4D centroid, Fréchet, and distance functions.

## GiST

`gist_geometry_ops_nd` stores `gidx` keys and supports `&&&`, `~~=`, `~~`, and `@@`, plus `<<->>` and `|=|` for ORDER BY.

- **GIDX is float32.** `typedef struct { int32 varsize; float c[1]; } GIDX;` with `GIDX_MAX_DIM 4`.
- **Boxes round outward.** `gidx_from_gbox_p` applies `next_float_down(min)` and `next_float_up(max)`, "ensuring the float box is larger than the double box".
- **M is always dimension 4.** For XYM without Z, the Z slot is padded to ±`FLT_MAX`.

A float32 box keeps 24 of a double's 53 significand bits, so many distinct doubles share one box. The index is a conservative candidate filter: an exact lookup is `&&&` or `~~=` followed by a recheck on the exact doubles, such as the byte-exact `=`.

Related index support:

- **SP-GiST.** `spgist_geometry_ops_nd` (PostGIS ≥ 3.0) is an n-D box-tree with the same operators and no KNN ordering.
- **BRIN.** `brin_geometry_inclusion_ops_4d` (and `_3d`, `_2d`) stores block-range inclusion boxes. It helps when the heap is physically clustered by space, for example loaded in [Hilbert order](#hilbert-curves).

## GIN

GIN indexes composite values whose queries look for elements inside them. It stores each key with a posting list of row TIDs. The built-in operator classes are `array_ops` (`&&`, `@>`, `<@`, `=` on any array), `jsonb_ops` and `jsonb_path_ops`, and `tsvector_ops` (`@@`). btree_gin adds GIN operator classes for scalar columns such as `int`, `text`, `bytea`, and `uuid`.

In Laplace, GIN finds every container of a node, and GiST indexes the geometry ([Physicality](../Storage/Physicality.md#indexes)). The GIN index is over the trajectory geometry itself, through an operator class that Laplace-postgres provides. A GIN operator class supplies:

- `extractValue`, which returns the keys in an indexed value (here, the constituents of a trajectory);
- `extractQuery`, which returns the keys in a query value;
- `consistent` (and optionally `triConsistent`), which decides whether a row matches given which query keys it contains;
- `compare`, and optionally `comparePartial` for partial-match queries.

Properties of GIN that carry over to any operator class:

- A posting list records presence. Order and multiplicity are not in the index, so a query about them rechecks the row, where the trajectory holds both.
- Each row adds one entry per distinct key, so writes are heavy. `fastupdate` and `gin_pending_list_limit` batch them into a pending list, which reads must also scan.

## C extensions

PostgreSQL documents every piece a native extension needs:

- **C functions.** The V1 calling convention, `PG_FUNCTION_INFO_V1`, `PG_MODULE_MAGIC`, and `_PG_init`. Set-returning functions use `SRF_FIRSTCALL_INIT` and `SRF_RETURN_NEXT`, or materialize mode with a tuplestore, allocating in `multi_call_memory_ctx`. Shared memory and LWLocks use `shmem_request_hook`, `RequestAddinShmemSpace`, and DSM or DSA.
- **Base types.** Input, output, receive, and send functions; `INTERNALLENGTH`, `ALIGNMENT = double`, and `STORAGE`; varlena types with TOAST.
- **SPI**, for running SQL from C.
- **Memory contexts**: `palloc` and `pfree`, with the design described in the `mmgr` README.
- **Parallel safety.** Nearly all PostGIS C functions are `IMMUTABLE STRICT PARALLEL SAFE`.
- **Packaging** with a control file and PGXS.
- **Index access methods.** GiST, SP-GiST, GIN extensibility, and the index AM API, for Laplace's own 4D operator classes.

PostgreSQL has no dedicated documentation for memory-mapped read-only data, such as the [tier 0 perf-cache](../Storage/Atoms.md#generation). The usual pattern:

- `mmap(PROT_READ, MAP_SHARED)` the file lazily in each backend or in `_PG_init`. Backends are forked processes, and the page cache shares the physical memory among them.
- Keep the mapping outside PostgreSQL memory contexts, and copy data into Datums rather than handing out pointers into the mapping beyond a single call.
- Read-only data needs no locking. Parallel workers map the file as well.
- A GUC (`DefineCustomStringVariable`) holds the file path.

PostGIS links GEOS through the stable GEOS C API (`geos_c.h`), found at build time with `--with-geosconfig`. liblwgeom converts between its own geometry and GEOS geometry (`LWGEOM2GEOS`, `GEOS2LWGEOM`, copying coordinate sequences with `GEOSCoordSeq_copyFromBuffer` and the Z and M flags), and `initGEOS(lwnotice, lwgeom_geos_error)` routes GEOS notices and errors into PostgreSQL `ereport`. The structure is a thin PostgreSQL glue layer over a pure C core library with no PostgreSQL dependency.

## Fréchet distance

- **Continuous.** Alt and Godau (1995) decide the distance in O(pq) with the free-space diagram, and compute it exactly in O(pq log pq) with parametric search.
- **Discrete.** Eiter and Mannila (1994) define the coupling distance and compute it in O(pq) with a simple dynamic program. It is an upper bound on the continuous distance, within the longest edge. It is defined over any metric space, so it works in any dimension; each cell of the dynamic program costs one d-dimensional distance.
- **Lower bound.** Bringmann (2014): no O(n^(2−ε)) algorithm exists unless SETH fails, for continuous and discrete, and even for approximation in 1D.
- **Subquadratic discrete.** Agarwal, Ben Avraham, Kaplan, and Sharir: O(mn · log log n / log n).

**Measured** in 4D, with random codepoint points on the S³ and the Euclidean chord as ground distance:

| Comparison | Discrete Fréchet |
| --- | --- |
| `[c,a,t]` and `[a,c,t]` | 1.307 |
| `[2,5,5]` and `[2,5]` | 0 exactly |
| `[c,a,t]` and `[c,a,a,t]` | 0 |
| `[c,a,t]` and `[c,a]` | 0.255 |
| `[c,a,t]` and `[t,a,c]` | 1.189 |
| 1,000 random pairs, one curve reversed | distance changed in 973 |
| d(P, Q) and d(Q, P) | equal |

Fréchet distance is sensitive to order and orientation; Hausdorff distance is not. Repeated vertices are free, so `[2,5,5]` and `[2,5]` are at distance 0, while their IDs differ ([Hashing](Hashing.md#the-cve-2012-2459-lesson)). Reversing a curve leaves the distance unchanged only when the bottleneck pair is unaffected. On the S³, the chord 2 sin(θ/2) is monotone in the geodesic angle θ, so the optimal coupling is the same under either ground distance.

Fast, approximate, and indexing work:

- Driemel, Har-Peled, and Wenk: a (1 + ε)-approximation in near-linear time for c-packed curves.
- Driemel and Silvestri: locality-sensitive hashing for curves under discrete Fréchet.
- Filtser, Filtser, and Katz: approximate nearest neighbours for curves.
- Bringmann, Künnemann, and Nusser: an engineered decider with pruning and filters.
- Data structures for approximate discrete Fréchet distance.
- "Walking Your Frog Fast in 4 LoC": a short, fast discrete Fréchet algorithm.
- Filters for similarity search: endpoint lower bounds, d ≥ max(|P₀ − Q₀|, |Pₙ − Qₘ|), bounding boxes, and simplification bounds. They form a candidate stage, such as GiST-nd, ahead of an exact recheck in C.

[Numerics](Numerics.md#trajectory-measures) compares Fréchet with DTW, EDR, and LCSS on noisy sequences.

## Centroids

Two definitions of a polyline's centroid:

| Definition | Formula | Repeated vertices |
| --- | --- | --- |
| Vertex average | Σvᵢ / n | shift the centroid |
| Length-weighted | Σ ℓₖ · midpointₖ / Σ ℓₖ | no effect: a zero-length segment has weight 0 |

GEOS and `ST_Centroid` use the length-weighted form, in 2D. Under the vertex average, `[c,a,t]` and `[a,c,t]` have the same centroid, as in [Physicality](../Storage/Physicality.md#centroids), and `[a,a,b]` differs from `[a,b]`.

**Measured:** inserting a repeated vertex changed the vertex average and left the length-weighted centroid unchanged. For four random points on the S³, the vertex average had ‖c‖ = 0.35 and the length-weighted centroid ‖c‖ = 0.42.

Either centroid of points on the S³ lies inside the ball, with ‖c‖ < 1 unless all points coincide. The norm ‖c‖ measures concentration, like the mean resultant length in directional statistics. c / ‖c‖ is the extrinsic mean on the S³; the intrinsic (Karcher) mean needs iteration. [Numerics](Numerics.md#the-fixed-point-grid) covers keeping ‖c‖ ≤ 1 exact in floating point.

## S³ distance and projection

- **Geodesic distance.** θ = arccos(u · v), computed stably as `atan2(|u − (u·v)v|, u·v)`.
- **Chord.** 2 sin(θ / 2). **Measured:** for one pair, θ = 1.8738, and the chord and 2 sin(θ/2) both equal 1.6115.
- **Stereographic projection** from the pole N = (0, 0, 0, 1): (x, y, z, w) ↦ (x, y, z) / (1 − w). It is conformal and maps great 2-spheres and circles to spheres, circles, planes, or lines, and it diverges near N.
- **Other views.** The Hopf fibration S³ → S², or dropping one coordinate for an orthographic view.

## Hilbert curves

[Atoms](../Storage/Atoms.md#placement) orders the codepoint points by Hilbert value, for locality, partitioning, and ordering.

- **Skilling (2004)** applies one Gray code over all n·p bits and then a single undo pass (`AxestoTranspose`, `TransposetoAxes`), in O(n·p) time with no tables. Public ports exist in Rust and Python.
- **Hamilton** defines compact Hilbert indices, which allow unequal bits per axis.
- **Haverkort** studies Hilbert curve families in d dimensions, their locality, and their bounding-box quality.
- **Moon, Jagadish, Faloutsos, and Saltz (2001)** show that Hilbert order clusters better than Z-order.

Using a Hilbert key in PostgreSQL:

1. Quantize each 4D coordinate to p bits: 4 × 16 bits fit a `bigint`, and 4 × 32 bits fit 128 bits.
2. Compute the Hilbert index in C.
3. Store it as a btree key, and `CLUSTER` or load in key order so that BRIN-4D and GiST pages are spatially coherent.
4. Answer a range query by decomposing the box into Hilbert intervals, then rechecking exactly.

PostGIS already sorts geometry by a Hilbert key of the bounding-box centre (`gserialized_cmp`, `geometry_sortsupport`), in 2D only.

## Sources

- [PostGIS `gserialized.txt`](https://github.com/postgis/postgis/blob/stable-3.6/liblwgeom/gserialized.txt).
- [PostGIS `gserialized_gist.h`](https://github.com/postgis/postgis/blob/stable-3.6/libpgcommon/gserialized_gist.h) and [`gserialized_gist.c`](https://github.com/postgis/postgis/blob/stable-3.6/libpgcommon/gserialized_gist.c).
- [PostGIS `liblwgeom_internal.h`](https://github.com/postgis/postgis/blob/stable-3.6/liblwgeom/liblwgeom_internal.h) and [`lwgeom_ogc.c`](https://github.com/postgis/postgis/blob/stable-3.6/postgis/lwgeom_ogc.c).
- [PostGIS functions that support 3D](https://postgis.net/docs/manual-3.6/PostGIS_Special_Functions_Index.html).
- [PostGIS `ST_Centroid`](https://postgis.net/docs/ST_Centroid.html), [`ST_FrechetDistance`](https://postgis.net/docs/ST_FrechetDistance.html), and [`&&&`](https://postgis.net/docs/geometry_overlaps_nd.html).
- [PostgreSQL GIN](https://www.postgresql.org/docs/current/gin.html), [GIN extensibility](https://www.postgresql.org/docs/current/gin.html#GIN-EXTENSIBILITY), and [btree_gin](https://www.postgresql.org/docs/current/btree-gin.html).
- [PostgreSQL C-language functions](https://www.postgresql.org/docs/current/xfunc-c.html), [user-defined types](https://www.postgresql.org/docs/current/xtypes.html), [TOAST considerations](https://www.postgresql.org/docs/current/xtypes.html#XTYPES-TOAST), and [`CREATE TYPE`](https://www.postgresql.org/docs/current/sql-createtype.html).
- [PostgreSQL SPI](https://www.postgresql.org/docs/current/spi.html) and the [memory context README](https://github.com/postgres/postgres/blob/master/src/backend/utils/mmgr/README).
- [PostgreSQL parallel safety](https://www.postgresql.org/docs/current/parallel-safety.html), [extensions](https://www.postgresql.org/docs/current/extend-extensions.html), and [PGXS](https://www.postgresql.org/docs/current/extend-pgxs.html).
- [PostgreSQL GiST](https://www.postgresql.org/docs/current/gist.html), [SP-GiST](https://www.postgresql.org/docs/current/spgist.html), and [index access method interface](https://www.postgresql.org/docs/current/indexam.html).
- [GEOS C API](https://libgeos.org/doxygen/geos__c_8h.html).
- [Alt and Godau, "Computing the Fréchet distance between two polygonal curves", IJCGA 5, 1995](https://doi.org/10.1142/S0218195995000064).
- [Eiter and Mannila, "Computing discrete Fréchet distance", CD-TR 94/64](https://www.kr.tuwien.ac.at/staff/eiter/et-archive/files/cdtr9464.pdf).
- [Bringmann, arXiv:1404.1448](https://arxiv.org/abs/1404.1448).
- [Agarwal, Ben Avraham, Kaplan, Sharir, arXiv:1204.5333](https://arxiv.org/abs/1204.5333).
- [Driemel, Har-Peled, Wenk, arXiv:1003.0460](https://arxiv.org/abs/1003.0460).
- [Driemel and Silvestri, arXiv:1703.04040](https://arxiv.org/abs/1703.04040).
- [Filtser, Filtser, Katz, arXiv:1902.07562](https://arxiv.org/abs/1902.07562).
- [Bringmann, Künnemann, Nusser, "Walking the Dog Fast in Practice", arXiv:1901.01504](https://arxiv.org/abs/1901.01504), with [code](https://zenodo.org/records/5644988).
- [Data structures for approximate discrete Fréchet distance, arXiv:2212.07124](https://arxiv.org/abs/2212.07124).
- ["Walking Your Frog Fast in 4 LoC", arXiv:2404.05708](https://arxiv.org/abs/2404.05708).
- [3-sphere, Wikipedia](https://en.wikipedia.org/wiki/3-sphere).
- [Skilling, "Programming the Hilbert curve", AIP Conf. Proc. 707, 2004](https://ui.adsabs.harvard.edu/abs/2004AIPC..707..381S), with ports in [Rust](https://github.com/paulchernoch/hilbert) and [Python](https://pypi.org/project/hilbertcurve/).
- [Hamilton, "Compact Hilbert Indices"](https://web.cs.dal.ca/~arc/publications/2-43/paper.pdf).
- [Haverkort, arXiv:1711.04473](https://arxiv.org/abs/1711.04473), [arXiv:1211.0175](https://arxiv.org/abs/1211.0175), and [Haverkort and van Walderveen, arXiv:0806.4787](https://arxiv.org/abs/0806.4787).
- [Moon, Jagadish, Faloutsos, Saltz, IEEE TKDE 13(1), 2001](https://dl.acm.org/doi/10.1109/69.908985).
