# SemLink

SemLink 2 attests cross-lexicon role and frame mappings joining PropBank rolesets, VerbNet classes and thematic roles, and FrameNet frames (`pb-vn2.json`, `vn-fn2.json`, `external_vn2pb.json`, `other_resources/`), together with WSJ predicate-argument sentence instances annotated simultaneously across those resources.

SemLink 2 ("the mappings between PropBank, VerbNet and FrameNet", aligned to VerbNet 3.3+, Unified PropBank frames, and FrameNet 1.7) serves both as a core interchange on the linguistic superhighway ([Hops](Hops.md)) and as a multi-formalism annotated corpus over Wall Street Journal text.

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `semlink` | `SemLink` source trunk | class `AcademicCurated` | `propbank`, `verbnet`, `framenet` | `instances/pb-vn2.json`, `instances/vn-fn2.json`; target `Batch 2` expansion adds WSJ annotated instances under `instances/`, `external_vn2pb.json`, and role/frame tables under `other_resources/` | [`pb-vn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/semlink/pb-vn.recipe), [`vn-fn.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/semlink/vn-fn.recipe) (instance and auxiliary role recipes queued for `Batch 2`) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## Lexicon-to-lexicon mappings & WSJ annotated instances

Each mapping row is one interchange strand where a route switches road classes (`pbroleset` ↔ `vnclass` with `ARGn` ↔ `vnrole` role bindings, and `vnclass` ↔ `fnframe`), feeding `laplace highway` ([Types](../Reference/Types.md#perf-caches)). Alongside the type-level JSON dictionaries, SemLink's WSJ annotated instances and `other_resources` role/frame alignment tables supply empirical sentence-grounded bindings showing which `[roleset, vnclass, fnframe]` and argument-to-role pairings co-occur on real predicates in context.

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state |
| --- | --- | --- | --- |
| `pb-vn2.json` outer key | `"abduct.01": { ... }` | PropBank roleset highway node (`type … pbroleset`, content `abduct.01`) | first node of `[roleset, vnclass]` |
| `pb-vn2.json` class key & role map | `"10.5": { "ARG0": "agent", "ARG1": "theme" }` | VerbNet class highway node (`abduct-10.5`, `type … vnclass`) and argument-to-`vnrole` correspondences | `[abduct.01, abduct-10.5]`, `[[abduct.01, abduct-10.5], ARG0, Agent]`, plus `pbroleset`→`vnclass` highway edge |
| `vn-fn2.json` class key & frame list | `"26.5-shake": ["Moving_in_place", "Body_movement"]` | VerbNet class (`26.5` → `vnclass`) mapped to FrameNet frame highway nodes (`type … fnframe`) | `[vnclass, fnframe]` interchange strands + `vnclass`→`fnframe` highway edges |
| WSJ annotated instances (`instances/`) | WSJ sentence/token pointer, predicate lemma, PropBank `roleset`, VerbNet `vnclass`, FrameNet `fnframe`, and span `ARGn`↔`vnrole`↔`fnfe` tags | sentence-aligned predicate-argument annotation layers resolving WSJ token pointers onto canonical WSJ sentences and binding `pbroleset`, `vnclass`, `fnframe`, `vnrole`, and `fnfe` on each instance | target: contextual multi-lexicon instance attestations and empirical pairing counts (`Batch 2` recipe gap: not yet matched by a recipe in `recipes/semlink/`) |
| `external_vn2pb.json` & `other_resources/` role mappings | `"change_bodily_state-40.8.4": ["sicken.01"]`, FN↔VN role alignment tables | supplementary `vnclass`↔`pbroleset` and `vnrole`↔`fnfe` interchange strands | target: admitted into SemLink's highway and claim set (`Batch 2` recipe gap: currently unmatched) |

## Relations

`pb-vn.recipe` and `vn-fn.recipe` already emit pure interchange strands (`[roleset, class]`, `[class, frame]`, `[[roleset, class], ARG0, agent]`) with zero markup field names. Adding recipes in `Batch 2` for SemLink's WSJ annotated instances, `external_vn2pb.json`, and `other_resources/` role mappings completes both empirical instance frequency weighting and `vnrole`↔`fnfe` role-level highway bridges.
