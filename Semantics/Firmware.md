# Personality firmware

The personality firmware is a pull's decision tree: which segment of which branch to take, and how to combine them, from the observation, its attestations, and the tree across tiers, kept out of the training data.

## Knowledge and control

The knowledge is the training data: the records of entities, physicalities, claims, attestations, and standings. Governance, control, limitations, restrictions, and behavior are the firmware. They stay isolated from that knowledge so they do not contaminate it.

How this knowledge is navigated, and how an answer is reached, is individual to each human being. The same records can be pulled under different firmware. What differs is the selection.

A record that something exists is not a decision to act with it. Guns exist and violence exists, and both can be stored and attested. Whether a given pull hops toward that knowledge, fans out through it, or picks it is that human's firmware.

## The decision tree

The [trajectory](../Storage/Physicality.md#trajectories) is knowledge. Order in the path is precedes. A trunk over its constituents is contains. Two constituents of one path are a co-occurrence. The coordinates add the shape of that path: the angular separation on the S³, and the Fréchet, DTW, and EDR distances between trajectories. None of these is a probability. They are the set.

These are different operations, and the firmware is which one a pull runs. Containment looks up one trunk. The [ID](../Query.md#lookup-by-id) of a composition such as "Sherlock Holmes" is bit-packed into the mantissas of a path vertex, and the [GIN](../Query.md#containers-and-occurrences) keys that ID. A [gap](../Query.md#gaps) reads the next vertex of a trajectory, as in every "Captain ␣ Name" in Moby Dick. Shape compares the [real coordinates](../Storage/Physicality.md#real-coordinates) on the entities. The packed mantissas are not those coordinates, and the vertex sequence is the order, so the pull does not invent an ordinal. Which operation runs, which segment it lifts, and whether one high-trust attestation is returned as a fact, is the firmware. The records stay as they are.

The shape in that comparison is the tree, not the centroid of a short word. `cat` and `act` only show the small case: the same centroid, and a Fréchet distance of 0.132 because `c` and `a` are transposed. The use of the measure is a tree against other trees. An error log is one such tree. Across 1,000 clients and 10,000 repositories, one log's shape can lie very close to 50,000 others, and those 50,000 are the same pattern. See [Query: Shape](../Query.md#shape).

Plain Fréchet will not find them when a timestamp or a request id is one vertex of the tree. Favoring the outlier-tolerant measure, or tolerating that jitter, is what keeps the pattern. Favoring the plain maximum throws it out. The logs do not change. The favor does.

The tree is Laplace's probability. A conventional step reduces a set to a scalar, by a dot product or a cosine, and samples one token. Laplace keeps the set, and a step may return any segment of any branch, or a combination of segments. The basis is the observation, the attestations on that observation, and the whole composition across tiers: a tier-0 branch under a word, a run of a tier-3 sentence, a container above that sentence. On "the cat", 599 observed paths continue most often into a space, 409 times, and the tier-3 sentence "The cat sat on the mat" holds `sat on the mat` as a later segment of the same branch. Emitting the space is one token. Taking the later segment, or taking `cat` together with an attestation of it, is the tree.

The tree is the muscle memory of what this human being does with that set: which relation to follow, which shape measure to favor, which segment to lift out of which tier, where to hop, how far to fan out, what to refuse, and what to combine. That sequence of decisions is the firmware. It is not a weight stored in the records.

One branch returns a single member as a fact. It fires when that member was curated by a high-trust witness, a mandate or a result of that class, rather than merely observed. The return is one fact, not a draw from the rest of the set. The confidence sort does not fire this branch. Returning the fact is a decision of the tree, made because of the witness's trust, and the observations stay in the set for a firmware that asks for them.

## How a standing is read

A [standing](Consensus.md) is a Glicko-2 rating, a deviation, and a volatility. The pull does not change it. What the pull selects on is a reading of it.

The anchor is rating 1500. A claim's confidence is the chance it beats that anchor, taken *k* deviations below its rating, on Glicko-2's scale of 173.7178:

$$
p = \sigma\left(\frac{r - 1500}{173.7178} - k \frac{\mathrm{RD}}{173.7178}\right)
$$

The cost of crossing the claim is $-\ln p + \lambda$, with $\lambda$ a tax paid once per hop. Costs add, so the cheapest chain is the one whose confidences multiply to the most, shortened by the tax. *k* and $\lambda$ are not records. They are how this firmware reads the records.

*k* is a restriction on uncertainty. At *k* = 0 the rating is taken as it stands. Each step of *k* demands that the rating still hold further down inside its deviation, so a claim few witnesses have touched tugs less than its rating alone says. Two standings with the same records and different *k* are two selections:

| *k* | Rating 1700, deviation 300 | Rating 1600, deviation 40 | Selected |
| --- | --- | --- | --- |
| 0 | 0.760 | 0.640 | the louder rating |
| 0.5 | 0.572 | 0.613 | the tighter deviation |
| 2 | 0.091 | 0.529 | the tighter deviation |

They cross at *k* = 0.38. Nothing in the two standings changed.

## Temperature and restriction

Always taking the top of a set is a decision. Temperature is that decision's spread: how near a tie has to be before another strand can be taken. The pull has no softmax. The set is already in hand, and the firmware says whether two near confidences are an answer or a tie.

A restriction is the same kind of decision, applied before the sort. A firmware that does not navigate through layout and punctuation drops those strands out of the list. The standings stay. Another human's firmware keeps them.

## How far a search walks

$\lambda$ decides whether a longer, stronger chain beats a shorter, weaker one. Two hops at confidence 0.90 cost $0.211 + 2\lambda$. One hop at 0.70 costs $0.357 + \lambda$. They cross at $\lambda = 0.146$. Below that, the search walks the two strong hops. Above it, the search takes the single weaker hop and stops. The records of the three claims are the same either way.

Fanout is the other limit. A hop reads at most 4,096 claims that hold the entity, then orders that set by confidence. A degrees search reads at most 512, walks at most 8 hops, and pays $\lambda = 0.05$. An entity that holds more claims than the fan — a part of speech, a language — is reached and not crossed. The limit is applied before the ordering, so past the fan the set is whatever the index returned, not the strongest claims.

## Weights that are not standings

Role trust is a weight on which kind of word is allowed to pull. It is not a column of the claim. The measurements are in [Research: Trust](../Research/Trust.md#role-trust-in-word-sense-disambiguation).

Function words were drafted to pull a quarter as hard as a noun, or not at all, and a word attached to the target to pull four times as hard as a word elsewhere in the sentence. Those weights are a personality. Fitting them is a different personality. Neither one is a change to the records.

## One set of decisions

The selection a pull makes is this list, and each entry can differ per human being:

- Which operation runs against the records: containment of a trunk through the GIN, a gap read from the next vertex of a trajectory, or a shape on the real coordinates.
- Which segment of which branch to pull, at which tier, and which of those segments to combine. A step is not required to emit one token.
- *k*, how far below the rating a standing must still hold.
- $\lambda$, the tax on another hop.
- The fan, and which entities are hubs that may be reached and not crossed.
- How many hops a chain may run.
- Which kinds of strand are refused before they are scored: layout, punctuation, a part of speech, a witness, a language.
- The role weights, when a context word is doing the pulling.
- Whether the top of the resulting set is taken every time, and the temperature of that choice.
- Which relation of the trajectory to follow: precedes, contains, co-occurrence.
- Which shape of the tree to favor: angular separation, Fréchet, Fréchet with outliers skipped, DTW, or EDR, and how many variable vertices (a timestamp, a request id) the match may skip.
- Whether a high-trust curation in the set is returned as one fact, the rest of the set held back.
- On an open claim, whether the witness's own order is taken before the standing. The program does that for a translation and for a claim with a part left open, and it does not do it for a hop on one entity.

The program carries one of these: *k* = 2, always the top, fan 4,096 on a hop and 512 on a search, 8 hops, $\lambda$ = 0.05. That is one way through the records. It is not the knowledge, and it is not every human being's way.

## Instruction sets

The firmware's form is instruction sets. An instruction set takes each step of each operation of the forward pass.

The operations include the ones a conventional forward pass uses to fetch: attention, convolution, diffusion, the feed-forward network, the multilayer perceptron, and QK, KV, and VO. In Laplace those fetches are the lookup. The weights they would have shifted are the attestations, the observations, and the witnessing. UAX #29 breaks the prompt, and the trunk ID is the token index. What remains after the lookup has returned the set is the choice, and that choice is the instruction set rather than another record.

## Modification

The engine does not modify the personality firmware, unless it is wired up to the GitHub repository and allowed to deploy to itself.

A running engine can update itself without shutting off only partially, by patches, and only maybe.

That prohibition is about the firmware. It does not specify changes to records.

## How the control was separated

Storage already names every piece of content and keeps its trajectory. Semantics already gives every claim a standing. The forward pass ingests a prompt, breaks it down, and looks it up. The standing says what was attested and how hard it tugs. The selection says how this human being navigates those records and comes to an answer.

That selection was kept out of the training data. Governance, limitations, restrictions, and behavior written into the records would contaminate the knowledge, and every later pull would inherit someone else's way of navigating it. The records stay the knowledge. The selection stays the firmware, one for each human being.
