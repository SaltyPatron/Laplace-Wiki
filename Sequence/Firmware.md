# 13. Firmware

The decisions a pull makes are written as instruction sets, one firmware per human being, kept out of the records.

The personality firmware is a pull's decision tree: which segment of which branch to take, and how to combine them, from the observation, its attestations, and the tree across tiers, kept out of the training data. It comes before the pull because no pull can choose without it.

## Before this stage

[12. Web](Web.md): the operations a firmware chooses between. Nothing in the records: the firmware is kept out of them on purpose.

## Operations, per firmware

### 13.1 Separate control from knowledge

- **In:** the records of [8. Content](Content.md) to [10. Consensus](Consensus.md).
- **Do:** the knowledge is the training data: the records of entities, physicalities, claims, attestations, and standings. Governance, control, limitations, restrictions, and behavior are the firmware. They stay isolated from that knowledge so they do not contaminate it. Governance, limitations, restrictions, and behavior written into the records would contaminate the knowledge, and every later pull would inherit someone else's way of navigating it. A record that something exists is not a decision to act with it: guns exist and violence exists, and both can be stored and attested; whether a given pull hops toward that knowledge, fans out through it, or picks it is that human's firmware.
- **Out:** a firmware file, separate from the database.
- **From:** [Personality firmware: Knowledge and control](../Semantics/Firmware.md#knowledge-and-control), [Personality firmware: How the control was separated](../Semantics/Firmware.md#how-the-control-was-separated).

### 13.2 Decide which operation runs

- **In:** the operations of [12. Web](Web.md) and [14. Pull](Pull.md).
- **Do:** containment of a trunk through the GIN; a gap read from the next vertex of a trajectory; or a shape on the real coordinates. Which relation of the trajectory to follow: precedes, contains, co-occurrence. These are different operations, and the firmware is which one a pull runs.
- **Out:** the operation.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree).

### 13.3 Decide the segment and the combination

