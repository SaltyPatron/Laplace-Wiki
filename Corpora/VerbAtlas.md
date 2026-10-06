# VerbAtlas

VerbAtlas attests what its tables say of a frame, a selectional preference, and a synset: a frame is a highway node, the type the highway lists from `VA_frame_info.tsv`, whose id (`va:0001f`) is VerbAtlas's identifier of it, content, and as built it is its name; a BabelNet or WordNet synset id is a pointer, read as the ILI concept it resolves to and recorded nowhere; and the mapping files the package ships are read too: those that pair a synset or a roleset with a frame attest the pair, and those that only pair one pointer with another give the highway its aliases.

One source reads VerbAtlas 1.1.0, "WordNet synsets clustered into frames", by one recipe per file under [`recipes/verbatlas`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/verbatlas). The frames are the highway's `vaframe` list (432), highway nodes exactly as an ILI is, concept nodes of the linguistic superhighway; as built a frame is its name, and the target is the frame as the content of its highway ID; `bn2wn.tsv` gives the highway the `bn:` and `wn:` spellings of each ILI concept, `VA_bn2va.tsv` and `pb2va.tsv` its edges to the frames ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `verbatlas` | `VerbAtlas 1.1.0`, "named as the README's title names it" | class `AcademicCurated` | `unicode`, `iso-639` | the `.tsv` files under `VerbAtlas-1.1.0` | one per file read |

## The files

| File | Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `VA_frame_info.tsv` | ID; name; definition; prototypical synset; its definition; small definition | the frame, which is its name (`thing row name`), a type of the highway's `vaframe` list (`types`, `keyed … ID`); its id VerbAtlas's identifier of it, a highway ID, content as written, the frame's identity in the target (as built `key row ID` resolves it and records nothing of it); the definitions said of it; the prototypical synset read as the ILI concept (`type prototypical_synset ili`) | `[TOLERATE, definition, An agent TOLERATES a theme …]`, `[TOLERATE, prototypical_synset, concept]`, `[TOLERATE, small_definition, Tolerate, accept, endure.]` | README, FORMAT 1 |
| `VA_frame_pas.tsv` | the frame's id, then its roles | the row itself: the frame, then the roles in order | `[TOLERATE, Agent, Theme, Beneficiary, Attribute]` | FORMAT 2 |
| `VA_preference_info.tsv` | ID; reference BabelNet synset; name; a fourth, unnamed field | the preference is its name; its id a pointer, recorded nowhere; the synset read as the concept; the fourth field a pair with the name | `[absorbent, reference_BabelNet_synset_ID, concept]`, `[absorbent, https://upload.wikimedia.org/…]` | FORMAT 5 |
| `VA_bn2shadow.tsv`, `VA_bn2implicit.tsv` | synset; role; filler synsets parted by `\|` | the synsets read as concepts; the row says together that the synset has the role as a shadow or implicit argument (the file's name) and what fills it | `[concept, shadow, Stimulus]`, `[concept, Stimulus, concept]` | FORMATS 6, 7 |
| `VA_synset_preferences.tsv` | synset; class | the concept and its preference class, a pair | `[concept, CONCRETE]` | |
| `wn2lemma.tsv` | WordNet synset; lemma | the concept, and its lemma | `[concept, lemma, breathe]` | FORMAT 10 |
| `VA_bn2va.tsv` | BabelNet synset; frame id | the synset read as its concept, paired with the frame; an edge `ili`→`vaframe` | `[concept, frame]` | FORMAT 4 |
| `pb2va.tsv` | `roleset>frame`, then `argument>role` parts | the roleset, paired with the frame; each argument's role said of the roleset; an edge `pbroleset`→`vaframe` | `[roleset, frame]`, `[roleset, A0, Agent]` | FORMAT 9 |
| `bn2wn.tsv`, `wn2sense.tsv` | pointers and pointers | both columns omitted: each row gives the highway an `alias` of the `ili` list, one pointer for another; as built that includes `wn2sense.tsv`'s sense keys, so a sense key resolves to the concept, where in the target it resolves to the lexicalization strand it points at | nothing | FORMATS 8, 11 |
| `VA_va2sp.tsv` | a frame, then its type, then roles and the preferences each takes | the frame (`type frame vaframe`); its type said of it; each role related to its preferences, read as the preferences `VA_preference_info.tsv` names (`refer`), together as one record | `[frame, type, C]`, `[frame, role, preference]` | FORMAT 3 |
| every file | an empty field | nothing | nothing | |

`VA_bn2va.tsv` and `pb2va.tsv` are mappings: each row is one interchange strand, where a route changes road class, with the argument-to-role pairs said within it, never a claim per column.

The first line of each `VA_*.tsv` file is a licence line, passed over. `README.txt` is not read: the source has no `reads` line and no recipe of its own matches it.

## Relations

As built, the relation of a claim above is the name of the field that carries its value: the README format's field name, or the file's name. That is markup, not meaning. A relation is what the source means, resolved through the road classes, never the name of a field, column, attribute, or layer: a tagset value is a value of its tagset with its attested equivalence, a per-span label belongs in the sentence's annotation layer, and a pointer's attribute name is in no claim, [10. Recipes](../Sequence/Recipes.md#1011-disposition-every-recovered-field).

| Claim, as built | Its relation, as built | What it means: the target |
| --- | --- | --- |
| `[TOLERATE, definition, …]`, `small_definition` | the field's name | the frame's definition and short definition, as the README's formats document them |
| `[TOLERATE, prototypical_synset, concept]` | the field's name | the frame's prototypical concept: a highway mapping |
| `[TOLERATE, Agent, Theme, Beneficiary, Attribute]` | none: the row's own shape | already meaning: the frame's roles in order |
| `[absorbent, reference_BabelNet_synset_ID, concept]` | the field's name | the concept the selectional preference refers to |
| `[absorbent, https://upload.wikimedia.org/…]` | none: an unnamed field | what VerbAtlas documents the field to be; until it does, an explicit unresolved obligation |
| `[concept, shadow, Stimulus]`, `[concept, Stimulus, concept]` | the file's name, `shadow` or `implicit`; the role | the concept's role as a shadow or implicit argument, and what fills it, as FORMATS 6 and 7 document |
| `[concept, CONCRETE]`, `[concept, frame]`, `[roleset, frame]` | none: pairs | mappings, already interchange strands |
| `[concept, lemma, breathe]` | the field's name | a lexicalization of the concept |
| `[roleset, A0, Agent]` | the argument | already meaning: the PropBank argument maps to the VerbAtlas role |
| `[frame, type, C]`, `[frame, role, preference]` | the field's name; the role | the frame's type as FORMAT 3 documents it; the role's selectional preference |
