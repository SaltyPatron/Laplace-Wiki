# PropBank

PropBank attests what each frame file says of its predicates, highway rolesets (`abandon.01`), roleset-scoped argument slots (`[abandon.01, 0]`), multi-word predications, VerbNet and FrameNet links, and annotated example sentences, while the DTD and usage bookkeeping attest nothing.

One source reads Unified PropBank frame files ("every predicate's rolesets, their numbered and adjunct roles, and their links to VerbNet and FrameNet") via [`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe). Rolesets populate the highway's `pbroleset` road class (`11,208` highway nodes anchored directly on their PropBank ID `abandon.01`, [Types](../Reference/Types.md)), and `<rolelink>` / `<lexlink>` elements supply `pbroleset`↔`vnclass` and `pbroleset`↔`fnframe` edges ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `propbank` | `PropBank` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `frames` | [`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe) |

## The frame file (`frames.recipe`)

[`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe) anchors rolesets directly on `id` (`thing roleset id`, e.g., `abandon.01`), scopes numbered roles strictly to their parent roleset (`thing role resolved ^roleset/id required n required`, so `ARG0` of `abandon.01` never collides with `ARG0` of `eat.01`), and omits release-usage and character-offset bookkeeping (`omit usagenotes inuse version confidence src start end relloc note`):

| Piece | Written as | Laplace reads it as | Attestation recorded | Specification |
| --- | --- | --- | --- | --- |
| `<predicate lemma="abandon">` | inside `<frameset>` | predicate lemma (`thing predicate lemma`) holding its rolesets | `[abandon, sense, abandon.01]` | `frameset.dtd` |
| `<roleset id="abandon.01" name="leave behind">` | inside `<predicate>` | `pbroleset` highway node `abandon.01` (`thing roleset id`, `types pbroleset`, `keyed pbroleset roleset id`), with `name` attested as its gloss | `[abandon.01, sense description, leave behind]` | "Multiple rolesets per predicate are necessary for the accommodation of different senses" |
| `<alias pos="v">abandon</alias>`, `<argalias>` | under `<aliases>` | evoking word and POS (`propbank-pos` crosswalked to `upos` for `r`/`p`/`v`/`n`/`j`, preserving undocumented `l`/`x`/`m`/`d`/`f` source codes without fabricating UPOS tags) | `[abandon.01, abandon]`, `upos` slot | `frameset.dtd` |
| `<role n="0" f="PPT" descr="abandoner">` | under `<roles>` | roleset-scoped argument slot `[abandon.01, 0]` (`thing role resolved ^roleset/id required n required`) with function tag `f` and mnemonic `descr` | `[abandon.01, argument slot, [abandon.01, 0]]`, `[[abandon.01, 0], mneumonic, abandoner]`, `f` (`PPT`, `PAG`, `LOC`, ...) | "Roles have a number … labeled with the function tags" |
| `<rolelink class="leave-51.2" resource="VerbNet">theme</rolelink>`, `<lexlink class="Departing" resource="FrameNet"/>` | under `<role>` or `<roleset>` | VerbNet `vnclass` (`leave-51.2`) and `vnrole` (`theme`), or FrameNet `fnframe` (`Departing`) highway links | `[role_or_roleset, leave-51.2]`, `[role, theme]`, `[roleset, Departing]` + `maps` highway edges | VerbNet and FrameNet crosswalks |
| `<mwp-descriptions>` (`<syntaxdesc>`, `<token>`, `<mapping>`) | multi-word predications | roleset-scoped multi-word predication syntax and source/target slot mappings | `multi-word predication`, `syntactic description`, `source representation`, `target representation` | Unified PropBank MWP |
| `<example name="..."><text>And they believe…</text><propbank><rel>abandoned</rel><arg type="ARG0">the Big Board</arg></propbank></example>` | inside `<roleset>` | canonical sentence `text` (`thing example text`), predicate `rel`, and `ARG0..ARG7`/`ARGM-*` spans resolved onto `[roleset, n]` (`refer arg.type role under ^roleset/id`) | `[example, predicate, abandoned]`, `[example, [abandon.01, 0], the Big Board]` (with sentence-aligned span layer refinement in `Batch 2`) | `frameset.dtd` |
| `<usagenotes>`, `inuse`, `version`, `confidence`, `src`, `start`, `end`, `relloc` | XML packaging & token offsets | omitted (`omit`) | none | release bookkeeping and local offsets |

## Relations

`frames.recipe` already anchors `roleset` on `abandon.01`, scopes `role` to `[^roleset/id, n]`, resolves `ARG0..9` onto those roleset-scoped slots rather than a universal Agent/Patient, crosswalks `alias.pos` to `upos`, and maps XML elements onto `frameset.dtd` semantic relations (`sense`, `sense description`, `argument slot`, `mneumonic`, `predicate`). `frameset.dtd` and release guidelines are schema/documentation files outside the frame XML stream.
