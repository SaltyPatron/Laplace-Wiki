# VerbNet

VerbNet attests what a class file says of each class, subclass, thematic role and member; a class is its ID as VerbNet writes it, a role its type, a member the verb it names; a member's `verbnet_key` is bookkeeping, read by nothing (`omit`, with `xtag` and `descriptionNumber`), and its `wn`, `grouping` and `fn_mapping` are read as the WordNet senses, PropBank rolesets and FrameNet frame they are those resources' keys of; the schema and README attest nothing.

One source reads VerbNet: the class files of VerbNet 3.4, "their members, thematic roles and frames", by [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe). The classes and roles are the highway's `vnclass` (609) and `vnrole` (39, a mask field) lists ([Types](../Reference/Types.md)); the members' mappings are its edges ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `verbnet` | `VerbNet` | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `verbnet3.4` | [`classes.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/verbnet/classes.recipe) |

## The class file

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<VNCLASS ID="leave-51.2">` | the root | the class, its ID as written: the highway's type; the subject of what the file says | | `vn_schema-3.xsd` |
| `<VNSUBCLASS ID="leave-51.2-1">` | under `SUBCLASSES` | the subclass, the same way; its place in the class | `[leave-51.2, VNSUBCLASS, leave-51.2-1]` | "VerbNet subclasses inherit features from the top class" |
| `<MEMBER name="abandon" wn="abandon%2:40:00 abandon%2:38:00" grouping="abandon.01" fn_mapping="None" verbnet_key="abandon#1">` | under `MEMBERS` | the member is the verb its `name` writes; its place in the class; `wn` the ILI concepts the sense keys resolve to, `grouping` the rolesets, `fn_mapping` the frame (`type wn ili`, `type grouping pbroleset`, `type fn_mapping fnframe`; `None` names no frame and says nothing); `verbnet_key` bookkeeping, read by nothing | `[leave-51.2, MEMBER, abandon]`, `[abandon, wn, concept]`, `[abandon, grouping, [abandon, leave behind]]` | "Contains the list of verbs belonging to a specific class or subclass." |
| `<THEMROLE type="Theme">` | under `THEMROLES` | the role, its type: the highway's `vnrole`; its place in the class; its restrictions said of it | `[leave-51.2, THEMROLE, Theme]`, `[Theme, Value, +]`, `[Theme, type, animate]` | "Thematic roles refer to the semantic relationship between a predicate and its arguments." |
| `<FRAME>` with `DESCRIPTION`, `EXAMPLES`, `SYNTAX`, `SEMANTICS` | under `FRAMES` | of the class: each attribute under its name, each example's text under `EXAMPLE`; the frame one record | `[leave-51.2, primary, NP V NP.initial_location]`, `[leave-51.2, EXAMPLE, He deserted his post.]`, `[leave-51.2, value, has_location]` | "The syntactic frames in VerbNet provide a description of the different surface realizations…" |
| `xmlns:xsi`, `xsi:noNamespaceSchemaLocation` | on the root | XML's own plumbing: nothing | nothing | |
| an empty attribute value | | nothing | nothing | |

A thing's own attributes are one record, witnessed once; an element that is no thing is one record of what it says. Nothing is renamed, reordered, or filled in: what the file says of a frame is said of the class, under the attribute's name, because the recipe names no other thing for it to be said of.

## Not read

`vn_schema-3.xsd` and the README match no recipe and are not read.
