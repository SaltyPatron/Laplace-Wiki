# Pull

Laplace's forward pass is native C recursive operations with A* and indexed lookups, pulling on an interwoven web of entities and attestations.

## The web

When entities and physicalities are recorded, additional records and relations are added to form a spider colony web: N spiders, all with interwoven webs, where pulling on one strand makes everything else tug back. [Consensus](Consensus.md) tells how hard it tugs back.

Degrees of separation, as in a Bacon number or an Erdős number, measure how far anything is from anything else.

## The forward pass

A step does not have to emit one token. The forward pass can pull any segment of any branch, or combine segments, however the [firmware](Firmware.md) sees fit.

What a step has to work from is the observation, the attestations on that observation, and the observation's whole tree across tiers. The observation is the trajectory: precedes, contains, co-occurrence, and the shape of the path. The attestations are the claims witnessed of that same content. The tree is the composition, from tier 0 up through every constituent and every container.

"The cat sat on the mat" is one tier-3 node of eleven constituents, six tier-2 words and five tier-0 spaces. `cat` is one segment of that branch. `sat on the` is another, a contiguous run of the same trajectory. The letters of `cat` are the tier-0 branch under the word. A step can return any of those, or a combination of them: the word together with a gloss attested of it, the remainder of the sentence, the letters, or all three.

The same phrase, looked up as an observation, is held by 599 paths. Counted by occurrence, what follows it is a space 409 times across 356 paths, then a period 233 times across 170. The containers of those paths reach their trunks in four levels. That count is the observation, and a step required to emit one token stops on the space. A step allowed to take a segment keeps going along the branch, and a step allowed to combine can bring the attestation of `cat` along with whatever segment of the sentence it kept.

Under that, a step is still native C: A* and indexed lookup, O(log N) + O(K), with no softmax and no context window. A prompt is ingested as text, broken down, and given a trunk node ID.

## The choice

The choice of which segment, which branch, and which combination is the [personality firmware](Firmware.md). One of those combinations is a single fact, when the set holds a high-trust curation. Whether the top of a set is taken every time is that tree's decision, and taking the top is not the same as emitting one token.

## Hop and fanout

From any entity, Laplace can hop and fan out to anything else with integrity. Attestations identify which words are fluff and which are important, and give words trust levels and stability. From `Butler`, Laplace can pull a great deal of information and link it to `butler`. See [Research: Semantics Experiments](../Research/Semantics-Experiments.md).
