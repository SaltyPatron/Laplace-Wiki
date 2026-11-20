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
| `hops N` | `hops` | how many hops a chain or scan may run |
| `top always` / `top within N` | `top_within` | whether the top of a set is taken every time, or how near a tie has to be before another strand can be taken in its place |
| `only predicate NAME...` | `only_predicate[32]` | ablation filter: read only strands of these relations |
| `refuse predicate NAME...` | `refuse_predicate[32]` | kinds of strand refused before they are scored |
| `refuse witness NAME...` | `refuse_witness[32]` | strands witnessed by these source names refused |
| `negate WORD...` | `negate[32]` | words that flip polarity within a local scope (`not`, `no`, `never`, `without`, `neither`, `nor`) |
| `negate_relation REL...` | `negate_relation[32]` | relations whose edge reverses polarity (`antonym`, `excludes`, `contradicts`; supports `@RECIPE/FIELD`) |
| `scope_stop TOKEN...` | `scope_stop[32]` | punctuation tokens closing a local negation scope (`. ; : ? ! ,`) |
| `fact N` | `fact` | a member of the set curated by a witness of at least this trust is returned as one fact, the rest held back; above 1 means never |
| `order witness` / `order standing` | `order_witness` | on a claim with a part left open, the witness's own order before the standing, or not |
| `prevalence RELATION \| pair` | `prevalence` | prevalence relation or pair reading |
| `shape frechet` / `outliers N` / `dtw` / `edr N` | `shape`, `shape_n` | which 4D trajectory shape measure to favour, and how many interior outliers to skip or the EDR tolerance |
| `rounds N` | `rounds` | coupling rounds a forward pass spends (`layers`, each carrying forward the hardest-responding entities of the round before) |
| `breadth N` | `breadth` | how many of a round's hardest-responding entities the next round couples from |
| `nearest N` | `nearest` | how many entities nearest a curve's centroid the 4D GiST nominates for shape comparison |
| `walks N` | `walks` | BLAKE3-seeded random walkers launched from each position (`0`: none) |
| `walkfan N` | `walk_fan` | hub cap for random walkers: a node holding more strands is reached and returns home |
| `steps N` | `steps` | steps each walker takes |
| `restart P` | `restart` | restart probability (`0` to `1`) at each walker step |
| `sure N` | `sure` | standard-error margin separating two walk counts before one beats the other |
| `lift N` | `lift` | minimum observed-over-base-rate co-occurrence ratio (`≥ 1`) for `CH_BESIDE` grounding |
| `elect KEY...` | `elect[9]` | proposal comparison order across `grounds`, `continuity`, `agree`, `heads`, `cooccur`, `walks`, `shape`, `confidence`, `shared` |
| `tie first` / `tie draw` / `tie ask` | `tie` | tie-break rule when proposals are indistinguishable across all `elect` keys: lowest ID, seeded draw, or ask |
| `seed observation` / `seed session` | `seed_session` | derive the deterministic BLAKE3 seed from `(observation, firmware)` alone, or include `(session, turn)` |
| `for OPERATION` | | begins an operation-specific block: `hop`, `search`, `translate`, `follows`, `pull` |
| `emit N` | `emit` | maximum constituents a turn may emit; `32` unless said |
| `enough N` | `enough` | a turn completes when no more than `N` (`0` to `1`) of initial role-weighted obligation remains open; `0` unless said |
| `up RELATION...` | `up[8]` | under `for pull`, selective two-key relations (`@wn-lmf/Sense`) used to bubble past fan-limited word hubs (`up` is rejected under `for translate` in favor of `lexicalization`) |
| `language HELD-BY SAYS` | `language[2]` | under `for pull`, language selector |
| `lexicalization RECIPE THING LANGUAGE CONCEPT` | `lexical[4]` | under `for translate` and `for pull`, resolves lexicalization relations (`[lemma, language, ILI]`) directly from `RECIPE`'s declarations (`wn-lmf Sense language ili`) |
| `gloss RECIPE NAME` | `gloss[2]` | under `for translate`, shows the relation `RECIPE` declares for `NAME` (`wn-lmf Definition`) |
| `equivalent RECIPE NAME...` | `equiv[5]` | under `for translate`, joins ISO 639 code sets declared by `RECIPE` (`iso-639-3 Part1 Part2b Part2t`) |
| `usages RECIPE NAME` | `usages[2]` | under `for translate` and `for pull`, orders senses by concordance game counts declared by `RECIPE` (`wordnet-cntlist tag_cnt`) ahead of witness order and standing |
| `take fact` / `take segment` / `take attestations N` / `take constituents N` | `take[16]` | under `for pull`, the segments a pull takes in order |
| `take chain N RELATION... [\| RELATION...]` | `take`, `chain` | under `for pull` (and `turn`), follows up to 8 relation steps across up to 4 `\|`-separated alternatives (`@RECIPE/FIELD` resolved against `$LAPLACE_RECIPES` before any DB call) |
| `weigh N KIND...` | `weigh[128]` | strands of these kinds pull `N` as hard (`0` to `1`; `1` unless said) |
| `role by KIND` / `role N VALUE...` | `role_by`, `role[128]` | reads each word's obligation weight (`0` to `1`) from what is attested of it under `KIND` (`UPOS`) |

