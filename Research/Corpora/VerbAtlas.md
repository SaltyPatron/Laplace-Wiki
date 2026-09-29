# VerbAtlas

VerbAtlas attests a clustering of WordNet synsets into frames.

## Files

| Path | Bytes | What the file is | Proof |
| --- | ---: | --- | --- |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` | 9401 | README.txt. The title is VerbAtlas 1.1.0. The package list says the inner directory "contains the files for VerbAtlas 1.0.3". | The file |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_frame_info.tsv` | 69736 | Name, id, and other info for each VerbAtlas frame. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_frame_pas.tsv` | 18550 | The argument structure of each VerbAtlas frame. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_va2sp.tsv` | 56452 | The selectional preferences of each VerbAtlas frame. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_bn2va.tsv` | 302954 | The synsets in each VerbAtlas frame. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_preference_info.tsv` | 13806 | "Name, id, reference synset for each preference." The format section describes this under the name `VA_preference_ids.tsv`. | `README.txt` |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_bn2shadow.tsv` | 106252 | Shadow arguments for each synset. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_bn2implicit.tsv` | 33593 | Implicit arguments for each synset. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/pb2va.tsv` | 245113 | Mapping from PropBank to VerbAtlas. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/bn2wn.tsv` | 358024 | One-to-one mapping from BabelNet to WordNet. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/wn2lemma.tsv` | 524134 | Mapping from WordNet synset to lemmas. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/wn2sense.tsv` | 774604 | Mapping from WordNet synset to WordNet sense key. | `README.txt`, package contents |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_synset_preferences.tsv` | 302954 | Present in the package. Not listed under package contents and not described under format. | `README.txt` does not name it; the file is on disk |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Hop | "Manually cluster WordNet synsets that share similar semantics into a set of semantically-coherent frames." [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) does not name VerbAtlas. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. [Hops](Hops.md) lists the edge. | WordNet synsets and VerbAtlas frames | The cluster | VerbAtlas 1.1.0, Sapienza NLP Group | `README.txt` |
| Sources | "VerbAtlas relies on WordNet 3.0, BabelNet 4.0.1, and Proposition Bank I." | Those three resources | The mappings below | VerbAtlas 1.1.0 | `README.txt`, Resources |
| Frame ID | "Each line contains the ID and the name of a VerbAtlas frame, separated by a tab." | The frame | `va:0001f` on the first data line of `VA_frame_info.tsv` | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Frame name | The name of the frame, the second field of `VA_frame_info.tsv`. | The frame ID | `TOLERATE` on that line | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Frame definition | A definition, added in VerbAtlas 1.1.0. | The frame ID | `An agent TOLERATES a theme in favour of a beneficiary (+attribute)` on that line | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Prototypical synset | "The synset that roughly represents the frame." | The frame ID | `bn:00082138v` on that line | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Definition of the prototypical synset | The definition of that synset. | The frame ID | `Put up with something or somebody unpleasant` on that line | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Small definition | A "small definition" of the frame. | The frame ID | `Tolerate, accept, endure.` on that line | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Supporting frame | "Frames with id > 999 (e.g. va:1001f - AUXILIARY) are not semantic frames, but rather supporting frames we added to support other resources like PropBank. Please, do not consider them as core frames of VerbAtlas." | Those frame IDs | The README's example `va:1001f` | VerbAtlas 1.1.0 | `README.txt`, format 1 |
| Argument structure | "Each line contains the ID of a VerbAtlas frame and its argument structure, where each element is separated by a tab." | The frame ID | `va:0001f`, then `Agent`, `Theme`, `Beneficiary`, `Attribute` | VerbAtlas 1.1.0 | `README.txt`, format 2; `VA_frame_pas.tsv` |
| Selectional preference | "The ID of a VerbAtlas frame F followed by the selectional preferences of the roles in F." The default is "entity" (`va:0003p`). Several preferences in one role are separated by a pipe. | The frame, then each role | `va:0001f`, `C`, `Agent`, `va:0081p` and `va:0103p` | VerbAtlas 1.1.0 | `README.txt`, format 3; `VA_va2sp.tsv` |
| Concrete and Abstract | "Some frames support two types of selectional preferences: Concrete (C) and Abstract (A)." | The frame line in `VA_va2sp.tsv` | `C` or `A` after the frame ID | VerbAtlas 1.1.0 | `README.txt`, format 3 |
| BabelNet synset to frame | "Each line contains a BabelNet synset ID and its corresponding VerbAtlas frame ID, separated by a tab." | A BabelNet synset and a VerbAtlas frame | `bn:00082138v`, `va:0001f` | VerbAtlas 1.1.0 | `README.txt`, format 4 |
| Preference ID | "The ID of a VerbAtlas selectional preference." The format section titles the file `VA_preference_ids.tsv`. The file in the package is `VA_preference_info.tsv`. | The preference | `va:0001p` | VerbAtlas 1.1.0 | `README.txt`, format 5 and package contents |
| Preference reference synset | "Its reference BabelNet synset ID." | The preference ID | `bn:00000467n` on the first data line | VerbAtlas 1.1.0 | `README.txt`, format 5 |
| Preference name | "Its name." | The preference ID | `absorbent` on the first data line | VerbAtlas 1.1.0 | `README.txt`, format 5 |
| Fourth field of `VA_preference_info.tsv` | Not defined. The README names three fields. The file has four. | The preference ID and that field | `https://upload.wikimedia.org/wikipedia/commons/3/3a/Sponge-viscose.jpg` on the first data line. That is the field text; the README does not say what it is. | Not defined | `VA_preference_info.tsv`; `README.txt` format 5 |
| Shadow argument | "The shadow arguments, if any, for each BabelNet synset ID. A synset may support multiple shadow arguments in different roles." | The BabelNet synset, then a role, then the argument | `bn:00082124v`, `Stimulus`, `bn:00030466n` | VerbAtlas 1.1.0 | `README.txt`, format 6 |
| Implicit argument | "The implicit arguments, if any, for each BabelNet synset ID." A role may have multiple implicit arguments, separated by a pipe. | The BabelNet synset, then a role, then the arguments | `bn:00082162v`, `Patient`, `bn:00035378n`, `bn:00035596n`, `bn:00036686n` joined by pipes | VerbAtlas 1.1.0 | `README.txt`, format 7 |
| PropBank to VerbAtlas | "Each line maps a PropBank predicate sense and its corresponding argument structure to a VerbAtlas frame and its argument structure" as `[PB predicate sense]>[VA frame]` then `[PB role]>[VA role]`. | A PropBank predicate sense and a VerbAtlas frame, and each PropBank role and VerbAtlas role | `abandon.01>va:0255f`, then `A0>Agent`, `A1>Theme`, `A2>Attribute` | VerbAtlas 1.1.0 | `README.txt`, format 8 |
| BabelNet to WordNet | "A mapping from BabelNet synset to WordNet synset for verbs. Each line contains a BabelNet synset ID and its corresponding WordNet synset ID, separated by a tab." | A BabelNet synset and a WordNet synset | `bn:00082116v`, `wn:00865776v` | VerbAtlas 1.1.0, under the BabelNet 4.0 license line in the file | `README.txt`, format 9 |
| WordNet synset to lemma | "Each line contains a WordNet synset ID and a lemma, separated by a tab." The same synset ID may appear on multiple lines, and the same lemma may appear on multiple lines. | A WordNet synset | `wn:00001740v`, `breathe` | VerbAtlas 1.1.0; this file is under the WordNet 3.0 license, not CC BY-NC-SA 4.0 | `README.txt`, format 10 and package contents |
| WordNet synset to sense key | "Each line contains a WordNet synset ID and a WordNet sense key, separated by a tab." The same synset ID may appear on multiple lines. | A WordNet synset | `wn:00001740v`, `breathe%2:29:00::` | VerbAtlas 1.1.0; WordNet 3.0 license | `README.txt`, format 11 |
| `VA_synset_preferences.tsv` | Not defined. The README neither lists it under package contents nor describes it under format. | The two fields of the line | Two tab-separated fields. The first data line is `bn:00082116v` then `CONCRETE`. | Not defined | The file; absence from `README.txt` package contents and format |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `VA_frame_info.tsv` | ID, name, definition, prototypical synset, definition of the prototypical synset, small definition | One VerbAtlas frame. 432 data lines of width 6, after one license line. | `README.txt`, format 1; the file |
| `VA_frame_pas.tsv` | Frame ID, then one tab-separated element per argument | The argument structure of one frame. Width is not fixed. The six most common data widths are 5, 4, 6, 7, 3, and 8 fields, and those six do not cover every data line. One license line, then 426 data lines. | `README.txt`, format 2; the file |
| `VA_va2sp.tsv` | Frame ID, `C` or `A`, then repeating pairs of role and preference list | Selectional preferences of one frame at one type. Width is not fixed. | `README.txt`, format 3; the file |
| `VA_bn2va.tsv` | BabelNet synset ID, VerbAtlas frame ID | One synset in one frame. 13,767 data lines after one license line. | `README.txt`, format 4 |
| `VA_preference_info.tsv` | ID, reference BabelNet synset ID, name, then a fourth field the README does not name | One selectional preference, plus that extra field. 122 data lines of width 4 after one license line. | `README.txt`, format 5; the file |
| `VA_bn2shadow.tsv` | BabelNet synset ID, then repeating pairs of role and shadow argument | Shadow arguments of one synset. Most data lines have 3 fields; some have 5, 7, or 9. | `README.txt`, format 6; the file |
| `VA_bn2implicit.tsv` | BabelNet synset ID, then repeating pairs of role and pipe-separated arguments | Implicit arguments of one synset. | `README.txt`, format 7; the file |
| `pb2va.tsv` | `[PB predicate sense]>[VA frame]`, then one `[PB role]>[VA role]` per further field | One PropBank sense mapped onto a VerbAtlas frame and roles. Width is not fixed. | `README.txt`, format 8; the file |
| `bn2wn.tsv` | BabelNet synset ID, WordNet synset ID | One BabelNet verb synset and one WordNet synset. 13,767 data lines after a `#` license line. | `README.txt`, format 9 |
| `wn2lemma.tsv` | WordNet synset ID, lemma | One lemma of one synset. 25,047 lines, no license line. | `README.txt`, format 10 |
| `wn2sense.tsv` | WordNet synset ID, WordNet sense key | One sense key of one synset. 25,047 lines, no license line. | `README.txt`, format 11 |
| `VA_synset_preferences.tsv` | Two fields. Not named. | Not defined. 13,767 data lines of width 2 after one license line. | The file |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/VerbAtlas-1.1.0.zip` and `extracted/VerbAtlas-1.1.0/` | Every zip member matches the extracted file byte for byte. | SHA-256 |
| WordNet 3.0 | `wn2lemma.tsv` and `wn2sense.tsv` are under the WordNet 3.0 license. The README says the other files are CC BY-NC-SA 4.0, and `bn2wn.tsv` is under the BabelNet 4.0 license. | `README.txt`, package contents |
| `/vault/Data/` outside the refresh tree | No VerbAtlas directory there. | Directory listing |
