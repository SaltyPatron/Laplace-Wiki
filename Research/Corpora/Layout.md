# Corpus layout

Every collection under `/vault/Data`, `/vault/Data/.refresh-20260903`, and `/vault/models` is listed with its file count, its size, and its largest files.

The sizes were measured on 2026-09-29. `/vault/models`, `code-authority`, `TreeSitter`, `.git-cache`, and `.jobs` are `du` totals, with a hard link counted once. The other rows are sums of file sizes. Contents of `.git` directories are not in the totals. `omw` and `OMW` are two checkouts of one build repository; the OMW 2.0 release is the separate `OMW-2.0` tree in the refresh directory. A model directory that holds both `snapshots/` and `blobs/` includes both in its size.

## `/vault/Data`

| Collection | Files | Size | Largest files |
| --- | ---: | ---: | --- |
| [Atomic2020](ATOMIC.md) | 7 | 66.0 MB | `train.tsv`, `test.tsv` |
| [CILI](Wordnets.md) | 22 | 56.5 MB | `ili.ttl`, `ili-map-wn31.ttl` |
| `COCO` | 5,002 | 1.5 GB | `val2017.zip`, `val2017/000000163682.jpg` |
| `code-authority` | 96,177 | 1.3 GB | `cpython`, `docs`, `postgres`, `runtime` |
| [ConceptNet](ConceptNet.md) | 6 | 9.5 GB | `assertions.csv`, `documentation/Relations.md` |
| [FrameNet](FrameNet.md) | 14,932 | 910.0 MB | `framenet_v17.zip`, `framenet_v17/miscXML/lemma_to_wordformR1.7.xml` |
| `Games` | 426 | 18.9 GB | `Chess/Lumbras/online/LumbrasGigaBase_Online_2024.pgn`, `Chess/Lumbras/otb/LumbrasGigaBase_OTB_2010-2014.pgn` |
| [ISO639](ISO-639.md) | 78 | 7.4 MB | `cldr/likelySubtags.xml`, `iana/language-subtag-registry.txt` |
| `LaplaceAssets` | 12 | 25.7 MB | `Laplace_Patreon_Post2.png`, `Laplace_Title_Bar.png` |
| `LaplacePatreon` | 8 | 1.5 MB | `images/01-glome-of-unicode.png`, `images/03-falling-inward.png` |
| `LaplacePrototype` | 1,784 | 18.7 GB | `out/gutenberg/physicality.copy`, `pgdata/base/16384/19094.1` |
| `LaplaceResearch` | 8,066 | 1.7 GB | `models/stanza/en/depparse/combined_charlm.pt`, `models/stanza/en/pretrain/conll17.pt` |
| [MapNet-0.1](MapNet.md) | 4 | 369.2 KB | `mapping_lus_synsets.txt`, `mapping_frame_synsets.txt` |
| `nltk_data` | 504 | 12.8 MB | `corpora/brown.zip`, `corpora/brown/CONTENTS` |
| [omw](Wordnets.md) | 1,424 | 146.4 MB | `wns/jpn/wn-data-jpn.tab`, `wns/ron/wn-data-ron.tab` |
| [OMW](Wordnets.md) | 1,424 | 146.4 MB | `wns/jpn/wn-data-jpn.tab`, `wns/ron/wn-data-ron.tab` |
| [OpenSubtitles](OpenSubtitles.md) | 16 | 15.3 GB | `en-es.txt.zip`, `ar-en.txt.zip` |
| [PredicateMatrix.v1.3](Predicate-Matrix.md) | 2 | 134.3 MB | `PredicateMatrix.v1.3.txt`, `README.txt` |
| [ProjectGutenberg](Project-Gutenberg.md) | 223 | 203.3 MB | `text/webster-unabridged-dictionary-1913.txt`, `text/britannica-1911-bulgaria-to-calgary.txt` |
| [PropBank](PropBank.md) | 7,579 | 37.8 MB | `propbank-frames-main.zip`, `propbank-frames-main/AMR-UMR-91-rolesets.xml` |
| [SemLink](SemLink.md) | 19 | 28.6 MB | `semlink-master/instances/semlink-2`, `semlink-master/other_resources/1.2.2c.okay` |
| [Tatoeba](Tatoeba.md) | 8 | 5.3 GB | `audio/tatoeba_audio_eng.zip`, `sentences.csv` |
| `test-data` | 48 | 13.7 MB | `text/newton.zip`, `electronics/ncvec-2024-2028-extra-class-pool.pdf` |
| `TreeSitter` | 21,960 | 1.6 GB | `tree-sitter-nim/src/parser.c`, `tree-sitter-systemverilog/src/parser.c` |
| [UCD](Unicode.md) | 136 | 733.5 MB | `Public/UCD/latest/ucdxml/ucd.all.flat.xml`, `Public/UCD/latest/charts/fr/CodeCharts.pdf` |
| [UD-Treebanks](Universal-Dependencies.md) | 2,408 | 4.2 GB | `ud-treebanks-v2.17.tgz`, `ud-treebanks-v2.17/UD_Czech-PDTC/cs_pdtc-ud-train.conllu` |
| `Unicode.BAD-DONOTUSE` | 23,038 | 36.7 GB | `irg/docs/n2835-Evidence.zip`, `wg2/docs/n5221-Proposed Horizontal Extension.pdf` |
| [VerbNet](VerbNet.md) | 1,023 | 11.4 MB | `verbnet-master.zip`, `verbnet-master/vn-gl/say-37.7.xml` |
| [Wiktionary](Wiktionary.md) | 4 | 33.8 GB | `raw-wiktextract-data.jsonl`, `en/enwiktionary-latest-pages-articles.xml` |
| [WordFrameNet](WordFrameNet.md) | 4 | 1.4 MB | `WFN/WordFrameNet`, `XWFN/eXtendedWFN` |
| [Wordnet](Wordnets.md) | 187 | 48.5 MB | `WordNet-3.0/dict/data.noun`, `WordNet-3.0.tar.gz` |
| [WSD](Word-Sense-Disambiguation.md) | 56 | 1.5 GB | `WSD_Evaluation_Framework/Training_Corpora/SemCor+OMSTI/semcor+omsti.data.xml`, `WSD_Evaluation_Framework.zip` |

