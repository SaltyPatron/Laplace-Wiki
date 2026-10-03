# Firmware

A firmware is a text file of decisions, one line each, read by `firmware.c` for one operation at a time; `firmware/program.firmware` is the program's own and says what a firmware can decide; `$LAPLACE_FIRMWARE`, or `--firmware FILE` on `pull`, `turn`, `hop`, `translate` and `degrees`, names another.

The firmware is never a record. The same records pulled under another firmware give another selection, and no standing changes.

## Grammar

`#` begins a comment; blank lines are ignored; a line that is not a decision, or a `for` naming an operation that does not exist, exits with status 2 and the line number.

| Line | Field | Meaning |
| --- | --- | --- |
| `k N` | `k` | how far below its rating a standing must still hold, in deviations |
| `lambda N` | `lambda` | the tax on another hop |
| `fan N` | `fan` | how many claims that hold an entity are read; one that holds more is reached, not crossed |
| `hops N` | `hops` | how many hops a chain may run |
| `top always` / `top within N` | `top_within` | whether the top of a set is taken every time, or how near a tie has to be before another strand can be taken in its place |
| `refuse predicate NAME...` | `refuse_predicate[32]` | kinds of strand refused before they are scored |
| `refuse witness NAME...` | `refuse_witness[32]` | strands witnessed by these refused |
| `fact N` | `fact` | a member of the set curated by a witness of at least this trust is returned as one fact, the rest held back; without the line no such branch fires |
| `order witness` / `order standing` | `order_witness` | on a claim with a part left open, the witness's own order before the standing, or not |
| `shape frechet` / `outliers N` / `dtw` / `edr N` | `shape`, `shape_n` | which shape of the tree to favour, and how many variable vertices a match may skip, or the EDR tolerance |
| `for OPERATION` | | what follows holds for that operation only: `hop`, `search`, `translate`, `follows`, `pull` |
| `emit N` | `emit` | how many constituents a turn may emit; 32 unless said |
| `enough N` | `enough` | a turn is complete when no more than N (0 to 1) of what its obligations owed at the start, each word as hard as it pulls, is still owed; 0 unless said |
| `take fact` / `take segment` / `take attestations N` / `take constituents N` | `take[16]` | under `for pull`, the segments a step takes, in order: the single fact when the fact branch fires; the rest of the branch the prompt is a run of, followed along what was observed; the N strongest strands of the prompt itself; the N strongest strands of each of its constituents |
| `take chain N RELATION... [\| RELATION...]` | `take`, `chain` | under `for pull` (and in `turn`), from each of the N words that pull hardest, the relations followed in order, each by its witness's order then its standing: where the chain ends is the answer; alternatives parted by `\|` are tried in turn (at most 8 steps, 4 alternatives) |
| `weigh N KIND...` | `weigh[128]` | strands of these kinds pull N as hard (0 to 1; 1 unless said); the firmware's reading, never a change to a standing |
| `role by KIND` | `role_by` | how hard a word pulls is read from what is attested of it under KIND |
| `role N VALUE...` | `role[128]` | a word of that VALUE pulls N as hard (0 to 1) |
| `up RELATION...` | `up[8]` | under `for translate`, the relations from a word up to its concept, in order; translation follows them back down in another language |
| `language HELD SAYS` | `language[2]` | under `for translate`, the language of what stands below the concept: what holds it under HELD, and what that says under SAYS |
| `gloss RELATION` | `gloss` | under `for translate`, what is shown of a concept |

Reading: `firmware_for(path, op)` starts from the defaults, then applies every line that holds everywhere and every line under `for op`, skipping other operations' sets. At most 32 names per refuse list, 16 take steps, 128 weights and roles, 8 steps of a chain and 4 alternatives.

## Defaults

Compiled into `firmware_for` and applied before the file is read: `k` 2.0, `lambda` 0.05, `fan` 4096, or 512 for `search`, `hops` 8, `top always`, `fact` 2.0 (above 1: never), `order witness`, `shape frechet`.

## The program's own firmware

`firmware/program.firmware`:

```text
k 2
lambda 0.05
hops 8
top always
order witness
role by UPOS
role 1 NOUN ADJ NUM
role 0.75 PROPN
role 0.5 VERB ADV ADP PART
role 0.25 PRON DET CCONJ PUNCT
role 0.05 SCONJ
role 0 AUX
for hop
  fan 4096
for search
  fan 512
for translate
  fan 4096
  up Sense synset ili
  language Synset language
  gloss Definition
for pull
  fan 4096
  refuse predicate BNC PENN GF PT NER WSL Target Other Sent Verb Noun Adj Prep Adv UPOS XPOS DEPREL FEATS MISC LEMMA type n f itype
  take chain 1 Sense Definition | LEMMA Sense Definition
  enough 0.5
  take segment
  take attestations 3
  take constituents 1
```

This is the one set of decisions of [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions): *k* = 2, always the top, fan 4,096 on a hop and 512 on a search, 8 hops, λ = 0.05; and a pull that takes the rest of the branch, three strands of the prompt, and one of each constituent. Besides those, the file carries a word's pull by its part of speech (`role`, the role trust fitted on SemCor's held-out documents), the tag layers a pull refuses, a chain from a word through its sense to a definition, and `enough 0.5`; the file marks the last three as defaults to be ruled on.

## Where each decision acts

| Decision | Acts in |
| --- | --- |
| `k` | `lp_confidence(r, k)` on every claim fetched by `claims_like`; `lp_cost(r, k, lambda)` in `degrees` |
| `lambda` | `lp_cost` per hop in the frontier search |
| `fan` | the `LIMIT fan + 1` of the claims fetch; `capped` is reported when more exist |
| `hops` | the frontier's hop bound |
| `top within N` | `take_top` in `pull`: among strands within `N` of the one above, one is drawn with `rand_r` from `--seed` or the clock |
| `refuse` | refused predicates go into every claim read the database makes (`laplace_claims`, `laplace_claims_each`, `laplace_couple`) and are taken out before the fan; `refused()` takes out refused witnesses before the sort |
| `fact` | the fact branch of `pull` |
| `order witness` | `positions_of` and `claim_by_position` before `claim_by_conf` on an open claim |
| `shape` | which of `lp_frechet4`, `lp_frechet4_outliers`, `lp_dtw4`, `lp_edr4` a shape comparison calls |
| `take` | the steps of `cmd_pull`, in order |

## What is specified beyond this

Spec 39 of the monorepo specifies the firmware as a content-addressed image over the operation ISA with a registry of policy kinds, an identity in every receipt, and rating by consequences; [18. Firmware](../Sequence/Firmware.md) documents that. The file above is what is built; the image, the registry, and the receipt are **specified** and not built in these repositories.
