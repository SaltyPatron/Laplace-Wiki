# PropBank

PropBank attests what a frame file says of each predicate and roleset: a predicate is its lemma, a roleset is a highway node whose id (`abandon.01`) is PropBank's identifier of it, a highway ID, content as written on which every source that cites it lands, and as built the roleset is the predicate's lemma and the name PropBank writes for it; the aliases, roles, links, notes and examples of a roleset speak of it, an example being its text; and the DTD and guidelines attest nothing.

One source reads PropBank: its frame files, "every predicate's rolesets, their roles, and their links to VerbNet and FrameNet", by [`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe). The rolesets are the highway's `pbroleset` list (11,208; [Types](../Reference/Types.md)), each, as built, the content `[lemma, name]`, as a frame element is its frame and name; a roleset is a highway node exactly as an ILI is, a concept node of the linguistic superhighway, and the target is the roleset as the content of its highway ID, `abandon.01`, on which every source that cites it lands; the links to VerbNet and FrameNet are the highway's edges ([Hops](Hops.md)).

## Source

| Source | Witness | Trust class | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `propbank` | `PropBank` | class `AcademicCurated` | `unicode`, `iso-639` | `*.xml` under `frames` | [`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe) |

## The frame file

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<frameset>` | the root | structure: nothing | nothing | `frameset.dtd` |
| `<predicate lemma="abandon">` | inside the frameset | the predicate, its lemma | `[abandon, roleset, [abandon, leave behind]]` | "Each file will contain a set of predicates associated with a particular lemma" |
| `<roleset id="abandon.01" name="leave behind">` | inside a predicate | the roleset, a highway node; as built its content is `[abandon, leave behind]`, a type of the highway's `pbroleset` list (`types pbroleset`, `keyed pbroleset roleset id`), with `name` said of it; the `id` is PropBank's identifier of the roleset, a highway ID, content as written, which as built the recipe resolves and records nothing of (`key roleset id`), and the target is the roleset as that highway node | `[[abandon, leave behind], name, leave behind]` | "The rolesets give mneumonics of the argument labels for each different set of arguments." |
| `<alias pos="v">abandon</alias>` | under `aliases` | of the roleset: `pos` and the text under `alias` | `[[abandon, leave behind], pos, v]`, `[…, alias, abandon]` | |
| `<role n="0" f="PPT" descr="abandoner">` | under `roles` | of the roleset: `n`, `f`, `descr` under their names; the role and its links one record | `[…, n, 0]`, `[…, f, PPT]`, `[…, descr, abandoner]` | "Roles have a number…" |
| `<rolelink class="leave-51.2" resource="VerbNet">theme</rolelink>`, `<lexlink class="Departing" resource="FrameNet" .../>` | under a role, or a roleset | `class` is the VerbNet class's or the FrameNet frame's identifier, content as written, and the link says the roleset or role maps to what it names (`type rolelink.class vnclass`, `type rolelink.class fnframe`); `resource`, `version`, `confidence`, `src` and the text under their names | `[…, class, leave-51.2]`, `[…, class, Departing]`, `[…, rolelink, theme]` | "their links to VerbNet and FrameNet" |
| `<usage resource="PropBank" version="3.4" inuse="+"/>` | under `usagenotes` | of the roleset | `[…, inuse, +]` | |
| `<example name="..." src="..."><text>And they believe…</text>` | inside a roleset | the example is its text (`thing example text`); its place in the roleset; `name` and `src` said of it | `[[abandon, leave behind], example, And they believe …]`, `[And they believe …, name, abandon-v: typical transitive]` | `frameset.dtd`: example (name, src) |
| `<rel relloc="12">abandoned</rel>`, `<arg type="ARG0" start="3" end="5">the Big Board</arg>` | under the example's `propbank` | of the example: each attribute and text under its name; the example one record | `[And they believe …, type, ARG0]`, `[…, arg, the Big Board]`, `[…, rel, abandoned]` | `type` is ARG0 to ARG7, the ARGM- forms |
| `<note>` | text inside a roleset or a predicate | of the thing it is inside | `[…, note, text]` | |
| `id` | on a roleset | PropBank's identifier of the roleset, a highway ID, content: in the target the roleset is the highway node `abandon.01`; as built the recipe resolves it and records nothing of it | nothing | |

A thing's own attributes are one record, witnessed once; an element that is no thing is one record of what it says. Nothing is renamed, reordered, or filled in.

## Not read

`frameset.dtd` matches no recipe. The source names no `reads`, so no README of the release is read.
