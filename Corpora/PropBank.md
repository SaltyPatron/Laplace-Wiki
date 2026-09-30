# PropBank

PropBank attests what a frame file says of each predicate and roleset, the aliases, roles, links, notes, and examples of a roleset speaking of the roleset they are inside, and the DTD and guidelines attest nothing.

One source reads PropBank: its frame files, "every predicate's rolesets, their roles, and their links to VerbNet and FrameNet". Each file is XML, read as what it says: the recipe names two elements as things, and says of the rest that "everything else speaks of the roleset it is inside". The project's guidelines are the [Framing Guidelines](https://verbs.colorado.edu/mpalmer_old/palmer.bk01/projects/ace/FramingGuidelines.pdf) and the [English PropBank Annotation Guidelines](https://verbs.colorado.edu/~mpalmer/projects/ace/EPB-annotation-guidelines.pdf).

## Source

| Source | Witness | Uncertainty | After | Files | Recipe |
| --- | --- | --- | --- | --- | --- |
| `propbank` | `PropBank` | deviation 90 | `unicode`, `iso-639` | `*.xml` under `frames` | [`frames.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/propbank/frames.recipe) |

The uncertainty is the deviation the witness's attestations enter at, as [Consensus](../Semantics/Consensus.md#entry) describes. The source says of its 90 that it is "this recipe's choice for a curated academic resource; the specification does not give one": the number is not settled, and [Corpora](README.md#not-settled) lists it among what stays missing.

## The frame file

A frame file is one `frameset` element holding predicates. "A predicate is its lemma and a roleset its id; everything else speaks of the roleset it is inside." A predicate and a roleset are named as written, with no kind before the name. Every predicate of a claim is an attribute's or an element's name as the file writes it: `n`, `f`, `descr`, `pos`, `type`, `start`, `end`.

| Piece | Written as | Laplace reads it as | Claim recorded | Specification |
| --- | --- | --- | --- | --- |
| `<frameset>` | the root of a frame file | structure: it is inside nothing and speaks of nothing; the predicates in it are things of their own | nothing | "note or predicate, any number", `frameset.dtd` |
| `<predicate lemma="abandon">` | inside the frameset | the predicate, named by its lemma as written; each roleset inside it takes its place there | `[abandon, roleset, abandon.01]` | "Each file will contain a set of predicates associated with a particular lemma (including phrasal variants, like 'keep_from', etc)." `frameset.dtd` |
| `<roleset id="abandon.01" name="...">` | inside a predicate | the roleset, named by its id; `name` said of it; everything inside it speaks of it | `[abandon.01, name, text]` | "The rolesets give mneumonics of the argument labels for each different set of arguments. Multiple rolesets per predicate are necessary for the accomodation of different senses of the predicate." `frameset.dtd` |
| `<aliases>` holding `<alias pos="v">abandon</alias>` | inside a roleset | of the roleset: `pos` under its name, the text under `alias`; each alias one record | `[abandon.01, pos, v]`, `[abandon.01, alias, abandon]` | `frameset.dtd`: alias, text; attribute pos (r, p, v, n, j, l, x, m, d, f); the DTD glosses r Adverb, p Preposition, v Verb, n Noun, j Adjective |
| `<roles>` holding `<role n="0" f="PAG" descr="...">` | inside a roleset | of the roleset: `n`, `f`, and `descr` each under its name; a role and its links one record | `[abandon.01, n, 0]`, `[abandon.01, f, PAG]`, `[abandon.01, descr, text]` | "Roles have a number (or an M associated with them, for common adjuncts that don't qualify for number argument status)." `frameset.dtd`: n is 0 to 7, m, or M; f is a function tag, PAG "prototypical agent", PPT "prototypical patient", LOC "location", TMP "temporal", and the rest the DTD comment glosses. "The Arg0 label is assigned to arguments which are understood as agents, causers, or experiencers." Annotation Guidelines 1.3.1 |
| `<rolelinks>` holding `<rolelink ...>` under a role; `<lexlinks>` holding `<lexlink ...>` under a roleset | inside a roleset | of the roleset: each attribute under its name, the text under the element's name | `[abandon.01, attribute, value]`, `[abandon.01, rolelink, text]` | "their links to VerbNet and FrameNet", the source's own words; `frameset.dtd`: rolelinks; lexlinks |
| `<note>`, `<usagenotes>` | text inside a roleset or a predicate | of the thing it is inside, under the element's name; a note inside the frameset is inside no thing and is not recorded | `[abandon.01, note, text]`, `[abandon, note, text]` | `frameset.dtd`: aliases, note, roles, usagenotes, then lexlinks or example or note |
| `<example name="..." src="...">` with `<text>`, and `<propbank>` holding `<arg type="ARG0" start="..." end="...">` and `<rel relloc="...">` | inside a roleset | of the roleset: `name` and `src` of the example, its `text`, and each argument's `type`, `start`, `end`, and text, and the relation's `relloc` and text, each under its name; the example one record. The recipe names no span: `start` and `end` are recorded as written, not as a stretch of the text | `[abandon.01, name, value]`, `[abandon.01, src, value]`, `[abandon.01, text, sentence]`, `[abandon.01, type, ARG0]`, `[abandon.01, start, value]`, `[abandon.01, end, value]`, `[abandon.01, arg, text]`, `[abandon.01, relloc, value]`, `[abandon.01, rel, text]` | `frameset.dtd`: example (name, src): note, text, then propbank or amr or note; arg (type, start, end); rel (relloc). `type` is ARG0 to ARG7, C-ARG0 to C-ARG7, R-ARG0 to R-ARG7, and the ARGM- forms |
| any other element inside a roleset | with attributes or text | of the roleset: each attribute under its name, its text under the element's name; together, one record | `[abandon.01, attribute, value]`, `[abandon.01, ELEMENT, text]` | |
| an empty attribute value | what the file leaves empty | nothing | none | |

A thing's own attributes are one record, witnessed once. An element that is no thing is one record: the path of its name, its claims, and the records of the elements inside it. Nothing is renamed, reordered, or filled in: a role's number is said of the roleset under `n`, not of a role, because the recipe names no role as a thing.

## Not read

`frameset.dtd` under `frames` matches no recipe and is not read: it is the specification cited above, and nothing on this page is attested by it. The source names no `reads`, so no README or other text of the release is read.
