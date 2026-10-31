# Windows LZ4 decoder repair

On HART-DESKTOP, PostgreSQL 18.6 could not create `laplace_substrate` in a
new database. Building `consensus_edge_rank_btree` failed in `nodeRead` with
`XX000: did not find '}' at end of input node`.

The installed LZ4 1.10.0 decoder, compiled with IntelLLVM 2026.1.1, returned
the expected decoded length but left bytes unwritten. The regression input
in `tests/lz4-index-expression.txt` reproduces the failure outside PostgreSQL.
Rebuilding the same pinned source with loop vectorization disabled fixes
the reproduced failure. `/O2`, inlining and SLP vectorization remain enabled.
This evidence identifies a decoder build failure; it does not establish an
upstream source defect or certify all historical stored values.

`setup.ps1` records the LZ4-specific compiler option in its dependency
contract, rebuilds older installations, and runs `tests/windows-lz4.ps1`
against the actual DLL before accepting it. Runtime closure refresh also
replaces a stale PostgreSQL-adjacent LZ4 copy, with a backup and the existing
service-stop boundary. A failed copy or regression check restores the backup.

## Activation evidence

The operator executed recovery on 2026-10-15 at 05:25 UTC against the original
cluster `7696004236835714020`. Both the dependency prefix and PostgreSQL
`bin/lz4.dll` then had SHA-256
`6258E2A551B9D2369F1C8F726D8B749FB7FABAAFD270A32F9CEE28726D1264B3`.
The actual installed DLL passed 10,001 byte-exact full and partial decode
cases, including output-boundary checks. All seven substrate migrations
completed, with zero pending. IIS subsequently served HTTP 200, reached
the substrate, and reported its native cache ready.

These receipts are retained under the desktop task root
`C:/Users/ahart/AppData/Local/Temp/laplace-database-lifecycle-20261015`:

- `receipts/lz4-repair-20261015T0525271831411Z/receipt.json`
- `receipts/iis-database-20261015T0525337819260Z/receipt.json`
- `site-recovery-receipts/iis-restart-20261015T0525399378374Z.json`

Product readiness remained false because the recreated substrate was empty.
Schema recovery does not restore ingested content. Chess transition-cache
readiness also remained false; the position cache was loaded. These results
are separate from LZ4 and website recovery and do not close whole-installation
acceptance.

Run the named `lz4-windows-roundtrip` acceptance check to verify the selected
installed DLL. It requires the declared Windows toolchain; it does not stop
PostgreSQL or mutate a database.
