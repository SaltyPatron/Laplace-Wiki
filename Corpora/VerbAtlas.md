# VerbAtlas

VerbAtlas attests what its tables say of a frame, a selectional preference, and a synset: a frame is its name, the type the highway lists from `VA_frame_info.tsv`, and its id (`va:0001f`) a key; a BabelNet or WordNet synset id is read as the ILI concept it is the key of; and the mapping files the package ships are the highway's input, read by no recipe.

One source reads VerbAtlas 1.1.0, "WordNet synsets clustered into frames", by one recipe per file under [`recipes/verbatlas`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/verbatlas). The frames are the highway's `vaframe` list (432); `bn2wn.tsv` gives the highway the `bn:` and `wn:` spellings of each ILI concept, `VA_bn2va.tsv` and `pb2va.tsv` its edges to the frames ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `verbatlas` | `VerbAtlas 1.1.0`, "named as the README's title names it" | class `AcademicCurated` | `unicode`, `iso-639` | the `.tsv` files under `VerbAtlas-1.1.0` | one per file read |

## The files

| File | Piece | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `VA_frame_info.tsv` | ID; name; definition; prototypical synset; its definition; small definition | the frame the id is the key of (`type ID vaframe`), whose content is its name; the definitions said of it; the prototypical synset read as the ILI concept (`type prototypical_synset ili`) | `[TOLERATE, definition, An agent TOLERATES a theme …]`, `[TOLERATE, prototypical_synset, concept]`, `[TOLERATE, small_definition, Tolerate, accept, endure.]` | README, FORMAT 1 |
| `VA_frame_pas.tsv` | the frame's id, then its roles | the row itself: the frame, then the roles in order | `[TOLERATE, Agent, Theme, Beneficiary, Attribute]` | FORMAT 2 |
| `VA_preference_info.tsv` | ID; reference BabelNet synset; name; a fourth, unnamed field | the preference is its name; its id a key; the synset read as the concept; the fourth field a pair with the name | `[absorbent, reference_BabelNet_synset_ID, concept]`, `[absorbent, https://upload.wikimedia.org/…]` | FORMAT 5 |
| `VA_bn2shadow.tsv`, `VA_bn2implicit.tsv` | synset; role; filler synsets parted by `\|` | the synsets read as concepts; the row says together that the synset has the role as a shadow or implicit argument (the file's name) and what fills it | `[concept, shadow, Stimulus]`, `[concept, Stimulus, concept]` | FORMATS 6, 7 |
| `VA_synset_preferences.tsv` | synset; class | the concept and its preference class, a pair | `[concept, CONCRETE]` | |
| `wn2lemma.tsv` | WordNet synset; lemma | the concept, and its lemma | `[concept, lemma, breathe]` | FORMAT 10 |
| `bn2wn.tsv`, `VA_bn2va.tsv`, `pb2va.tsv`, `wn2sense.tsv` | keys and keys | the highway's input: not read here | nothing | FORMATS 4, 8, 9, 11 |
| `VA_va2sp.tsv` | a frame, then roles and preference ids | names preferences only by their ids, keys of another file's rows: not read | nothing | FORMAT 3 |
| every file | an empty field | nothing | nothing | |

The first line of each `VA_*.tsv` file is a licence line, passed over. `README.txt` is not read: the source has no `reads` line and no recipe of its own matches it.