## `/vault/Data/.refresh-20260903`

| Collection | Files | Size | Largest files |
| --- | ---: | ---: | --- |
| [Atomic](ATOMIC.md) | 1 | 1.4 GB | `ATOMIC10X.jsonl` |
| [CILI](Wordnets.md) | 44 | 153.4 MB | `cili-current-a895d7ecb18019dda3443f98901e59d81ce8722b.tar.gz`, `cili-a895d7ecb18019dda3443f98901e59d81ce8722b.tar.gz` |
| [FrameBase-2.0](FrameBase.md) | 3 | 35.5 MB | `FrameBase_schema_core.ttl.gz`, `FrameBase_schema_lemon_annotations.ttl.gz` |
| `Games` | 0 | 0 B | empty directory |
| [GeoNames](GeoNames.md) | 14 | 3.0 GB | `extracted/allCountries.txt`, `extracted/alternateNamesV2.txt` |
| `LichessOpenings` | 3 | 59.9 KB | `lichess-openings-4b8622759e7ae6f93f011cc6c83a3823401ab45e.tar.gz`, `lichess-openings-4b8622759e7ae6f93f011cc6c83a3823401ab45e.tar.gz.sha256` |
| `NaturalEarth` | 2 | 333.6 KB | `ne_110m_admin_0_countries-5.1.1.zip`, `ne_110m_populated_places-5.1.2.zip` |
| [OMW-2.0](Wordnets.md) | 118 | 622.4 MB | `extracted/omw-2.0/omw-en/omw-en.xml`, `omw-2.0.tar.xz` |
| [OpenEnglishWordNet-2025-plus](Wordnets.md) | 1 | 12.3 MB | `english-wordnet-2025-plus.xml.gz` |
| [PropBank](PropBank.md) | 7,580 | 32.8 MB | `propbank-current-c66e0ccf28b53f00051b187db83e937b5bee2e32.tar.gz`, `extracted/propbank-current-c66e0ccf28b53f00051b187db83e937b5bee2e32/AMR-UMR-91-rolesets.xml` |
| `Safety` | 273 | 2.9 GB | `CivilComments/civil-comments-f2970eb3a55777454c94069077cc8d9b5866312d/extracted/data/train-00000-of-00002.tsv`, `CivilComments/civil-comments-f2970eb3a55777454c94069077cc8d9b5866312d/extracted/data/train-00001-of-00002.tsv` |
| [SemLink](SemLink.md) | 20 | 28.6 MB | `extracted/semlink-current-2636bf5a4ae9c93b669a1184a8aaae9ca21552d3/instances/semlink-2`, `extracted/semlink-current-2636bf5a4ae9c93b669a1184a8aaae9ca21552d3/other_resources/1.2.2c.okay` |
| [Tatoeba](Tatoeba.md) | 25 | 3.7 GB | `extracted/sentences_detailed.csv`, `extracted/sentences.csv` |
| `TWIC` | 10 | 23.4 MB | `twic1657g.zip`, `twic1656g.zip` |
| [UD-Docs](Universal-Dependencies.md) | 154 | 53.1 MB | `docs-pages-source.tar.gz`, `extracted/docs-pages-source/format.md` |
| [UD-Tools](Universal-Dependencies.md) | 11 | 6.4 MB | `10ce40cf8a577714e51cf56b443dd4c2c6d55f91/data/feats.json`, `10ce40cf8a577714e51cf56b443dd4c2c6d55f91/data/docfeats.json` |
| [UD-Treebanks](Universal-Dependencies.md) | 2,502 | 4.3 GB | `ud-treebanks-v2.18.tgz`, `extracted/ud-treebanks-v2.18/UD_Czech-PDTC/cs_pdtc-ud-train.conllu` |
| [VerbAtlas-1.1](VerbAtlas.md) | 18 | 3.3 MB | `extracted/VerbAtlas-1.1.0/VerbAtlas-1.1.0/wn2sense.tsv`, `VerbAtlas-1.1.0.zip` |
| [VerbNet](VerbNet.md) | 1,024 | 10.8 MB | `verbnet-current-ae8e9cfdc2c0d3414b748763612f1a0a34194cc1.tar.gz`, `extracted/verbnet-current-ae8e9cfdc2c0d3414b748763612f1a0a34194cc1/vn-gl/say-37.7.xml` |
| [Wiktionary](Wiktionary.md) | 1 | 2.6 GB | `raw-wiktextract-data-2026-08-28.jsonl.gz` |

