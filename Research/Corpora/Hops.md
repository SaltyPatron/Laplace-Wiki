# Hops

The lexicons are separate witnesses, and a hop is the curated edge that lets consensus on a claim in one of them pull on a claim in another.

## Files

| Path | Bytes | What the file is | Proof |
| --- | ---: | --- | --- |
| `/vault/Data/SemLink/semlink-master/instances/pb-vn2.json` | 312656 | Mapping file between PropBank and VerbNet. | `/vault/Data/SemLink/semlink-master/README.md` |
| `/vault/Data/SemLink/semlink-master/instances/vn-fn2.json` | 67512 | Mapping file between VerbNet and FrameNet. The same README once calls this file `pb-fn2.json`. The file on disk is `vn-fn2.json`. | `/vault/Data/SemLink/semlink-master/README.md` |
| `/vault/Data/SemLink/semlink-master/instances/semlink-2` | 14217973 | Annotated instances: predicates in the Ontonotes corpora. | `/vault/Data/SemLink/semlink-master/README.md` |
| `/vault/Data/PredicateMatrix.v1.3/PredicateMatrix.v1.3.txt` | 140813653 | Predicate Matrix v1.3 file. 426,696 data rows after a 27-column header. | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `/vault/Data/MapNet-0.1/mapping_frame_synsets.txt` | 124887 | Mapping between FrameNet frames and WordNet synsets. 5,162 lines, the count the README states. | `/vault/Data/MapNet-0.1/README` |
| `/vault/Data/MapNet-0.1/mapping_lus_synsets.txt` | 174794 | Mapping between FrameNet frames, lus, and WordNet synsets. 5,162 lines, the count the README states. | `/vault/Data/MapNet-0.1/README` |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/VA_bn2va.tsv` | 302954 | The synsets in each VerbAtlas frame. | `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/pb2va.tsv` | 245113 | Mapping from PropBank to VerbAtlas. | `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/bn2wn.tsv` | 358024 | One-to-one mapping from BabelNet to WordNet. | `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` |
| `/vault/Data/.refresh-20260903/FrameBase-2.0/FrameBase_schema_core.ttl.gz` | 30159236 | Core schema. RDFS+ schema for representing frame-based knowledge. RDFS+ inference is materialized. | [FrameBase data](https://www.framebase.org/data) |
| `/vault/Data/.refresh-20260903/FrameBase-2.0/FrameBase_schema_lemon_annotations.ttl.gz` | 5114489 | Lemon annotations for the schema. | [FrameBase data](https://www.framebase.org/data) |
| `/vault/Data/.refresh-20260903/FrameBase-2.0/FrameBase_schema_wordnet_30_links.ttl.gz` | 1994485 | `owl:sameAs` links with the RDF version of WordNet. 117,659 triples, every predicate `owl:sameAs`. | [FrameBase data](https://www.framebase.org/data) |
| `/vault/Data/WordFrameNet/WFN/WordFrameNet` | 625643 | The member `WordFrameNet` inside `WFN.tar.gz`. No publisher format file is in the drop. | `/vault/Data/WordFrameNet/WFN.tar.gz` |
| `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` | 451382 | The member `eXtendedWFN` inside `XWFN.tar.gz`. No publisher format file is in the drop. | `/vault/Data/WordFrameNet/XWFN.tar.gz` |
| `/vault/Data/CILI/ili.ttl` | 16777636 | The main interlingual index file, a definition and a source for each identifier, in Turtle. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map.ttl` | 7362300 | Mapping from Princeton WordNet 3.0 to the ILI in Turtle. Byte-identical to `ili-map-wn30.ttl`. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map-wn30.ttl` | 7362300 | The same Princeton WordNet 3.0 Turtle mapping. The README says the two files are identical. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map-pwn30.tab` | 2242075 | Mapping from Princeton WordNet 3.0 to the ILI as tab-separated values. 117,659 rows. CRLF line endings. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map-pwn31.tab` | 2240647 | Mapping from Princeton WordNet 3.1 to the ILI, tab-separated. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map-wn31.ttl` | 7712991 | Mapping from Princeton WordNet 3.1 to the ILI, Turtle. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/ili-map-odwn13.ttl` | 1988636 | Mapping from Open Dutch WordNet 1.3 to the ILI. | `/vault/Data/CILI/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn15.tab` | 1933900 | Automatic mapping from WordNet 1.5 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn16.tab` | 2094701 | Automatic mapping from WordNet 1.6 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn17.tab` | 2297638 | Automatic mapping from WordNet 1.7 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn171.tab` | 2335862 | Automatic mapping from WordNet 1.7.1 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn20.tab` | 2427700 | Automatic mapping from WordNet 2.0 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/CILI/older-wn-mappings/ili-map-pwn21.tab` | 2471139 | Automatic mapping from WordNet 2.1 to the ILI. | `/vault/Data/CILI/older-wn-mappings/README.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` | 1634 | Says these tab files map synset IDs to sense IDs, not ILI ids, and that they are complementary to the ILI maps. | The file |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn15.tab` | 5377042 | One of those synset-to-sense tab files. Column order was not re-counted in this file. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn16.tab` | 5536808 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn17.tab` | 6155965 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn171.tab` | 6262735 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn20.tab` | 6510216 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn21.tab` | 6636519 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn30.tab` | 6637176 | Princeton WordNet 3.0 synset IDs to sense IDs. An opened line is `00001740-r` then `a_cappella%4:02:00::`. Not an ILI map. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md`, the file |
| `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/pwn31.tab` | 6646233 | One of those synset-to-sense tab files. | `/vault/Data/.refresh-20260903/CILI/extracted/sense-mappings/Readme.md` |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| [SemLink](SemLink.md) | Mapping files between PropBank, VerbNet, and FrameNet, plus annotated instances. The README says direct PropBank–FrameNet links are not included and are retrieved through VerbNet. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names SemLink on the Linguistic Super Highway. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | PropBank rolesets and VerbNet classes; VerbNet verb senses and FrameNet frames | The mapping. Not a third lexicon. Designed for VerbNet 3.3, the Unified PropBank frame files, and FrameNet 1.7. | SemLink 2, repository README | `/vault/Data/SemLink/semlink-master/README.md` |
| [Predicate Matrix](Predicate-Matrix.md) | Each row is the mapping of a role over the different resources and the aligned knowledge about its corresponding verb. The README names FrameNet, VerbNet, PropBank, WordNet, NomBank, ESO, AnCora, Basque Verb Index, and the Multilingual Central Repository. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) writes this edge as PredicateMatrix. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | One role, the index of the first four columns, and the resources those columns name | The row. The first four columns are the index. | Predicate Matrix v1.3, IXA Group | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| [MapNet](MapNet.md) | Mapping of FrameNet v. 1.3 frames and lexical units to WordNet 1.6 synsets. "The resource was automatically generated." "The evaluated precision of the mapping 0.794." The README gives that precision to the mapping and no score to a row. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names MapNet. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | FrameNet 1.3 and WordNet 1.6 | The pair of files, 5,162 mappings each. Columns are not named. | MAPNET v.0.1, Sara Tonelli and Daniele Pighin | `/vault/Data/MapNet-0.1/README` |
| [VerbAtlas](VerbAtlas.md) | "The goal of VerbAtlas is to manually cluster WordNet synsets that share similar semantics into a set of semantically-coherent frames." The same package maps PropBank to those frames and BabelNet synsets to WordNet synsets. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) does not name VerbAtlas. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | WordNet synsets and VerbAtlas frames; PropBank predicate senses and VerbAtlas frames | The cluster, and the PropBank mapping shipped beside it | VerbAtlas 1.1.0, Sapienza NLP Group | `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` |
| [FrameBase](FrameBase.md) | RDFS classes for FrameNet frames, and `owl:sameAs` links with the RDF version of WordNet. The schema page says synset-microframes are linked to LU-microframes. This drop is the 2.0 schema files, not the 107 FrameNet 1.7 fulltext XML files. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) does not name FrameBase. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | A FrameBase frame IRI and a WordNet 3.0 RDF synset IRI | The `owl:sameAs` triple | FrameBase 2.0, FrameBase team at Aalborg University and Rutgers University | [FrameBase schema](https://www.framebase.org/schema), [FrameBase data](https://www.framebase.org/data) |
| [WordFrameNet](WordFrameNet.md) | Not defined. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names WordFrameNet. The two files name no witness and define no field. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop; these files do not state an edge. | Not defined | Not defined | Not named in the files | `/vault/Data/WordFrameNet/WFN/WordFrameNet`, `/vault/Data/WordFrameNet/XWFN/eXtendedWFN`, and the queries on [WordFrameNet](WordFrameNet.md) |
| [CILI](Wordnets.md) | A single interlingual index of concepts for wordnets, and the mappings from Princeton WordNet 3.0, Princeton WordNet 3.1, and Open Dutch WordNet 1.3 onto it. Older WordNet versions are separate automatic mappings. [Claims](../../Semantics/Claims.md#the-linguistic-super-highway) names CILI. [Pull](../../Semantics/Pull.md#hop-and-fanout) is the pull across a hop. | A wordnet synset identifier and an ILI identifier | `owl:sameAs` in the Turtle maps; two tab-separated fields in `ili-map-pwn30.tab` and `ili-map-pwn31.tab` | Collaborative Interlingual Index, maintained by the Open Multilingual Wordnet | `/vault/Data/CILI/README.md` |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| `pb-vn2.json` entry | Roleset key, VerbNet class-number key, then an object of argument label to a string | One PropBank roleset mapped to VerbNet classes. 4,177 top-level keys. | `/vault/Data/SemLink/semlink-master/instances/pb-vn2.json` |
| `vn-fn2.json` entry | Key `class-verb`, then a list of frame-name strings | FrameNet frames for one VerbNet verb sense. 1,681 keys. | `/vault/Data/SemLink/semlink-master/instances/vn-fn2.json` |
| `semlink-2` line | Source file, sentence number, token number, verb, VerbNet class, FrameNet frame, PropBank roleset, OntoNotes group, then the remaining argument fields | One annotated predicate instance. | `/vault/Data/SemLink/semlink-master/tools/annotation.py` |
| Predicate Matrix row | The 27 header names, tab-separated | The mapping of one role. The README says the first four columns are the unique index. | `/vault/Data/PredicateMatrix.v1.3/README.txt` |
| `mapping_frame_synsets.txt` line | Two tab-separated fields. The README does not say which is the frame. | One of the 5,162 frame–synset mappings. | `/vault/Data/MapNet-0.1/README` |
| `mapping_lus_synsets.txt` line | Three tab-separated fields. The README names no column. | One of the 5,162 frame / lu / synset mappings. | `/vault/Data/MapNet-0.1/README` |
| `VA_bn2va.tsv` line | BabelNet synset ID, VerbAtlas frame ID | A synset placed in a frame. | `/vault/Data/.refresh-20260903/VerbAtlas-1.1/extracted/VerbAtlas-1.1.0/README.txt` |
| FrameBase WordNet link | WordNet 3.0 RDF IRI, `owl:sameAs`, FrameBase synset-microframe IRI | One link from the RDF edition of WordNet 3.0. | `/vault/Data/.refresh-20260903/FrameBase-2.0/FrameBase_schema_wordnet_30_links.ttl.gz` |
| WordFrameNet line | Not a fixed field list | Not defined. See [WordFrameNet](WordFrameNet.md). | `/vault/Data/WordFrameNet/WFN/WordFrameNet` |
| `eXtendedWFN` line | Three whitespace-separated tokens under a `Frame:` line | Not defined. 20,587 such lines. | `/vault/Data/WordFrameNet/XWFN/eXtendedWFN` |
| `ili-map-pwn30.tab` line | Two fields. The README does not name them. An opened line is `i1` then `00001740-a`. | One Princeton WordNet 3.0 to ILI mapping. The older-mapping README's third field, confidence, is not in this file. | `/vault/Data/CILI/README.md`, `/vault/Data/CILI/ili-map-pwn30.tab` |
| `ili-map.ttl` triple | `ili` identifier, `owl:sameAs`, `pwn30:` identifier, then a `#` comment the README does not define | Mapping between the CILI and Princeton WordNet 3.0. The file's own header says that, produced by Francis Bond (CC BY). | `/vault/Data/CILI/ili-map.ttl` |
| Older WordNet map line | ILI, WNX.X, CONFIDENCE | An automatic mapping from WordNet 1.5, 1.6, 1.7, 1.7.1, 2.0, or 2.1. | `/vault/Data/CILI/older-wn-mappings/README.md` |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| `/vault/Data/SemLink/semlink-master/` and `/vault/Data/.refresh-20260903/SemLink/extracted/semlink-current-2636bf5a4ae9c93b669a1184a8aaae9ca21552d3/` | The same 17 files, byte-identical pairwise, including `.idea/vcs.xml`. The wrapping tar archives differ: 4,782,096 bytes and 4,782,298 bytes. | SHA-256 of each file pair |
| `/vault/Data/MapNet-0.1/MapNet-0.1.zip` and the three files beside it | The zip members `README`, `mapping_frame_synsets.txt`, and `mapping_lus_synsets.txt` match those files byte for byte. | SHA-256 of each zip member and the file beside the zip |
| `/vault/Data/WordFrameNet/WFN.tar.gz` and `/vault/Data/WordFrameNet/XWFN.tar.gz` | Not the same archive and not the same member. 218,272 bytes against 136,895. Each archive has one member, and that member matches the extracted file byte for byte. The 722 `Frame:` lines are the same set of strings. The other lines are not one shared file. | `tarfile` member SHA-256 and a line-set compare |
| `/vault/Data/CILI/ili-map.ttl` and `/vault/Data/CILI/ili-map-wn30.ttl` | Byte-identical, as the README says. The refresh extract's pair is byte-identical to itself and not byte-identical to the live file (7,244,632 bytes against 7,362,300). | SHA-256 |
| `/vault/Data/CILI/ili-map-pwn30.tab` and `/vault/Data/.refresh-20260903/CILI/extracted/ili-map-pwn30.tab` | The same 117,659 records. The live file is CRLF; the refresh file is LF. Sizes 2,242,075 and 2,124,416. | SHA-256 after stripping CR |
| `/vault/Data/CILI/` and `/vault/Data/.refresh-20260903/CILI/extracted/` | Not one snapshot. `ili.ttl` is 16,777,636 bytes live and 16,307,282 in the refresh extract. `sense-mappings/` is only in the refresh extract. The two refresh tarballs differ: 26,758,145 and 26,758,251 bytes. | `stat` of both trees |
| `/vault/Data/.refresh-20260903/FrameBase-2.0/` and `/vault/Data/FrameNet/framenet_v17/fulltext/` | Not the same witness. FrameBase's three files are gzipped triples. They contain no `annotationSet`, no `fulltext`, and no `<sentence`. FrameNet 1.7 fulltext is 107 XML files. | Gzip scan of the three FrameBase files; directory listing of FrameNet fulltext |
| `/vault/Data/.refresh-20260903/VerbAtlas-1.1/VerbAtlas-1.1.0.zip` and `extracted/VerbAtlas-1.1.0/` | Every zip member matches the extracted file byte for byte. There is no VerbAtlas directory under `/vault/Data` outside the refresh tree. | SHA-256; directory listing |
