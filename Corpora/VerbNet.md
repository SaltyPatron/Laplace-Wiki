# VerbNet

VerbNet attests what a class file says of each class, subclass, and member, everything else in the file speaking of the class it is inside, and the schema and README attest nothing.

One source reads VerbNet: the class files of VerbNet 3.4, "their members, thematic roles and frames". Each file is XML, read as what it says: the recipe names three elements as things, and says of the rest that "everything else speaks of the class it is inside". The project's guidelines are the [VerbNet Annotation Guidelines](https://verbs.colorado.edu/verb-index/VerbNet_Guidelines.pdf).

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `verbnet` | `VerbNet` | deviation 90 | `unicode`, `iso-639` | `*.xml` under `verbnet3.4` | [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The class file

A class file is one `VNCLASS` element. "A class and a subclass are their IDs and a member its key; everything else speaks of the class it is inside." A class, a subclass, and a member are named as written, with no kind before the name. Every predicate is an attribute's or an element's name as the file writes it, so `type` on a `THEMROLE`, on a `SELRESTR`, and on an `ARG` is the one predicate `type`, and `value` on an `NP` and on a `PRED` is the one predicate `value`.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<VNCLASS ID="...">` | the root of a class file | the class, named by its ID as written: the subject of everything in the file | the first part of every claim of the class | "VerbNet expands upon Levin's classification of shared syntactic alternations by making the relationships between syntax and semantics explicit." Guidelines; `vn_schema-3.xsd` gives `VNCLASS` the attribute ID |
| `<VNSUBCLASS ID="...">` | under a class's `SUBCLASSES` | the subclass, named by its ID; its place in the class; everything inside it speaks of the subclass | `[class, VNSUBCLASS, subclass]` | "VerbNet subclasses inherit features from the top class but specify further syntactic and semantic commonalities amongst their verb members." Guidelines |
| `<MEMBER name="..." wn="..." grouping="..." fn_mapping="..." verbnet_key="..." features="...">` | under `MEMBERS` | the member, named by its `verbnet_key`; its place in the class; every other attribute said of it under its name; together, one record | `[class, MEMBER, member]`, `[member, name, value]`, `[member, wn, value]`, `[member, grouping, value]`, `[member, fn_mapping, value]`, `[member, features, value]` | "Contains the list of verbs belonging to a specific class or subclass." Guidelines; `vn_schema-3.xsd`: name, wn, grouping, fn_mapping, verbnet_key, features. `wn` and `fn_mapping` are recorded as the member's fields: not a [Wordnets](Wordnets.md) or [FrameNet](FrameNet.md) attestation |
| `<THEMROLE type="Agent">` | under `THEMROLES` | no thing: `type` is said of the class; the role and its restrictions are one record | `[class, type, Agent]` | "Thematic roles refer to the semantic relationship between a predicate and its arguments." Guidelines; `vn_schema-3.xsd` themRoleType |
| `<SELRESTRS logic="...">` holding `<SELRESTR Value="+" type="animate">` | inside a THEMROLE, or inside an NP of a frame's syntax | of the class: `logic`, `Value`, and `type` each under its name | `[class, logic, value]`, `[class, Value, +]`, `[class, type, animate]` | "Each thematic role listed in a class may optionally be further characterized by certain selectional restrictions, which provide more information about the nature of a given role." Guidelines; `vn_schema-3.xsd` selrestrType |
| `<FRAME>` with `<DESCRIPTION descriptionNumber="..." primary="..." secondary="..." xtag="...">` | under `FRAMES` | of the class: each attribute of the description under its name; the frame's description, examples, syntax, and semantics are one record | `[class, descriptionNumber, value]`, `[class, primary, value]`, `[class, secondary, value]`, `[class, xtag, value]` | "The syntactic frames in VerbNet provide a description of the different surface realizations and diathesis alternations allowed for the members of the class." Guidelines |
| `<EXAMPLE>` | the text under a frame's `EXAMPLES` | of the class, under the element's name | `[class, EXAMPLE, text]` | `vn_schema-3.xsd`: EXAMPLES/EXAMPLE |
| `<SYNTAX>` with `<NP value="...">`, `<VERB/>`, `<PREP value="...">`, `<LEX value="...">`, `<ADV>`, `<ADJ>` and their `SYNRESTRS` | inside a frame | of the class: each `value` under `value`; a `SYNRESTR` as a `SELRESTR` above; an element with no attribute and no text says nothing | `[class, value, Agent]`, `[class, Value, +]`, `[class, type, value]` | `vn_schema-3.xsd`: NP, ADV, ADJ, PREP, LEX, then VERB, then NP, ADV, ADJ, PREP, LEX |
| `<SEMANTICS>` with `<PRED value="..." bool="...">` holding `<ARGS><ARG type="..." value="..."/></ARGS>` | inside a frame | of the class: `value` and `bool` of the predicate, `type` and `value` of each argument, each under its name | `[class, value, motion]`, `[class, bool, !]`, `[class, type, ThemRole]`, `[class, value, Agent]` | "The underlying components of meaning of an event and its participants are revealed in semantic predicates under the Frames section in a verb class." Guidelines; `vn_schema-3.xsd`: PRED (bool, value), ARG (type, value) |
| `<MEMBERS>`, `<THEMROLES>`, `<FRAMES>`, `<SUBCLASSES>` | wrappers without attributes | structure: `MEMBERS` and `SUBCLASSES` hold things and are the record of their places; `THEMROLES` and `FRAMES` only hold | nothing of their own | `vn_schema-3.xsd`: MEMBERS, THEMROLES, FRAMES, SUBCLASSES |
| an empty attribute value | what the file leaves empty | nothing | none | |

A thing's own attributes are one record, witnessed once. An element that is no thing is one record: the path of its name, its claims, and the records of the elements inside it. A claim that stands alone is its own record. Nothing is renamed, reordered, or filled in: what the file says of a role, a restriction, a frame, or a predicate is said of the class, under the attribute's name, because the recipe names no other thing for it to be said of.

## Not read

`vn_schema-3.xsd` and the README match no recipe and are not read: the schema is the specification cited above, and nothing on this page is attested by it.
