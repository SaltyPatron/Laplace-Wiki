# ATOMIC

ATOMIC 2020 attests commonsense tuples written as a head, a relation, and a tail, and ATOMIC10X is a model-generated witness of the same shape that enters unrated.

## Format

| Record | Field | Order | Type | Specification |
| --- | --- | --- | --- | --- |
| ATOMIC 2020 tuple | head, relation, tail | 1, 2, 3 | string, string, string | No header. Each line is one commonsense tuple: column 1 the head node/concept, column 2 the edge relation, column 3 the tail node/concept. `train.tsv`, `dev.tsv`, and `test.tsv` are the splits of that record. The relation is the mask ([Claims](../Semantics/Claims.md#masks)). The tail is the value. The composition is the tuple. |
| ATOMIC10X example | head | 1 in the release field list | string | JSON object, not a TSV column. Not defined as a key by Hwang et al. 2021. West et al. 2021 describe an event–relation–inference triple. The release field list: head is the event for this example (string). |
| ATOMIC10X example | relation | 2 in the release field list | string | JSON object. Not defined as a key by Hwang et al. 2021. The release field list: the relation for this example, one of [xNeed, xReact, xEffect, xIntent, xAttr, xWant, HinderdBy]. That list spells HinderdBy. West et al. 2021 names xAttr, xReact, xEffect, xIntent, xWant, xNeed, and HinderedBy. |
| ATOMIC10X example | tail | 3 in the release field list | string | JSON object. Not defined as a key by Hwang et al. 2021. West et al. 2021 call the third element the inference. The release field list: tail is the inference for this example (string). |
| ATOMIC10X example | split | 4 in the release field list | string | JSON object. Not defined by Hwang et al. 2021 or West et al. 2021. The release field list: the dataset split for this example, one of [train, test, val]. |
| ATOMIC10X example | rec_0.5 | 5 in the release field list | bool | JSON object. Not defined by Hwang et al. 2021 or West et al. 2021. The release field list: rec_X is whether this example is cutoff by the critic at an expected recall of X. High filtration uses 0.5. |
| ATOMIC10X example | rec_0.6 | 6 in the release field list | bool | JSON object. Not defined. The release field list defines rec_X and names 0.5 and 0.8. It does not give a separate sentence for 0.6. |
| ATOMIC10X example | rec_0.7 | 7 in the release field list | bool | JSON object. Not defined. The release field list defines rec_X and names 0.5 and 0.8. It does not give a separate sentence for 0.7. |
| ATOMIC10X example | rec_0.8 | 8 in the release field list | bool | JSON object. Not defined by Hwang et al. 2021 or West et al. 2021. The release field list: rec_X is whether this example is cutoff by the critic at an expected recall of X. Medium filtration uses 0.8. |
| ATOMIC10X example | rec_0.9 | 9 in the release field list | bool | JSON object. Not defined. The release field list defines rec_X and names 0.5 and 0.8. It does not give a separate sentence for 0.9. |
| ATOMIC10X example | p_valid_model | 10 in the release field list | float | JSON object. Not defined by Hwang et al. 2021 or West et al. 2021. The release field list: the score assigned by the critic model (float). |

## Value

| Field | Composition | Mask | What is recorded | Lineage or hop | Specification |
| --- | --- | --- | --- | --- | --- |
| ObjectUse | head, relation, tail | ObjectUse | tail | ATOMIC 2020 | ObjectUse describes everyday affordances or uses of objects, and includes both typical and atypical uses. Hwang et al. 2021, Appendix A. |
| MadeUpOf | head, relation, tail | MadeUpOf | tail | ATOMIC 2020 | MadeUpOf describes a part, portion or makeup of an entity. Hwang et al. 2021, Appendix A. |
| HasProperty | head, relation, tail | HasProperty | tail | ATOMIC 2020 | HasProperty usually describes entities' general characteristics such as "rose" is "red," subjective attributes such as "thirst" is "uncomfortable." In certain case, the relation can also map to descriptors that speak to the substance or value of items. Hwang et al. 2021, Appendix A. |
| AtLocation | head, relation, tail | AtLocation | tail | ATOMIC 2020 | AtLocation is a spatial relation that describes the location in/on/at which an entity is likely to be found. Hwang et al. 2021, Appendix A. |
| CapableOf | head, relation, tail | CapableOf | tail | ATOMIC 2020 | CapableOf is designed to describe abilities and capabilities of everyday living entities (e.g., humans, animals, insects) and natural entities that can exert a force (e.g. sun, storms). Hwang et al. 2021, Appendix A. |
| Desires | head, relation, tail | Desires | tail | ATOMIC 2020 | Desires and NotDesires are relations that deal with desires of sentient entities. Hwang et al. 2021, Appendix A. |
| NotDesires | head, relation, tail | NotDesires | tail | ATOMIC 2020 | Desires and NotDesires are relations that deal with desires of sentient entities. Hwang et al. 2021, Appendix A. |
| xIntent | head, relation, tail | xIntent | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xIntent defines the likely intent or desire of an agent (X) behind the execution of an event. Hwang et al. 2021, Appendix A. |
| xReact | head, relation, tail | xReact | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xReact and oReact define the emotional reactions on the part of X or other participants in an event. Hwang et al. 2021, Appendix A. |
| oReact | head, relation, tail | oReact | tail | ATOMIC 2020 | xReact and oReact define the emotional reactions on the part of X or other participants in an event. Hwang et al. 2021, Appendix A. |
| xNeed | head, relation, tail | xNeed | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xNeed describes a precondition for X achieving the event. Hwang et al. 2021, Appendix A. |
| xWant | head, relation, tail | xWant | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xWant and oWant are postcondition desires on the part of X and others, respectively. Hwang et al. 2021, Appendix A. |
| oWant | head, relation, tail | oWant | tail | ATOMIC 2020 | xWant and oWant are postcondition desires on the part of X and others, respectively. Hwang et al. 2021, Appendix A. |
| xEffect | head, relation, tail | xEffect | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xEffect and oEffect are social actions that may occur after the event. Hwang et al. 2021, Appendix A. |
| oEffect | head, relation, tail | oEffect | tail | ATOMIC 2020 | xEffect and oEffect are social actions that may occur after the event. Hwang et al. 2021, Appendix A. |
| xAttr | head, relation, tail | xAttr | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. | xAttr describes X's persona or attribute as perceived by others given an event. Hwang et al. 2021, Appendix A. |
| Causes | head, relation, tail | Causes | tail | ATOMIC 2020 | Causes specifically captures the causal relation between two events or entities. The postcondition in Causes is not socially triggered and can exist outside human control. Hwang et al. 2021, Appendix A. |
| HinderedBy | head, relation, tail | HinderedBy | tail | ATOMIC 2020. ATOMIC10X is a separate witness of this relation, not a second copy of the 2020 graph, and enters unrated. The release field list spells HinderdBy. | HinderedBy introduces hindrances that obstruct the natural path to the achievement of a goal. Hwang et al. 2021, Appendix A. |
| xReason | head, relation, tail | xReason | tail | ATOMIC 2020 | xReason provides a post-fact explanation of the cause of an event, which is related to, but distinct from, xIntent's intentions. Hwang et al. 2021, Appendix A. |
| isAfter | head, relation, tail | isAfter | tail | ATOMIC 2020 | isAfter and isBefore introduce events that can precede or follow an event, respectively. These relations are temporally situated without specific regard to the need or reaction of the person X. Hwang et al. 2021, Appendix A. |
| isBefore | head, relation, tail | isBefore | tail | ATOMIC 2020 | isAfter and isBefore introduce events that can precede or follow an event, respectively. These relations are temporally situated without specific regard to the need or reaction of the person X. Hwang et al. 2021, Appendix A. |
| HasSubEvent | head, relation, tail | HasSubEvent | tail | ATOMIC 2020 | HasSubEvent provides the internal structure of an event, each tail denoting a step within the larger head event. Hwang et al. 2021, Appendix A. |
| isFilledBy | head, relation, tail | isFilledBy | tail | ATOMIC 2020 | isFilledBy provides a filler phrase for an event with a blank that is sensical and commonly acceptable for the event. Hwang et al. 2021, Appendix A. |
| none | head, relation, tail | relation | the string none | ATOMIC 2020 | Not defined. |
| split | ATOMIC10X example | not a relation | split | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| rec_0.5 | ATOMIC10X example | not a relation | rec_0.5 | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| rec_0.6 | ATOMIC10X example | not a relation | rec_0.6 | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| rec_0.7 | ATOMIC10X example | not a relation | rec_0.7 | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| rec_0.8 | ATOMIC10X example | not a relation | rec_0.8 | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| rec_0.9 | ATOMIC10X example | not a relation | rec_0.9 | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
| p_valid_model | ATOMIC10X example | not a relation | p_valid_model | ATOMIC10X. Not a second copy of the 2020 graph. Enters unrated. | Not defined. |
