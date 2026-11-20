# ConceptNet

ConceptNet 5.7 attests commonsense relation edges scored by assertion `weight`, decomposing concept URIs into `[lemma, language, pos, qualifier]` terms, preserving `Relations.md` relation definitions and `ExternalURL` crosswalks to Wikidata, WordNet, DBpedia, and Wiktionary, and omitting edge packaging bookkeeping.

The source is ConceptNet 5.7's assertions dump (`assertions.csv`), accompanied by ConceptNet's relation inventory (`Relations.md`) and URI specifications ([Downloads](https://github.com/commonsense/conceptnet5/wiki/Downloads), [Edges](https://github.com/commonsense/conceptnet5/wiki/Edges), [URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy), [Relations](https://github.com/commonsense/conceptnet5/wiki/Relations)).

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `conceptnet` | `ConceptNet` source trunk | class `UserCuratedResource` | `unicode`, `iso-639`, `wiktionary` | `assertions.csv` (`conceptnet-assertions-5.7.0.csv`), `Relations.md` | [`assertions.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/assertions.recipe), [`relations.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/conceptnet/relations.recipe) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

ConceptNet's `concept_uri` sub-grammar decomposes `/c/<lang>/<lemma>[/<pos>[/<qualifier>]]` paths (`part start grammar concept_uri`, `part end grammar concept_uri`): underscores in `<lemma>` decode to spaces (`/c/en/ice_cream/n` → `ice cream`), `<lang>` resolves onto its ISO 639 highway node (`type lexicalization.language language`), and `<pos>` crosswalks through `wordnet-pos` onto `upos` while retaining satellite categories such as `s` (`type pos.category upos crosswalk wordnet-pos`).

## The assertions (`assertions.csv`)

Each tab-separated line has five fields (`uri`, `rel`, `start`, `end`, `json`). `ConceptNet` is the single corpus witness trunk; `contributor` entries inside `json.sources` are participant qualifiers (`itself edge with json/sources/contributor`), never separate witnesses ([30. Conflicts](../Sequence/Conflicts.md) I3).

Two Recording Law rules govern edge weights and external crosswalks:

- **Edge `weight` scores the attestation (`score edge json/weight from 0 to 2`)**: ConceptNet documents `weight` as *"the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive."* `assertions.recipe` maps `json/weight` directly onto the attestation score (`0` loss, `1.0` neutral draw, `2.0+` full win) rather than recording `"weight"` as a string claim or treating low-weight noisy edges (`weight < 1`) as unconditional wins.
- **`/r/ExternalURL` crosswalks join shared highway nodes**: ConceptNet's `/r/ExternalURL` rows link `/c/<lang>/<term>/<pos>` nodes directly to Wikidata QIDs (`http://wikidata.dbpedia.org/resource/Q...`), Princeton/RDF WordNet synsets (`http://wordnet-rdf.princeton.edu/wn31/...`), DBpedia, OpenCyc, and Wiktionary URLs. Parsed by dedicated external-URI sub-grammars rather than naive `/` splitting, these rows supply high-value cross-resource highway bridges onto `Q...` and `ILI` nodes (`Batch 2` recipe gap: `assertions.recipe` currently filters `where rel/2 is-not ExternalURL` because the `concept_uri` `/` splitter had not yet been paired with an external-URL grammar).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `start`, `end` | `/c/en/dog`, `/c/en/ice_cream/n/wn/food` | decomposed by `concept_uri` into `[lemma, language, pos, qualifier]` (`ice cream`, `en`, `n` → `NOUN`, qualifier) | subject and object of the assertion `[start, rel, end]` | [URI hierarchy](https://github.com/commonsense/conceptnet5/wiki/URI-hierarchy) |
| `rel` | `/r/IsA`, `/r/CapableOf`, ... | ConceptNet relation (`rel/2`: `IsA`, `CapableOf`, ...) | predicate of `[start, IsA, end]` | "The relation expressed by the edge" |
| `rel` `/r/ExternalURL` | `/r/ExternalURL` with Wikidata, WordNet, DBpedia, OpenCyc, or Wiktionary target URL | external-URI sub-grammar extracts Wikidata QID (`Q...`), WordNet synset → `ILI`, or canonical external identifier | target: `[concept, ExternalURL, Q... / ILI / resource_id]` crosswalk strand (`Batch 2` gap: `assertions.recipe` currently skips `ExternalURL` rows via `where rel/2 is-not ExternalURL`) | "ExternalURL: Points to a URL outside of ConceptNet" |
| `weight` in `json` | `"weight": 1.0` / `2.828` / `0.25` | attestation strength score (`score edge json/weight from 0 to 2`, `omit json.weight`) | scored outcome on `[start, rel, end]` (already active in `assertions.recipe`) | "weight: the strength with which this edge expresses this assertion" |
| `sources[].contributor` in `json` | `"/s/contributor/omcs/..."` | participant content qualifying the assertion (`itself edge with json/sources/contributor`) | contributor provenance under the single `ConceptNet` trunk | "sources that, when combined, say that this assertion should be true" |
| `surfaceText` in `json` | natural-language prompt template, or `null` | attested on the edge (`relation "the original natural language text" json.surfaceText`); `surfaceStart`/`surfaceEnd` omitted | `[edge, the original natural language text, text]` | "The original natural language text that expressed this statement" |
| `uri`, `dataset`, `license`, `process`, `activity` | assertion path and provenance packaging | bookkeeping (`omit`) | none | redundant edge path and build metadata |

## The relations page (`Relations.md`)

`relations.recipe` reads the `Relations in ConceptNet 5` Markdown table, attesting each relation's prose definition and canonical examples (`[IsA, Description, …]`, `[IsA, Examples, …]`).

## Relations

`assertions.recipe` already scores edges by `json/weight`, decomposes `/c/...` URIs with `concept_uri` and `wordnet-pos` → `upos` crosswalks, keeps contributors as participant qualifiers under one `ConceptNet` trunk, and maps `surfaceText` to its documented semantic relation. Closing the `Batch 2` gap adds the external-URI grammar so `/r/ExternalURL` rows bridge ConceptNet concepts onto Wikidata QIDs and WordNet `ILI` nodes cleanly.
