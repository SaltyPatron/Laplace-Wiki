# VerbNet

VerbNet attests what each class file says of its verb classes and subclasses (`leave-51.2`), class-scoped thematic roles (`[vnclass, role]`) and selectional restrictions, verb members (`grouping` PropBank rolesets, `fn_mapping` FrameNet frames, and `wn` WordNet sense keys), and syntactic-semantic frames.

Two sources in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) read VerbNet XML class hierarchies via [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe): `verbnet` (VerbNet 3.4) and `verbnet-gl` (VerbNet Generative Lexicon subcategorizations). VerbNet classes and thematic roles populate the highway's `vnclass` (609 classes) and `vnrole` (39 roles, mapped to the `vnrole` `bit(64)` bank: `6` bits at offset `25`, [Types](../Reference/Types.md)), while member mappings supply highway edges ([Hops](Hops.md)).

## Sources

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `verbnet` | `VerbNet` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `verbnet3.4` | [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe) |
| `verbnet-gl` | `VerbNet Generative Lexicon` source trunk | class `AcademicCurated` | `verbnet` | `vn-gl/*.xml` | [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet-gl/classes.recipe) (`like verbnet-classes`) |

The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior bounds the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The class file

> [!IMPORTANT]
> **Class-scoped thematic role restrictions (`[vnclass, role]`):** In VerbNet XML, `<THEMROLE type="Theme">` appears inside a specific `<VNCLASS>` or `<VNSUBCLASS>` with selectional restrictions (`<SELRESTRS logic="or"><SELRESTR Value="+" type="animate"/>...`) that apply **only to `Theme` in that class or subclass** (whereas another class restricts `Theme` to `-animate` or `+concrete`). Selectional restrictions **must** attach to the class-scoped role `[vnclass, role]` (e.g., `[[leave-51.2, Theme], +animate]`), **never** to bare global `Theme` (`Batch 2` recipe fix: `classes.recipe` currently declares `thing THEMROLE type` without `within`, attaching `<SELRESTR>` attributes globally onto bare `Theme`).

| Piece | Written as | Laplace reads it as | Target attestation & current recipe state | Specification |
| --- | --- | --- | --- | --- |
| `<VNCLASS ID="leave-51.2">` | root element | VerbNet class highway node (`thing VNCLASS ID`, `types vnclass`), keyed both by `leave-51.2` and numeric suffix `51.2` | class subject `leave-51.2` | `vn_schema-3.xsd` |
| `<VNSUBCLASS ID="leave-51.2-1">` | under `SUBCLASSES` | subclass highway node (`thing VNSUBCLASS ID`), inheriting parent features | `[leave-51.2, subclass, leave-51.2-1]` | "VerbNet subclasses inherit features from the top class" |
| `<MEMBER name="abandon" wn="abandon%2:40:00 ..." grouping="abandon.01" fn_mapping="Departing" verbnet_key="abandon#1">` | under `MEMBERS` | verb lemma scoped to its class/subclass (`[leave-51.2, abandon]`); `grouping` → `pbroleset`, `fn_mapping` → `fnframe` (`None` omitted), `wn` sense keys → `[lemma, eng, ILI]` lexicalization via `highway.bin` (`verbnet_key`, `xtag`, `descriptionNumber` omitted as pointers/bookkeeping) | `[leave-51.2, verb member, abandon]`, class-member links to `abandon.01`, `Departing`, and `[abandon, eng, ILI]` (`classes.recipe` currently resolves `wn` to `ILI` via `type wn ili` and attaches member attributes; scoping member sense links cleanly to `[vnclass, member]` + lexicalization closes in `Batch 2`) | "Contains the list of verbs belonging to a specific class or subclass." |
| `<THEMROLE type="Theme">` with `<SELRESTRS>` / `<SELRESTR Value="+" type="animate"/>` | under `THEMROLES` | thematic role `Theme` (`vnrole` slot) **scoped to its enclosing `VNCLASS`/`VNSUBCLASS`** (`[leave-51.2, Theme]`), with boolean selectional restriction expressions (`+animate`, `logic="or"`) attested of `[vnclass, Theme]` | `[leave-51.2, Theme]` (`vnrole`), `[[leave-51.2, Theme], [+animate]]` (`Batch 2` recipe gap: `classes.recipe` currently uses `thing THEMROLE type` without `within`, colliding selectional restrictions onto global `Theme`) | "Selectional restrictions further specify semantic roles ... within each class" (`VerbNet_Guidelines.pdf`) |
| `<FRAME>` (`DESCRIPTION`, `EXAMPLES`, `SYNTAX`, `SEMANTICS`) | under `FRAMES` | syntactic-semantic frame (`thing FRAME .`), holding `primary`/`secondary` phrase patterns, `EXAMPLE` sentences, `SYNTAX` (`NP` → `vnrole`), and `SEMANTICS` (`PRED` value/negation `bool="!"` and typed `ARG` tuples) | `[leave-51.2, syntactic frame, frame]`, `[frame, primary frame name, …]`, `[frame, example sentence, …]`, structured `PRED(ARG...)` semantics | "The syntactic frames in VerbNet provide a description of the different surface realizations…" |
| `xmlns:xsi`, `xsi:noNamespaceSchemaLocation`, `verbnet_key`, `xtag`, `descriptionNumber` | XML schema & internal pointers | omitted (`omit`) | none | XML plumbing and internal cross-references |

## Relations

`classes.recipe` already maps `VNSUBCLASS`, `MEMBER`, `FRAME`, `DESCRIPTION.primary`, `DESCRIPTION.secondary`, and `EXAMPLE` onto documented VerbNet relations (`subclass`, `verb member`, `syntactic frame`, `primary frame name`, `example sentence`) and registers `vnclass` and `vnrole` slots plus `vnclass`→`ili` and `vnclass`→`fnframe` highway edges. Closing the `Batch 2` gaps scopes `THEMROLE` and `MEMBER` via `within` (`[vnclass, role]` and `[vnclass, verb]`), groups each `<SELRESTR Value="+" type="animate"/>` and `<PRED>`/`<ARG>` tuple intact, and resolves `wn` sense keys to `[lemma, eng, ILI]` lexicalization strands.
