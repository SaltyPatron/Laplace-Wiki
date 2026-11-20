# Consensus

Everything attested about a claim, as a whole, provides its overall score: a Glicko-2 standing that tells how hard a strand tugs back.

## Deduplication

Same content means the same hash, and the deduplication applies to the attestations, to form a consensus.

## Glicko-2

Glicko-2 is what tells how hard a strand tugs back, and it replaces a lot of conventional AI mechanisms. See [Research: Learning](../Research/Learning.md#rating-one-matchup-at-a-time) and [Research: Chess](../Research/Chess.md).

## Matchups

There are no global, delayed rating periods. As content is observed, first in, first out, the matchups are played.

If WordNet says a dog is a noun 30 times, that is one attestation with 30 games. An attestation is one per strand and witness: its games, how many times that witness asserts the strand, and a score, and that series is played at the witness's trust. The client folds a source's repeats before the database sees anything and solves the series as one update: the rating where the claim's prior standing and the series' score agree, with the deviation the series' games give. That is not Glicko-2's single period step, one linearized move that assumes a period moves a rating only a little, which is fine for small moves and wrong for a long series. A 450 player against a 3400 player, 1,000 games, 100 wins and 100 draws, is one series with score 0.15: played game by game it converges to 3100 with deviation 15; solved as one update it gives 3092 with deviation 16; one period step from 450 gives 105,823. The database receives one update per strand per witness. Different witnesses play first in, first out.

Run-length encoding is content structure only: identical consecutive children in a path, with the run in M. A sentence pasted a million times into one prompt is a run in that prompt's content, an observation that attests nothing; the same message across turns lengthens the session's trajectory. Across users or witnesses, repeats are separate witnesses, independent only as far as their dependence roots are. Copies count once: a derived witness records its lineage, so dependence never masquerades as independent confirmation.

Empirical corpus frequencies measured from real annotated tokens — such as SemCor concordance sense counts in WordNet's `cntlist` (`tag_cnt`, folded via `games row tag_cnt`) and gold Universal Dependencies part-of-speech, lemma, and dependency observations across annotated treebank sentences — are preserved as genuine `games` in that witness's series (`lp_tally_edge`). By contrast, synthetic packaging inflation — Cartesian cross-product join layouts (such as Predicate Matrix rows repeating one mapping across paired combinations) or automatic secondary tagger layers (such as FrameNet's automatic BNC and PENN layers) — is packaging rather than new empirical observations, and does not multiply games.

Incoming records play existing records, for attestation and Glicko-2 scores. Querying picks the records with higher scores, but does not change scores.

The more something is attested to, the more its score rises or lowers, just like a chess rating. Uncertainty, source trust, and the like all affect an attestation's weight and how much it can change a consensus: a low-trust user prompt or social media post weighs far less than the results of mathematical algorithms or curated academic sources.

## Trust

Trust runs from `SubstrateMandate` (`1.00`), down through `StandardsDerived` (`0.95`), `AcademicCurated` (`0.85`), `UserCuratedResource` (`0.60`), `AIModelProbe` (`0.50`), `UserPromptContent` (`0.30`), and `ResponseContent` (`0.20`), to `0.00`, or signed down to `-1.00` when a witness is reliably inverted (`manifest/trust_classes.toml`). Laplace's own generated outputs (`ResponseContent = 0.20`) carry lower trust than `UserPromptContent` (`0.30`) by design, while ordinary prompts enter as observations and do not self-attest semantic truth.

Assimilated AI models (`AIModelProbe = 0.50`) rank above user prompts, below user-curated and academically curated datasets, and corroborate one another as an independent multi-model round table whenever their causal lineages are distinct.

Trust bounds a vote. Each root's mean outcome is pulled toward a draw by the witness's trust ($s_{\text{eff}} = 0.5 + t(s - 0.5)$), and each causal `dependence_root` has one shared source variance $\omega_r^2$ whose Fisher information $J_r / (1 + \omega_r^2 J_r)$ saturates at $1/\omega_r^2$, so no amount of self-repetition takes a single witness past its trust ceiling (`lp_series` in `include/laplace/consensus.h`). Lineage capping applies strictly to shared causal lineage (`attestation.lineage` — copies, re-exports, fine-tunes of the same base model, or Sybil accounts folded into $k = 1$ root), **never** across independent curated lexicons (such as WordNet, UD, FrameNet, VerbNet, and PropBank) or independent model families (such as Qwen, Llama, Gemma, DeepSeek, and Mistral), whose distinct `dependence_root`s ($k > 1$) add independent precision ($k/\omega^2$) so genuine multi-model and multi-corpus agreement tugs harder than any single witness alone. A witness's effective trust starts at its trust class prior and moves only through agreement or disagreement with independent witnesses and verified outcomes, never by repeating itself. User prompts screaming that the earth is flat cannot drown out GPS, photographs, mathematics, reports, and NASA: as a million independent witnesses they would (*p* 0.351 from 0.947); as one capped Sybil root they barely dent it (0.821); as ordinary prompt observations the standing holds (0.954).

There are also trusts that differentiate subjects, pronouns, stopwords, and so on: a trust level for part of speech, for sense, and for dependency relation, so that filler does not drown everything. See [Research: Trust](../Research/Trust.md).

## Entry

A witness or claim entering for the first time starts from a stock default for its level of attestation: whether synonyms matter more or less than meronyms, nouns than verbs, proper nouns than stopwords, and the source's trust, stability, and uncertainty.

## No ETL

There are no delayed consensus folds. ETL is forbidden: no delayed segments that group everything together, no lazy, manually updated hot caches, and no SQL doing the heavy operations.
