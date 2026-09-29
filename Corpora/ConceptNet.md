# ConceptNet

ConceptNet attests an assertion of a relation between two concepts.

## Format

| Record | Field | Order | Type | Specification |
| --- | --- | --- | --- | --- |
| assertion | uri | 1 | URI | The URI of the whole edge. A unique URI for the assertion being expressed. Called `@id` in the Linked Data API. |
| assertion | rel | 2 | URI | The relation expressed by the edge. The URI of the predicate of this assertion. The relation is the mask ([Claims](../Semantics/Claims.md#masks)). |
| assertion | start | 3 | URI | The node at the start of the edge. The URI of the first argument of the assertion. |
| assertion | end | 4 | URI | The node at the end of the edge. The URI of the second argument of the assertion. |
| assertion | weight | 5, inside the JSON | number | The strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive. The fifth column is a JSON object. This file does not fix the order of keys inside it. |
| assertion | sources | 5, inside the JSON | list | The sources that, when combined, say that this assertion should be true. |
| assertion | license | 5, inside the JSON | URI | A Creative Commons URI for the license that governs this data. |
| assertion | dataset | 5, inside the JSON | URI | A URI representing the dataset, or the batch of data from a particular source that created this edge. |
| assertion | surfaceText | 5, inside the JSON | string or null | The original natural language text that expressed this statement. May be null, because not every statement was derived from natural language input. The locations of the start and end concepts are marked by surrounding them with double brackets. |

## Value

| Field | Composition | Mask | What is recorded | Lineage or hop | Specification |
| --- | --- | --- | --- | --- | --- |
| /r/RelatedTo | assertion (start, rel, end) | /r/RelatedTo | end | ConceptNet | The most general relation. There is some positive relationship between A and B, but ConceptNet can't determine what that relationship is based on the data. This was called "ConceptuallyRelatedTo" in ConceptNet 2 through 4. Symmetric. |
| /r/FormOf | assertion (start, rel, end) | /r/FormOf | end | ConceptNet | A is an inflected form of B; B is the root word of A. |
| /r/IsA | assertion (start, rel, end) | /r/IsA | end | ConceptNet | A is a subtype or a specific instance of B; every A is a B. This can include specific instances; the distinction between subtypes and instances is often blurry in language. This is the hyponym relation in WordNet. |
| /r/PartOf | assertion (start, rel, end) | /r/PartOf | end | ConceptNet | A is a part of B. This is the part meronym relation in WordNet. |
| /r/HasA | assertion (start, rel, end) | /r/HasA | end | ConceptNet | B belongs to A, either as an inherent part or due to a social construct of possession. HasA is often the reverse of PartOf. |
| /r/UsedFor | assertion (start, rel, end) | /r/UsedFor | end | ConceptNet | A is used for B; the purpose of A is B. |
| /r/CapableOf | assertion (start, rel, end) | /r/CapableOf | end | ConceptNet | Something that A can typically do is B. |
| /r/AtLocation | assertion (start, rel, end) | /r/AtLocation | end | ConceptNet | A is a typical location for B, or A is the inherent location of B. Some instances of this would be considered meronyms in WordNet. |
| /r/Causes | assertion (start, rel, end) | /r/Causes | end | ConceptNet | A and B are events, and it is typical for A to cause B. |
| /r/HasSubevent | assertion (start, rel, end) | /r/HasSubevent | end | ConceptNet | A and B are events, and B happens as a subevent of A. |
| /r/HasFirstSubevent | assertion (start, rel, end) | /r/HasFirstSubevent | end | ConceptNet | A is an event that begins with subevent B. |
| /r/HasLastSubevent | assertion (start, rel, end) | /r/HasLastSubevent | end | ConceptNet | A is an event that concludes with subevent B. |
| /r/HasPrerequisite | assertion (start, rel, end) | /r/HasPrerequisite | end | ConceptNet | In order for A to happen, B needs to happen; B is a dependency of A. |
| /r/HasProperty | assertion (start, rel, end) | /r/HasProperty | end | ConceptNet | A has B as a property; A can be described as B. |
| /r/MotivatedByGoal | assertion (start, rel, end) | /r/MotivatedByGoal | end | ConceptNet | Someone does A because they want result B; A is a step toward accomplishing the goal B. |
| /r/ObstructedBy | assertion (start, rel, end) | /r/ObstructedBy | end | ConceptNet | A is a goal that can be prevented by B; B is an obstacle in the way of A. |
| /r/Desires | assertion (start, rel, end) | /r/Desires | end | ConceptNet | A is a conscious entity that typically wants B. Many assertions of this type use the appropriate language's word for "person" as A. |
| /r/CreatedBy | assertion (start, rel, end) | /r/CreatedBy | end | ConceptNet | B is a process or agent that creates A. |
| /r/Synonym | assertion (start, rel, end) | /r/Synonym | end | ConceptNet | A and B have very similar meanings. They may be translations of each other in different languages. This is the synonym relation in WordNet as well. Symmetric. |
| /r/Antonym | assertion (start, rel, end) | /r/Antonym | end | ConceptNet | A and B are opposites in some relevant way, such as being opposite ends of a scale, or fundamentally similar things with a key difference between them. Counterintuitively, two concepts must be quite similar before people consider them antonyms. This is the antonym relation in WordNet as well. Symmetric. |
| /r/DistinctFrom | assertion (start, rel, end) | /r/DistinctFrom | end | ConceptNet | A and B are distinct member of a set; something that is A is not B. Symmetric. |
| /r/DerivedFrom | assertion (start, rel, end) | /r/DerivedFrom | end | ConceptNet | A is a word or phrase that appears within B and contributes to B's meaning. |
| /r/SymbolOf | assertion (start, rel, end) | /r/SymbolOf | end | ConceptNet | A symbolically represents B. |
| /r/DefinedAs | assertion (start, rel, end) | /r/DefinedAs | end | ConceptNet | A and B overlap considerably in meaning, and B is a more explanatory version of A. |
| /r/MannerOf | assertion (start, rel, end) | /r/MannerOf | end | ConceptNet | A is a specific way to do B. Similar to "IsA", but for verbs. |
| /r/LocatedNear | assertion (start, rel, end) | /r/LocatedNear | end | ConceptNet | A and B are typically found near each other. Symmetric. |
| /r/HasContext | assertion (start, rel, end) | /r/HasContext | end | ConceptNet | A is a word used in the context of B, which could be a topic area, technical field, or regional dialect. |
| /r/SimilarTo | assertion (start, rel, end) | /r/SimilarTo | end | ConceptNet | A is similar to B. Symmetric. |
| /r/EtymologicallyRelatedTo | assertion (start, rel, end) | /r/EtymologicallyRelatedTo | end | ConceptNet | A and B have a common origin. Symmetric. |
| /r/EtymologicallyDerivedFrom | assertion (start, rel, end) | /r/EtymologicallyDerivedFrom | end | ConceptNet | A is derived from B. |
| /r/CausesDesire | assertion (start, rel, end) | /r/CausesDesire | end | ConceptNet | A makes someone want B. |
| /r/MadeOf | assertion (start, rel, end) | /r/MadeOf | end | ConceptNet | A is made of B. |
| /r/ReceivesAction | assertion (start, rel, end) | /r/ReceivesAction | end | ConceptNet | B can be done to A. |
| /r/ExternalURL | assertion (start, rel, end) | /r/ExternalURL | end | ConceptNet | Instead of relating to ConceptNet nodes, this pseudo-relation points to a URL outside of ConceptNet, where further Linked Data about this term can be found. Similar to RDF's seeAlso relation. |
| /r/dbpedia/* | assertion (start, rel, end) | /r/dbpedia/* | end | ConceptNet | Deprecated. /r/dbpedia/* relations represent abandoned attempts to expand the knowledge we get from DBPedia. |
| /r/InstanceOf | assertion (start, rel, end) | /r/InstanceOf | end | ConceptNet | Deprecated. /r/InstanceOf expresses "A is an example of B", but because natural language rarely distinguishes this from "A is a type of B", it should be merged with /r/IsA. |
| /r/Entails | assertion (start, rel, end) | /r/Entails | end | ConceptNet | Deprecated. /r/Entails says that "if A is happening, B is also happening". Instances of Entails should either become MannerOf or HasPrerequisite. |
| /r/NotDesires | assertion (start, rel, end) | /r/NotDesires | end | ConceptNet | Deprecated. The negative relations that the file says it has data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. The same paragraph's example /r/NotIsA is not in that list. |
| /r/NotUsedFor | assertion (start, rel, end) | /r/NotUsedFor | end | ConceptNet | Deprecated. The negative relations that the file says it has data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. |
| /r/NotCapableOf | assertion (start, rel, end) | /r/NotCapableOf | end | ConceptNet | Deprecated. The negative relations that the file says it has data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. |
| /r/NotHasProperty | assertion (start, rel, end) | /r/NotHasProperty | end | ConceptNet | Deprecated. The negative relations that the file says it has data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. |