Reading: `firmware_for(path, op)` starts from the defaults, then applies top-level lines and lines under `for op`, skipping other operations' blocks. `firmware_ids` decomposes the `.firmware` file itself via `lp_text_decompose` so every firmware carries its canonical content-addressed `image_id` (`laplace firmware` inspects its resolved `@RECIPE/FIELD` bindings and `firmware_id` as JSON).

## Defaults

Compiled into `firmware_for` before reading the file: `k` `2.0`, `lambda` `0.05`, `fan` `4096` (`512` for `search`), `hops` `8`, `emit` `32`, `top always`, `fact` `2.0` (never), `order witness`, `shape frechet`, `rounds` `2`, `breadth` `64`, `nearest` `512`, `walks` `64`, `walkfan` `512`, `steps` `4`, `restart` `0.25`, `sure` `2.0`, `lift` `2.0`, `tie first`, `seed observation`, and `elect grounds continuity agree heads cooccur walks shape confidence shared`.

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
role 0.15 SCONJ
role 0.10 AUX

for hop
  fan 4096
for search
  fan 512
for translate
  fan 4096
  lexicalization wn-lmf Sense language ili
  gloss wn-lmf Definition
  equivalent iso-639-3 Part1 Part2b Part2t
  usages wordnet-cntlist tag_cnt
for pull
  fan 4096
  lexicalization wn-lmf Sense language ili
  up @wn-lmf/Sense
  usages wordnet-cntlist tag_cnt
  rounds 2
  breadth 64
  nearest 512
  walks 64
  walkfan 512
  steps 4
  restart 0.25
  sure 2
  lift 2
  elect grounds continuity agree heads cooccur walks shape confidence shared
  tie first
  seed observation
  refuse predicate BNC PENN GF PT NER WSL Target Other Sent Verb Noun Adj Prep Adv UPOS XPOS DEPREL FEATS MISC LEMMA type n f itype
  negate not no never without neither nor
  negate_relation antonym excludes contradicts
  scope_stop . ; : ? ! ,
  take chain 1 @wn-lmf/Sense @wn-lmf/synset @wn-lmf/Definition | @conllu/LEMMA @wn-lmf/Sense @wn-lmf/synset @wn-lmf/Definition
  enough 0.5
  take segment
  take attestations 3
  take constituents 1
```

This implements [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions) together with SemCor-fitted `UPOS` role weights, recipe-bound `@RECIPE/FIELD` relation chains (`lexicalization`, `gloss`, `equivalent`, `usages`, `up`), multi-round coupling (`rounds`, `breadth`, `nearest`), BLAKE3-seeded random walks (`walks`, `walkfan`, `steps`, `restart`, `sure`, `lift`), negation scoping, and the typed `elect` order. Note that the `refuse predicate ... UPOS Verb Noun ...` line is a temporary text-predicate workaround scheduled for replacement in `Batch 2` by 64-bit `manifest/banks.tsv` mask-bank filtering and proper word-POS fallback handling.

## Where each decision acts

| Decision | Acts in |
| --- | --- |
| `k`, `lambda` | `lp_confidence(r, k)` and `lp_cost(r, k, lambda)` across `hop`, `degrees`, `pull`, and `turn` |
| `fan`, `hops` | `LIMIT fan + 1` hub cutoff (`holds_capped`, `laplace_claims*`) and frontier depth bound |
| `up`, `lexicalization`, `usages`, `equivalent`, `gloss` | two-key hub bubbling in `program.c` and concept/sense resolution in `pull.c` (`laplace translate`) |
| `rounds`, `breadth`, `nearest` | multi-round `COUPLE` expansion and 4D GiST curve-centroid nomination in `program.c` |
| `walks`, `walkfan`, `steps`, `restart`, `sure`, `lift` | deterministic BLAKE3 random walks (`CH_WALK`) and co-occurrence lift (`CH_BESIDE`) in `program.c` |
| `elect`, `tie`, `seed`, `top within N` | `STEER` / `SELECT` proposal ranking and deterministic tie-breaking (`program.c`, `forward.c`) |
| `only`, `refuse`, `negate`, `negate_relation`, `scope_stop` | strand filtering and polarity tracking in `COUPLE`, `SCAN`, and `STEER` |
| `fact`, `order witness`, `shape`, `take`, `emit`, `enough` | `cmd_pull` steps, witness-position ordering, 4D curve distance (`lp_frechet4*`/`lp_dtw4`/`lp_edr4`), and turn completion |

## Additional profiles and Gödel OODA (`Batch 2`)

Firmware in Laplace stays plain, detached, content-addressed `.firmware` text files (`program.firmware`, `chess.firmware`, and the epistemic/task profiles `deductive`..`adversarial` scheduled in `Batch 2` under `Laplace-Engine#10`, alongside Gödel OODA `BELIEF ≠ RISK ≠ ACTION` abstention/clarification gates and consequence rating in [18. Firmware](../Sequence/Firmware.md)) — never a separate compiled binary-blob registry.
