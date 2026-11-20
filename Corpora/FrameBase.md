# FrameBase

FrameBase 2.0 attests RDFS/Lemon frame schema statements and `owl:sameAs` crosswalks bridging FrameNet frames, frame elements, and lexical units (`fnframe`, `fnfe`, `fnlu`) with WordNet 3.0 synsets resolved onto `ILI` highway nodes.

One source reads FrameBase 2.0 ("the RDFS+ core schema, Lemon lexical annotations, and `owl:sameAs` links to WordNet 3.0 RDF", [FrameBase data](https://www.framebase.org/data), [FrameBase schema](https://www.framebase.org/schema)). FrameBase is a cross-lexicon interchange source under [Hops](Hops.md), linking FrameNet frame structures and WordNet synsets without duplicating FrameNet's full-text sentence corpus.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `framebase` | `FrameBase` source trunk | class `AcademicCurated` | `unicode`, `iso-639`, `framenet`, `cili` | `FrameBase_schema_*.ttl.gz` under `FrameBase-2.0` | [`schema.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framebase/schema.recipe) (currently `like turtle`) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## URI decomposition and highway alignment

FrameBase encodes structured lexical and synset references directly inside its HTTP IRIs ([FrameBase schema](https://www.framebase.org/schema)):

- `http://framebase.org/frame/<Frame>` and LuMicroframes `http://framebase.org/frame/<Frame>.<lemma>.<pos>` name FrameNet frames (`fnframe`, e.g., `Closure`) and frame-scoped lexical units (`fnlu`, e.g., `[Closure, button.v]`).
- `http://framebase.org/fe/<Frame>.<FE>` names FrameNet frame elements (`fnfe`, e.g., `[Closure, Agent]`).
- `http://framebase.org/frame/Synset<offset>.<lemma>.<pos>` and `http://wordnet-rdf.princeton.edu/wn30/<offset>-<pos>` carry Princeton WordNet 3.0 `(offset, pos)` pointers (`01895612-v`).

Under the Recording Law ([30. Conflicts](../Sequence/Conflicts.md) S1, I5), structured URI syntax is packaging around highway identifiers and edition offsets: chained URI sub-grammars decompose FrameBase frame/FE/LU paths onto FrameNet's `fnframe`, `fnfe`, and `fnlu` highway nodes and resolve `wn30/<offset>-<pos>` offsets through `highway.bin` (`cili` PWN 3.0 map) onto canonical `ILI` highway nodes (`i46360`) and `[lemma, eng, ILI]` lexicalization strands—so FrameBase's `owl:sameAs`, `rdfs:subClassOf`, and Lemon lexical sense links join the linguistic superhighway directly instead of stranding isolated `http://...` strings (`Batch 2` recipe gap: `schema.recipe` currently inherits generic `turtle.recipe`, recording unsplit URI strings and skipping Turtle blank nodes `[ ... ]` and RDF collections `( ... )`).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| FrameBase frame / LU / FE IRI | `<http://framebase.org/frame/Closure.button.verb>`, `<http://framebase.org/fe/Closure.Agent>` | decomposed by URI sub-grammar onto `fnframe` (`Closure`), `fnlu` (`[Closure, button.v]`), or `fnfe` (`[Closure, Agent]`), retaining FrameBase microframe hierarchy (`LuMicroframe`, `SynsetMicroframe`, `Miniframe`) | highway-linked frame, LU, and FE claims + `maps` edges (`Batch 2` gap: `schema.recipe` currently records the unsplit IRI text) | [FrameBase schema](https://www.framebase.org/schema) |
| WordNet 3.0 RDF IRI | `<http://wordnet-rdf.princeton.edu/wn30/01895612-v>` | decomposed to PWN 3.0 offset `01895612-v`, resolved via `highway.bin` to its `ILI` node, with the raw byte-offset URI recorded nowhere | `[ILI, owl:sameAs, microframe]` + `ili`↔`fnframe`/`fnlu` highway edge (`Batch 2` gap: currently unsplit IRI string) | "`owl:sameAs` links with the RDF version of WordNet" ([FrameBase data](https://www.framebase.org/data)) |
| RDF/RDFS/OWL/Lemon predicate | `owl:sameAs`, `rdfs:subClassOf`, `a`, `lemon:lexicalForm`, `lexinfo:...` | vocabulary property from the RDFS, OWL, W3C Lemon, or LexInfo ontology | semantic predicate of the statement | FrameBase core & Lemon schemas |
| Language-tagged or typed literal | `"..."@en`, `"..."^^<xsd:...>` | decoded UTF-8 literal paired with its ISO 639 language node or XSD datatype | `[literal, en]`, `[subject, predicate, [literal, en]]` | RDF 1.1 Turtle literals |
| Blank nodes & RDF collections | `[ ... ]`, `_:b0`, `( ... )` | anonymous property bundles and ordered RDF lists in the schema | target: resolved inline onto their enclosing subject/list composition (`Batch 2` gap: currently skipped by `turtle.recipe`) | RDF 1.1 Turtle blank-node and collection syntax |

## Relations

Unlike tabular CSV headers, FrameBase's predicates (`owl:sameAs`, `rdfs:subClassOf`, `lemon:*`, `lexinfo:*`) are already formal ontology relations rather than markup column names. Replacing `like turtle` in `schema.recipe` with FrameBase's URI sub-grammar, blank-node/collection folding, and `highway` `maps` lines in `Batch 2` connects every FrameBase microframe and `wn30` link directly onto `ILI` and `FrameNet`.
