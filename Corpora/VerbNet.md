# VerbNet

VerbNet attests what a class file says of each class, subclass, thematic role and member; a class is its ID as VerbNet writes it, a role its type, a member the verb it names; a member's `verbnet_key` is VerbNet's pointer to the member, read by nothing (`omit`, with `xtag` and `descriptionNumber`); its `grouping` and `fn_mapping` are PropBank rolesets and a FrameNet frame by their highway IDs, content as written, and its `wn` WordNet senses by their sense keys, each attested of the member in its class; the schema and README attest nothing.

One source reads VerbNet: the class files of VerbNet 3.4, "their members, thematic roles and frames", by [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe). The classes and roles are the highway's `vnclass` (609) and `vnrole` (39, a mask field) lists ([Types](../Reference/Types.md)), a class a highway node exactly as an ILI is, a concept node of the linguistic superhighway; the members' mappings are its edges ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `verbnet` | `VerbNet` | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `verbnet3.4` | [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe) |

## The class file

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<VNCLASS ID="leave-51.2">` | the root | the class, its ID as written: the highway's type; the subject of what the file says | | `vn_schema-3.xsd` |
| `<VNSUBCLASS ID="leave-51.2-1">` | under `SUBCLASSES` | the subclass, the same way; its place in the class | `[leave-51.2, VNSUBCLASS, leave-51.2-1]` | "VerbNet subclasses inherit features from the top class" |
| `<MEMBER name="abandon" wn="abandon%2:40:00 abandon%2:38:00" grouping="abandon.01" fn_mapping="None" verbnet_key="abandon#1">` | under `MEMBERS` | the member is the verb its `name` writes; its place in the class; `wn`, `grouping` and `fn_mapping` said of the member in this class, never of the verb wherever it occurs: the rolesets and frame by their highway IDs, content as written, each a highway node the highway holds a slot for (`type grouping pbroleset`, `type fn_mapping fnframe`; `None` names no frame and says nothing); the sense keys, WordNet's internal pointers to lexicalizations, resolved through the highway perf-cache and recorded nowhere (as built, read as the concepts they resolve to, `type wn ili`); `verbnet_key` a pointer, read by nothing | `[leave-51.2, MEMBER, abandon]`, as built `[[leave-51.2, abandon], wn, concept]`, in the target the lexicalization strand in place of the concept, `[[leave-51.2, abandon], grouping, abandon.01]` | "Contains the list of verbs belonging to a specific class or subclass." |
| `<THEMROLE type="Theme">` | under `THEMROLES` | the role, its type: the highway's `vnrole`; its place in the class; its restrictions said of it | `[leave-51.2, THEMROLE, Theme]`, `[Theme, Value, +]`, `[Theme, type, animate]` | "Thematic roles refer to the semantic relationship between a predicate and its arguments." |
| `<FRAME>` with `DESCRIPTION`, `EXAMPLES`, `SYNTAX`, `SEMANTICS` | under `FRAMES` | of the class: each attribute under its name, each example's text under `EXAMPLE`; the frame one record | `[leave-51.2, primary, NP V NP.initial_location]`, `[leave-51.2, EXAMPLE, He deserted his post.]`, `[leave-51.2, value, has_location]` | "The syntactic frames in VerbNet provide a description of the different surface realizations…" |
| `xmlns:xsi`, `xsi:noNamespaceSchemaLocation` | on the root | XML's own plumbing: nothing | nothing | |
| an empty attribute value | | nothing | nothing | |

A thing's own attributes are one record, witnessed once; an element that is no thing is one record of what it says. Nothing is renamed, reordered, or filled in: what the file says of a frame is said of the class, under the attribute's name, because the recipe names no other thing for it to be said of.

## Relations

As built, the relation of a claim above is the name of the field that carries its value: the element's or attribute's name. That is markup, not meaning. A relation is what the source means, resolved through the road classes, never the name of a field, column, attribute, or layer: a tagset value is a value of its tagset with its attested equivalence, a per-span label belongs in the sentence's annotation layer, and a pointer's attribute name is in no claim, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field).

| Claim, as built | Its relation, as built | What it means: the target |
| --- | --- | --- |
| `[leave-51.2, VNSUBCLASS, leave-51.2-1]` | the element's name | the subclass of the class, which inherits its features, "VerbNet subclasses inherit features from the top class" |
| `[leave-51.2, MEMBER, abandon]` | the element's name | the verb is a member of the class |
| `[[leave-51.2, abandon], wn, concept]` | the attribute's name, `wn` | the WordNet sense the member has in the class: the lexicalization its sense key points at, the key resolved and in no claim |
| `[[leave-51.2, abandon], grouping, abandon.01]`, `fn_mapping` | the attribute's name | a highway mapping of the member in its class to that PropBank roleset or FrameNet frame: an interchange strand |
| `[leave-51.2, THEMROLE, Theme]` | the element's name | the class has the thematic role, "the semantic relationship between a predicate and its arguments" |
| `[Theme, Value, +]`, `[Theme, type, animate]` | the attributes' names | one selectional restriction on the role in that class, `+animate`, the two values together |
| `[leave-51.2, primary, NP V NP.initial_location]`, `[leave-51.2, EXAMPLE, …]`, `[leave-51.2, value, has_location]` | the attribute's or element's name | of the frame, not the class: its primary description, its example, and a predicate of its semantics, as VerbNet documents its frames |

## Not read

`vn_schema-3.xsd` and the README match no recipe and are not read.
