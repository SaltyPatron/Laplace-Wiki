# Windows Zstd decoder repair

On 2026-10-22, HART-DESKTOP's PostgreSQL 18.6 crash recovery failed with
`corrupted line pointer: 30854` while replaying a heap pruning record.
The preceding Zstd-compressed full-page WAL image was valid. Both locally
built Zstd 1.5.7 DLLs decoded four zero bytes incorrectly. An independent
decoder reconstructed the page correctly.

Rebuilding the same pinned source with the declared IntelLLVM toolchain
and `/clang:-fno-vectorize` produced the exact reference output. PostgreSQL's
own `pg_waldump` using that rebuilt DLL produced the same 8192-byte page.
The per-dependency option retains `/O2`, inlining and SLP vectorization.

`tests/windows-zstd.ps1` tests a selected actual DLL without accessing a
database or stopping PostgreSQL. Its C probe generates 4096 overlapping
short-match cases followed by 12000 deterministic inputs at compression
levels 1, 3 and 9, checking decoded bytes and output bounds. The old DLL
fails short-match case 450 at byte 297; the rebuilt DLL passes all cases.
The regression contains no database contents or captured WAL.

`setup.ps1` records the changed Zstd dependency contract, rebuilds stale
installations, and requires the DLL regression before acceptance. Runtime
closure verifies replacement codec DLLs before stopping a running service,
backs up the installed copy, refreshes the PostgreSQL-adjacent DLL and
checks it again. Copy or regression failure restores the old binary.

Use `laplace-ops repair-postgres` (or `pwsh -File setup.ps1 repair-postgres`)
to apply the repair through the maintained installer. `-Plan` on the CLI
or `-Check` on setup inspects the selected service without changing it.
The repair rebuilds only the declared LZ4/Zstd dependencies, verifies the
replacement DLLs and refreshes PostgreSQL's runtime with backups. It sets
up a fresh CMake configuration in the existing declared dependency build tree,
discarding cached paths to removed checkouts. Codec builds and verification
finish before stopping a recovered database; a build failure leaves it running.
The service repair sets
the service's startup wait to at least 1200 seconds: the default 60 seconds
expired during this cluster's successful WAL recovery and left a ready
postmaster behind a stopped Windows service. A surviving postmaster is
verified and stopped cleanly before the service takes ownership again.
The first service-command correction requires Windows service configuration
rights; that check happens before stopping a recovered database. Host setup
also registers new PostgreSQL services with the corrected wait.

The repair completes only when the service is Running, PostgreSQL accepts
connections and an authenticated read verifies the original system identifier,
data directory and completed recovery. It saves a repair receipt and the
installed codec hashes. A startup failure preserves the corrected binaries.
It does not reset WAL, recreate databases or use OpenBao to start PostgreSQL.

Run `tests/windows-zstd.ps1 -Library <absolute-dll-path>` for an explicit
library, or the named `zstd-windows-roundtrip` acceptance check for the
declared PostgreSQL runtime. PostgreSQL startup and completed WAL replay
must be checked separately after installing the corrected DLL.