## Files the refresh tooling wrote

These files sit in `/vault/Data/.refresh-20260903` beside the collections. They are checksums, staging tables, a git object cache, and download job state written by the refresh tooling.

| Collection | Files | Size | Largest files |
| --- | ---: | ---: | --- |
| `.git-cache` | 375 | 44.8 MB | git objects cached by the refresh tooling |
| `.jobs` | 166 | 39.7 KB | download job state |
| `DOWNLOADS.local.sha256` | 1 | 390.2 KB | `DOWNLOADS.local.sha256` |
| `DOWNLOADS.sha256` | 1 | 5.0 KB | `DOWNLOADS.sha256` |
| `project-gutenberg-relocation.tsv` | 1 | 40.0 KB | `project-gutenberg-relocation.tsv` |
| `REFRESH_RECEIPT.tsv` | 1 | 19.1 KB | `REFRESH_RECEIPT.tsv` |
| `STAGING_LOCAL.tsv` | 1 | 404.4 KB | `STAGING_LOCAL.tsv` |
| `STAGING_MANIFEST.tsv` | 1 | 5.2 KB | `STAGING_MANIFEST.tsv` |

## `/vault/models`

| Collection | Files | Size | Largest files |
| --- | ---: | ---: | --- |
| `.locks` | 32 | 8.1 KB | `.lock` files |
| `code-corpus` | 397,004 | 28.6 GB | `vault-E-Repositories/LotteryAI/.venv` |
| `Conditional-DETR-R50` | 13 | 332.3 MB | `pytorch_model.bin` |
| `DETR-ResNet-101` | 13 | 463.3 MB | `pytorch_model.bin` |
| `Florence-2-base` | 33 | 887.2 MB | `pytorch_model.bin` |
| `Florence-2-large` | 37 | 2.9 GB | `pytorch_model.bin` |
| `gguf` | 4 | 5.8 GB | `TinyLlama-1.1B-Chat-v1.0-f16.gguf`, `qwen3-embedding-0.6b-F16.gguf` |
| `Grounding-DINO-Base` | 21 | 1.7 GB | `pytorch_model.bin` |
| `models--deepseek-ai--deepseek-coder-33b-instruct` | 24 | 124.2 GB | `61dc97b922b13995e7f83b7c8397701dbf9cfd4c/pytorch_model-00005-of-00007.bin` |
| `models--deepseek-ai--DeepSeek-Coder-V2-Lite-Instruct` | 15 | 29.3 GB | `e434a23f91ba5b4923cf6c9d9a238eb4a08e3a11/model-00001-of-000004.safetensors` |
| `models--facebook--sam-audio-large` | 5 | 13.8 GB | `5f2cd3a9471a08c7282c06036be6893e18de8b70/checkpoint.pt` |
| `models--fishaudio--fish-speech-1.5` | 7 | 1.4 GB | `275a984d33c33659e39eed41ff5bcd6e67517f4c/model.pth` |
| `models--ibm-granite--granite-speech-3.3-8b` | 25 | 16.2 GB | `315afb31116c9b79dc15864d091e59ca6bf10cf9/model-00001-of-00009.safetensors` |
| `models--jinaai--jina-code-embeddings-1.5b` | 10 | 2.9 GB | `39aeb4fb9b60f930934c78ae5d749a46287c248a/model.safetensors` |
| `models--jinaai--jina-reranker-v3` | 11 | 1.1 GB | `050e171c4f75dfec5b648ed8470a2475e5a30f30/model.safetensors` |
| `models--microsoft--phi-2` | 37 | 10.4 GB | `810d367871c1d460086d9f82db8696f2e0a0fcd0/model-00001-of-00002.safetensors` |
| `models--nvidia--canary-qwen-2.5b` | 5 | 4.8 GB | `6cfc37ec7edc35a0545c403f551ecdfa28133d72/model.safetensors` |
| `models--nvidia--music-flamingo-hf` | 20 | 15.4 GB | `e29cfe92e682616f8f8014c60b2c5d17a37d4e33/model-00002-of-00004.safetensors` |
| `models--Qwen--Qwen2.5-Coder-14B-Instruct` | 16 | 27.5 GB | `aedcc2d42b622764e023cf882b6652e646b95671/model-00001-of-00006.safetensors` |
| `models--Qwen--Qwen2.5-Coder-3B-Instruct` | 12 | 5.8 GB | `488639f1ff808d1d3d0ba301aef8c11461451ec5/model-00001-of-00002.safetensors` |
| `models--Qwen--Qwen2.5-Coder-7B-Instruct` | 18 | 14.2 GB | `c03e6d358207e414f1eca0bb1891e29f1db0e242/model-00002-of-00004.safetensors` |
| `models--Qwen--Qwen2.5-Coder-7B-Instruct-AWQ` | 35 | 3.0 GB | `.cache/huggingface/download/aoe4E07IMh7reFyUkVoVk040mQk=.70cd6143ef90057120a829e73ef48fe9718d84672a075eea3a0ed167ac08fcb7.incomplete` |
| `models--Qwen--Qwen3-Coder-30B-A3B-Instruct` | 28 | 56.9 GB | `b2cff646eb4bb1d68355c01b18ae02e7cf42d120/model-00007-of-00016.safetensors` |
| `models--Qwen--Qwen3-Embedding-0.6B` | 13 | 1.1 GB | `c54f2e6e80b2d7b7de06f51cec4959f6b3e03418/model.safetensors` |
| `models--Qwen--Qwen3-Embedding-4B` | 16 | 7.5 GB | `5cf2132abc99cad020ac570b19d031efec650f2b/model-00001-of-00002.safetensors` |
| `models--Qwen--Qwen3-Reranker-0.6B` | 10 | 1.1 GB | `6e9e69830b95c52b5fd889b7690dda3329508de3/model.safetensors` |
| `models--Qwen--Qwen3-Reranker-4B` | 13 | 7.5 GB | `f16fc5d5d2b9b1d0db8280929242745d79794ef5/model-00001-of-00002.safetensors` |
| `models--Qwen--Qwen3-VL-Embedding-2B` | 15 | 4.0 GB | `929a0c31d84149ec61d4594889136e0c663af1a6/model.safetensors` |
| `models--Qwen--Qwen3-VL-Embedding-8B` | 19 | 15.2 GB | `a12d6118f720ceb6d95f7d1cad4e8aeccddd9340/model-00001-of-00004.safetensors` |
| `models--Qwen--Qwen3-VL-Reranker-2B` | 16 | 4.0 GB | `76219daff7a696073e0ab28b74fa32aa81183052/model.safetensors` |
| `models--Qwen--Qwen3-VL-Reranker-8B` | 20 | 16.3 GB | `8e52ab8fdc69d698b3e1c17f9977afb6fea4f656/model-00001-of-00004.safetensors` |
| `models--Qwen--Qwen3.8-27B` | 65 | 51.8 GB | `snapshots/1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0` |
| `models--sentence-transformers--all-MiniLM-L6-v2` | 15 | 87.3 MB | `c9745ed1d9f207416be6d2e6f8de32d1f16199bf/model.safetensors` |
| `models--TinyLlama--TinyLlama-1.1B-Chat-v1.0` | 21 | 4.1 GB | `fe8a4ea1ffedaf415f4da2f062534de366a451e6/model.safetensors` |
| `ollama` | 9 | 1.7 GB | `blobs/`, `manifests/` |
| `RT-DETR-v1-R101` | 11 | 293.1 MB | `model.safetensors` |
| `stack-v2` | 28 | 67.7 GB | `data/C++/train-00002-of-00007.parquet` |
| `tiny-codes` | 19 | 935.9 MB | `part_8_1600000.parquet` |
| `yolo11x` | 2 | 327.4 MB | `yolo11x.torchscript`, `yolo11x.pt` |