- **In:** the tree of the observation across tiers.
- **Do:** which segment of which branch to pull, at which tier, and which of those segments to combine. A step is not required to emit one token. On "the cat", 599 observed paths continue most often into a space, 409 times, and the tier-3 sentence "The cat sat on the mat" holds `sat on the mat` as a later segment of the same branch: emitting the space is one token; taking the later segment, or taking `cat` together with an attestation of it, is the tree.
- **Out:** the segment rule.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree), [Pull: The forward pass](../Semantics/Pull.md#the-forward-pass).

### 13.4 Set *k*, λ, the fan, and the hops

- **In:** the reading of [12. Web](Web.md) operations 12.2 to 12.4.
- **Do:** *k*, how far below the rating a standing must still hold; λ, the tax on another hop; the fan, and which entities are hubs that may be reached and not crossed; how many hops a chain may run. These are not records. One firmware carries *k* = 2, always the top, fan 4,096 on a hop and 512 on a search, 8 hops, λ = 0.05. That is one way through the records; it is not the knowledge, and it is not every human being's way.
- **Out:** the four numbers.
- **From:** [Personality firmware: How a standing is read](../Semantics/Firmware.md#how-a-standing-is-read), [Personality firmware: How far a search walks](../Semantics/Firmware.md#how-far-a-search-walks), [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions).

### 13.5 Set the refusals

- **In:** the kinds of strand.
- **Do:** which kinds of strand are refused before they are scored: layout, punctuation, a part of speech, a witness, a language. A firmware that does not navigate through layout and punctuation drops `SpaceAfter` and `punct` out of the list; the standings stay, and another human's firmware keeps them.
- **Out:** the restriction applied before the sort.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity).

### 13.6 Set the role weights

- **In:** the parts of speech and syntactic links of context words.
- **Do:** role trust is a weight on which kind of word is allowed to pull, when a context word is doing the pulling. It is not a column of the claim. Hand-drafted weights: nouns, adjectives, and numerals 1.0; proper nouns 0.75; verbs, adverbs, adpositions, and particles 0.5; pronouns, determiners, coordinating conjunctions, and punctuation 0.25; subordinating conjunctions 0.05; auxiliaries 0. The target's head or dependent 1.0; another dependent of the same head 0.5; anywhere else in the sentence 0.25. Function words pull a quarter as hard as content words, or not at all, and words attached to the target pull four times as hard as words elsewhere. Those weights are a personality; fitting them is a different personality; neither is a change to the records.
- **Out:** the role weights.
- **Check:** on 6,613 word-sense instances, prevalence alone scored 64.6, weights drafted by hand 66.2, and weights fitted 66.2, against WordNet's first sense at 65.2.
- **From:** [Personality firmware: Weights that are not standings](../Semantics/Firmware.md#weights-that-are-not-standings), [Research: Trust: Role trust in word sense disambiguation](../Research/Trust.md#role-trust-in-word-sense-disambiguation).

### 13.7 Set the choice and the temperature

- **In:** the ordered set of [12. Web](Web.md) operation 12.4.
- **Do:** whether the top of the resulting set is taken every time, and the temperature of that choice: how near a tie has to be before another strand can be taken. The pull has no softmax. The set is already in hand, and the firmware says whether 0.972 against 0.969 is an answer or a tie. On an open claim, whether the witness's own order is taken before the standing: the program does that for a translation and for a claim with a part left open, and does not for a hop on one entity.
- **Out:** the choice rule.
- **From:** [Personality firmware: What was measured on one entity](../Semantics/Firmware.md#what-was-measured-on-one-entity), [Personality firmware: One set of decisions](../Semantics/Firmware.md#one-set-of-decisions).

### 13.8 Set the shape measure

- **In:** the shape measures of [14. Pull](Pull.md) operation 14.6.
- **Do:** which shape of the tree to favor: angular separation, Fréchet, Fréchet with outliers skipped, DTW, or EDR, and how many variable vertices, a timestamp, a request id, the match may skip. Plain Fréchet will not find a pattern when one vertex is a timestamp: measured on 60-point trajectories, one outlier scores 1.39 against 1.72 for an unrelated sequence, the same pair with the outlier skipped scores 0, and jitter the size of those fields scores 0.087. Favoring the outlier-tolerant measure keeps the pattern; favoring the plain maximum throws it out. The logs do not change; the favor does.
- **Out:** the measure and its tolerance.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree), [Query: Shape](../Query.md#shape), [Research: Numerics: Trajectory measures](../Research/Numerics.md#trajectory-measures).

### 13.9 Set the fact branch

- **In:** the set of strands.
- **Do:** whether a high-trust curation in the set is returned as one fact, the rest of the set held back. One branch returns a single member as a fact. It fires when that member was curated by a high-trust witness, a mandate or a result of that class, rather than merely observed. The confidence sort does not fire this branch: on the claims that hold `Paris`, the head at *k* = 2 is `[Paris, UPOS, PROPN]` at 0.991 from 1,180 matches, while a claim that starts at stock and receives one attestation at trust 1.0 reads as 0.138 at *k* = 2 and five such attestations as 0.505. Usage outranks a new curated fact on the sort, so returning the fact is a decision of the tree, made because of the witness's trust.
- **Out:** the fact rule.
- **From:** [Personality firmware: The decision tree](../Semantics/Firmware.md#the-decision-tree).

### 13.10 Write it as instruction sets

- **In:** the decisions of 13.2 to 13.9.
- **Do:** the firmware's form is instruction sets. An instruction set takes each step of each operation of the forward pass. The operations include the ones a conventional forward pass uses to fetch: attention, convolution, diffusion, the feed-forward network, the multilayer perceptron, and QK, KV, and VO. In Laplace those fetches are the lookup; the weights they would have shifted are the attestations, the observations, and the witnessing; UAX #29 breaks the prompt, and the trunk ID is the token index. What remains after the lookup has returned the set is the choice, and that choice is the instruction set rather than another record.
- **Out:** the firmware, one per human being.
- **From:** [Personality firmware: Instruction sets](../Semantics/Firmware.md#instruction-sets), [Pull: The choice](../Semantics/Pull.md#the-choice).

### 13.11 Lock it

- **In:** the firmware of 13.10.
- **Do:** the engine does not modify the personality firmware, unless it is wired up to the GitHub repository and allowed to deploy to itself. A running engine can update itself without shutting off only partially, by patches, and only maybe. That prohibition is about the firmware; it does not specify changes to records.
- **Out:** a firmware the engine runs under and does not rewrite.
- **From:** [Personality firmware: Modification](../Semantics/Firmware.md#modification).

## What this stage leaves behind

One way through the records, for one human being, written as instruction sets and held apart from the records. The same records pulled under different firmware give different selections, and no standing changes.

## Without this stage

No pull can choose, so no pull can run.
