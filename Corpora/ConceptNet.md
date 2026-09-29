# ConceptNet

ConceptNet attests an assertion of a relation between two concepts.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| /r/RelatedTo | The most general relation. There is some positive relationship between A and B, but ConceptNet can't determine what that relationship is based on the data. This was called "ConceptuallyRelatedTo" in ConceptNet 2 through 4. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/FormOf | A is an inflected form of B; B is the root word of A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/IsA | A is a subtype or a specific instance of B; every A is a B. This can include specific instances; the distinction between subtypes and instances is often blurry in language. This is the hyponym relation in WordNet. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/PartOf | A is a part of B. This is the part meronym relation in WordNet. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasA | B belongs to A, either as an inherent part or due to a social construct of possession. HasA is often the reverse of PartOf. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/UsedFor | A is used for B; the purpose of A is B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/CapableOf | Something that A can typically do is B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/AtLocation | A is a typical location for B, or A is the inherent location of B. Some instances of this would be considered meronyms in WordNet. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/Causes | A and B are events, and it is typical for A to cause B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasSubevent | A and B are events, and B happens as a subevent of A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasFirstSubevent | A is an event that begins with subevent B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasLastSubevent | A is an event that concludes with subevent B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasPrerequisite | In order for A to happen, B needs to happen; B is a dependency of A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasProperty | A has B as a property; A can be described as B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/MotivatedByGoal | Someone does A because they want result B; A is a step toward accomplishing the goal B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/ObstructedBy | A is a goal that can be prevented by B; B is an obstacle in the way of A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/Desires | A is a conscious entity that typically wants B. Many assertions of this type use the appropriate language's word for "person" as A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/CreatedBy | B is a process or agent that creates A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/Synonym | A and B have very similar meanings. They may be translations of each other in different languages. This is the synonym relation in WordNet as well. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/Antonym | A and B are opposites in some relevant way, such as being opposite ends of a scale, or fundamentally similar things with a key difference between them. Counterintuitively, two concepts must be quite similar before people consider them antonyms. This is the antonym relation in WordNet as well. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/DistinctFrom | A and B are distinct member of a set; something that is A is not B. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/DerivedFrom | A is a word or phrase that appears within B and contributes to B's meaning. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/SymbolOf | A symbolically represents B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/DefinedAs | A and B overlap considerably in meaning, and B is a more explanatory version of A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/MannerOf | A is a specific way to do B. Similar to "IsA", but for verbs. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/LocatedNear | A and B are typically found near each other. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/HasContext | A is a word used in the context of B, which could be a topic area, technical field, or regional dialect. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/SimilarTo | A is similar to B. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/EtymologicallyRelatedTo | A and B have a common origin. Symmetric. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/EtymologicallyDerivedFrom | A is derived from B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/CausesDesire | A makes someone want B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/MadeOf | A is made of B. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/ReceivesAction | B can be done to A. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/ExternalURL | Instead of relating to ConceptNet nodes, this pseudo-relation points to a URL outside of ConceptNet, where further Linked Data about this term can be found. Similar to RDF's `seeAlso` relation. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/dbpedia/* | /r/dbpedia/* relations represent abandoned attempts to expand the knowledge we get from DBPedia. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/InstanceOf | /r/InstanceOf expresses "A is an example of B", but because natural language rarely distinguishes this from "A is a type of B", it should be merged with /r/IsA. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/Entails | /r/Entails says that "if A is happening, B is also happening". Instances of Entails should either become MannerOf or HasPrerequisite. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/NotDesires | The negative relations that we have data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/NotUsedFor | The negative relations that we have data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/NotCapableOf | The negative relations that we have data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| /r/NotHasProperty | The negative relations that we have data for are NotDesires, NotUsedFor, NotCapableOf, and NotHasProperty. These are expressed as negative versions of those relations. | the start concept and the end concept | the assertion | ConceptNet | /vault/Data/ConceptNet/documentation/Relations.md |
| weight | the strength with which this edge expresses this assertion. A typical weight is 1, but weights can be higher or lower. All weights are positive. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| sources | the sources that, when combined, say that this assertion should be true. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| license | a Creative Commons URI for the license that governs this data. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| dataset | a URI representing the dataset, or the batch of data from a particular source that created this edge. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| surfaceText | the original natural language text that expressed this statement. May be null, because not every statement was derived from natural language input. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| rel | the URI of the predicate (relation) of this assertion. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| start | the URI of the first argument of the assertion. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| end | the URI of the second argument of the assertion. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| uri | a unique URI for the assertion being expressed. | the assertion | the field | ConceptNet | /vault/Data/ConceptNet/documentation/Edges.md |
| concept URI | Each concept has at least three components: the initial /c to make it a concept, a part that indicates its language (using the BCP 47 language code for that language), and a part with the concept text. An optional fourth component gives the part of speech (as a single letter, following the convention of WordNet). | a concept | the URI | ConceptNet | /vault/Data/ConceptNet/documentation/URI-hierarchy.md |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| assertion line | URI of the whole edge, relation, start node, end node, JSON structure of additional information | One edge. Downloads.md says these are the five fields of each line. Edges.md names the JSON fields weight, sources, license, dataset, and surfaceText, and does not fix their order inside the JSON. | /vault/Data/ConceptNet/documentation/Downloads.md; /vault/Data/ConceptNet/documentation/Edges.md |
| concept URI | /c, language, concept text, optional part-of-speech letter | A concept, also called a term. URI-hierarchy.md lists the part-of-speech letters n, v, a, s, and r. | /vault/Data/ConceptNet/documentation/URI-hierarchy.md |
