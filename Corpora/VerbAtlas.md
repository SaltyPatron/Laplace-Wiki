# VerbAtlas

VerbAtlas attests what its tables say of a frame, a selectional preference, and a synset: a frame is its name, the type the highway lists from `VA_frame_info.tsv`, and its id (`va:0001f`) VerbAtlas's identifier of it, content attested of it; a BabelNet or WordNet synset id is content, an identifier the highway maps to the ILI concept it names; and the mapping files the package ships are read too: those that pair a synset or a roleset with a frame attest the pair, and those that only pair one identifier with another give the highway its aliases.

One source reads VerbAtlas 1.1.0, "WordNet synsets clustered into frames", by one recipe per file under [`recipes/verbatlas`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/verbatlas). The frames are the highway's `vaframe` list (432); `bn2wn.tsv` gives the highway the `bn:` and `wn:` spellings of each ILI concept, `VA_bn2va.tsv` and `pb2va.tsv` its edges to the frames ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `verbatlas` | `VerbAtlas 1.1.0`, "named as the README's title names it" | class `AcademicCurated` | `unicode`, `iso-639` | the `.tsv` files under `VerbAtlas-1.1.0` | one per file read |

## The files

| File | Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `VA_frame_info.tsv` | ID; name; definition; prototypical synset; its definition; small definition | the frame, which is its name (`thing row name`), a type of the highway's `vaframe` list (`types`, `keyed … ID`); its id VerbAtlas's identifier of it, content as written, said of it (`key row ID`, which as built records nothing of it); the definitions said of it; the prototypical synset read as the ILI concept (`type prototypical_synset ili`) | `[TOLERATE, ID, va:…]`, `[TOLERATE, definition, An agent TOLERATES a theme …]`, `[TOLERATE, prototypical_synset, concept]`, `[TOLERATE, small_definition, Tolerate, accept, endure.]` | README, FORMAT 1 |
| `VA_frame_pas.tsv` | the frame's id, then its roles | the row itself: the frame, then the roles in order | `[TOLERATE, Agent, Theme, Beneficiary, Attribute]` | FORMAT 2 |
| `VA_preference_info.tsv` | ID; reference BabelNet synset; name; a fourth, unnamed field | the preference is its name; its id VerbAtlas's identifier of it, content said of it; the synset read as the concept; the fourth field a pair with the name | `[absorbent, reference_BabelNet_synset_ID, concept]`, `[absorbent, https://upload.wikimedia.org/…]` | FORMAT 5 |
| `VA_bn2shadow.tsv`, `VA_bn2implicit.tsv` | synset; role; filler synsets parted by `\|` | the synsets read as concepts; the row says together that the synset has the role as a shadow or implicit argument (the file's name) and what fills it | `[concept, shadow, Stimulus]`, `[concept, Stimulus, concept]` | FORMATS 6, 7 |
| `VA_synset_preferences.tsv` | synset; class | the concept and its preference class, a pair | `[concept, CONCRETE]` | |
| `wn2lemma.tsv` | WordNet synset; lemma | the concept, and its lemma | `[concept, lemma, breathe]` | FORMAT 10 |
| `VA_bn2va.tsv` | BabelNet synset; frame id | the synset read as its concept, paired with the frame; an edge `ili`→`vaframe` | `[concept, frame]` | FORMAT 4 |
| `pb2va.tsv` | `roleset>frame`, then `argument>role` parts | the roleset, paired with the frame; each argument's role said of the roleset; an edge `pbroleset`→`vaframe` | `[roleset, frame]`, `[roleset, A0, Agent]` | FORMAT 9 |
| `bn2wn.tsv`, `wn2sense.tsv` | identifiers and identifiers | each row says that one identifier names what the other names, both content as written; it gives the highway an `alias` of the `ili` list; as built both columns are omitted and nothing is recorded | `[bn:…, wn:…]` as the edge VerbAtlas attests | FORMATS 8, 11 |
| `VA_va2sp.tsv` | a frame, then its type, then roles and the preferences each takes | the frame (`type frame vaframe`); its type said of it; each role related to its preferences, read as the preferences `VA_preference_info.tsv` names (`refer`), together as one record | `[frame, type, C]`, `[frame, role, preference]` | FORMAT 3 |
| every file | an empty field | nothing | nothing | |

The first line of each `VA_*.tsv` file is a licence line, passed over. `README.txt` is not read: the source has no `reads` line and no recipe of its own matches it.
