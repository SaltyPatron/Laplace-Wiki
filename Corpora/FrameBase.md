# FrameBase

FrameBase attests every statement of its three Turtle schema files as written, an identifier without its angle brackets and a text with its language tag or datatype, and statements of blank nodes and collections are not read.

One source reads FrameBase 2.0, "the schema (core), its lemon annotations, and its links to WordNet 3.0, in Turtle". The three files are read as Turtle, "one statement on every line, every identifier written in full between angle brackets", through the shared Turtle recipe. The publisher describes the files at [FrameBase data](https://www.framebase.org/data) and the schema at [FrameBase schema](https://www.framebase.org/schema). FrameBase is a hop between lexicons, as [Hops](Hops.md) lists it, and it is not FrameNet: its files hold the schema, not FrameNet's sentences.

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `framebase` | `FrameBase` | class `AcademicCurated` | `unicode`, `iso-639` | `FrameBase_schema_*.ttl.gz` under `FrameBase-2.0` | [`schema.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/framebase/schema.recipe), which reads like [`turtle.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/turtle.recipe) |

The witness is named as the source says: "The set has no README on this machine. The name is the one its files carry (FrameBase_schema_*.ttl.gz) and the one of the host of its identifiers (`http://framebase.org/`)." The class is the witness's trust class, one of those [6. Registries](../Sequence/Registries.md#65-declare-the-trust-classes) declares; its prior is the trust every attestation of the source plays at, and [9. Sources](../Sequence/Sources.md#the-estate-and-why-each-source-is-in-it) gives the class of each source.

## The schema files

"Every statement is recorded as written: [subject, predicate, object]." The three files are the core schema, "RDFS+ schema for representing frame-based knowledge"; the "Lemon annotations for the schema"; and the WordNet links, "owl:sameAs links with the RDF version of WordNet".

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| a statement | `<subject> <predicate> <object> .` | the claim of its three terms, each as what it stands for | `[http://wordnet-rdf.princeton.edu/wn30/01895612-v, http://www.w3.org/2002/07/owl#sameAs, http://framebase.org/frame/Synset01895612.waltz.verb]` | "`owl:sameAs` links with the RDF version of WordNet." [FrameBase data](https://www.framebase.org/data) |
| an identifier between angle brackets | `<http://framebase.org/frame/Closure.button.verb>` | the identifier without its brackets, in whichever of the three places it stands; it is recorded whole, never parted into the path the schema page's encoding describes | a part of the claim | "FrameBase's RDFS schema declares classes for each frame in FrameNet." "Outgoing properties for each frame element." [FrameBase schema](https://www.framebase.org/schema): `http://framebase.org/frame/`, `http://framebase.org/fe/`, `http://framebase.org/meta/` |
| a name written with a prefix, and `a` | `owl:sameAs`, `a` | as written: a prefixed name keeps its prefix, and `a` is recorded as the `a` the file writes | a part of the claim | the schema files write every identifier in full |
| a quoted text | `"..."` | the text without its quotes, with its escapes resolved | `[subject, predicate, text]` | |
| a language tag on a text | `"..."@en` | the pair of the text and its tag, a claim of its own | `[text, en]` | |
| a datatype on a text | `"..."^^<type>` | the pair of the text and its datatype | `[text, type]` | |
| a number, a boolean | `1`, `true` | as written | a part of the claim | |
| the statements of a blank node | `[ ... ]`, `_:name` | not read: "statements of a node the file does not name" | nothing | |
| a collection | `( ... )` | not read | nothing | |

Each statement is a claim of its own, witnessed once. Nothing is renamed, reordered, or filled in: a predicate of the lemon file under `http://lemon-model.net/lemon#` or `http://www.lexinfo.net/ontology/2.0/lexinfo#` is recorded as that identifier, and a class under `http://framebase.org/meta/`, such as `LuMicroframe`, `SynsetMicroframe`, or `Miniframe`, is what the file says of a subject, not a kind Laplace gives it.

## Not read

Nothing under the root but the three schema files matches a recipe, and the source names no `reads`: no other file is read. The schema page's own encoding of an identifier's path is not applied: an identifier is one entity, as written.
