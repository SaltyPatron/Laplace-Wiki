# Reader search surface audit

This inventory covers the two browser readers and the Native search read as
inspected on 2026-11-02 UTC. Product requirements remain those in the
[information-world model](08_PRODUCT_INFORMATION_WORLDS.md),
[#1537](https://github.com/SaltyPatron/Laplace/issues/1537) and
[#1404](https://github.com/SaltyPatron/Laplace/issues/1404).
It does not certify the repository-wide CLI, SQL, chat or construction surfaces.

| Entry or operation | Meaning and implementation | Boundary |
| --- | --- | --- |
| Monolith header, Knowledge, `/query`, historical `/topic` and textual `/explore/resolve` | Whole input enters the shared knowledge collection. Applicable entity and query methods compose; peer URL coordinates survive transitions. Textual resolution no longer silently changes a discovery miss into geometry. | Entity candidates and query methods remain independently bounded. Retained unsupported coordinates are disclosed. |
| Monolith relation entry and Highway search launchers | Shared search launcher preserves the whole observation and criteria. Relation entry requests the actual `mesh` presentation. Selection, parent/member pivots and comparison stay beside the originating collection. | Historical standalone domain routes still exist; complete domain and arena integration remains required. |
| Monolith collection and source checkboxes | OR within a field and AND across fields filter the returned finite collection. Search-method checkboxes enable concurrent applicable reads. | These are local collection filters, not global facet predicates or a tool selector. |
| Monolith exact canonical ID and `/explore/entity/{id}` | Direct addressing retains the requested identity. A preview that does not report content present is displayed as such. | A canonical ID alone establishes neither recording nor testimony. |
| Monolith `/explore/notfound/{input}` | Explicit identity/geometry calculation and returned geometric neighbors, with a separate known-content search action. | Similar spelling and geometric proximity do not establish a semantic relationship or an admitted root. |
| Modular knowledge input | Native `search` and observed continuations compose. Native discovery matches, root/member claims and containing structures form one deduplicated collection; measurements and query-member positions remain attached. | Calculated/unresolved roots are excluded from matches. Current response is scoped to the returned read, not all matching content. |
| Modular source/file filter and resource/tier/method checkboxes | Finite returned collection filtering with independent source and knowledge paging/filter keys. | Source provenance is an inspection path, not the organization of all knowledge. Global counts and predicates remain absent. |
| Modular selected resource and member occurrence | Direct canonical resource addressing; member references retain originating query, selected physicality and logical ordinal. Export retains the query root and discovery observations. | Returned physicality ordinal needs durable version/snapshot binding. Query decomposition ordinal is distinct from a stored occurrence. |
| Native HTTP/MCP `search` | Shared `laplace-discovery/v1` matches report database or canonical-cache presence, separate from computed identity and stored tier. Repeated query members retain separate positions. | 64-part text/cache prefix is explicit. Full interpretations, stable ranked paging, obligations, arena and epoch scope remain open. |
| Native `embeddings`, `shape`; modular calculation workspace | Explicit identity/geometry operations and schema-declared calculations. | Their outputs are calculations; no output creates admission or testimony. |
| Native schema banks | Canonical value IDs, labels and slots come from the selected Highway. | Enumeration does not imply implemented global filters, operators or counts. |

The obsolete unused monolith `ResolveRedirect` implementation was removed to
avoid retaining a second resolver that routed unknown text into geometric
exploration. The old `view=mesh` launcher parameter was replaced by the shared
presentation contract; a route that ignores a requested presentation is not a
successful implementation.

The browser fixture suites exercise finite filtering, preserved context,
calculated-root exclusion, repeated query-member positions, direct addressing
and domain pivots. Native integration uses a disposable database and verifies
HTTP/MCP parity, cache-only presence and incomplete-prefix disclosure. These
checks do not close either issue's broader requirements.
