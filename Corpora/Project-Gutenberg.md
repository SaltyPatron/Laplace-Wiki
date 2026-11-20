# Project Gutenberg

Project Gutenberg books separate wrapper header/footer metadata (`Title`, `Author`, `Language`, eBook number) from the pure work body so `.txt` and `.epub` editions converge on identical chapter, paragraph, and sentence `lp_id`s, while structured Gutenberg reference works (`webster-1913`, `roget-thesaurus`, `britannica-1911`, `sloane-electrical`) run dedicated lexicon and encyclopedia recipes.

Five sources in [`recipes/order`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/order) cover the [Project Gutenberg](https://www.gutenberg.org/) estate: `project-gutenberg` for literary and general prose works, and four curated reference corpora extracted with custom Tree-sitter grammars and semantic recipes.

## Sources

| Source | Witness | Trust class | After | Files | Recipes |
| --- | --- | --- | --- | --- | --- |
| `project-gutenberg` | Observed literary/prose works (edition metadata attested under Gutenberg wrapper recipe in `Batch 2`) | observed content (`StructuredCorpus` for bibliographic wrapper metadata) | `unicode` | `*.txt` and `*.epub` under `$LAPLACE_DATA/ProjectGutenberg` (excluding the four reference works below) | [`recipes/project-gutenberg/source`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/project-gutenberg/source) (currently `reads text`; `.txt`/`.epub` wrapper-stripping & edition convergence in `Batch 2`, `Laplace#1134`) |
| `webster-1913` | `Webster's Unabridged Dictionary (1913)` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `webster-unabridged-dictionary-1913.txt` (eBook #29765) | [`entries.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/webster-1913/entries.recipe) (`format webster`) |
| `roget-thesaurus` | `Roget's Thesaurus` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `rogets-thesaurus-of-english-words-and-phrases.txt` | [`thesaurus.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/roget-thesaurus/thesaurus.recipe) |
| `britannica-1911` | `Encyclopaedia Britannica (1911)` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `britannica-1911-*.txt` | [`articles.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/britannica-1911/articles.recipe) (`format britannica`) |
| `sloane-electrical` | `Sloane's Standard Electrical Dictionary` source trunk | class `AcademicCurated` | `unicode`, `iso-639` | `standard-electrical-dictionary-sloane.txt` | [`dictionary.recipe`](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/sloane-electrical/dictionary.recipe) |

## Edition convergence across `.txt` and `.epub` (`project-gutenberg`)

Every Project Gutenberg `.txt` release wraps the public-domain work between `*** START OF THE PROJECT GUTENBERG EBOOK ... ***` (preceded by `Title:`, `Author:`, `Release date:`, `Language:`, eBook `#N`) and `*** END OF THE PROJECT GUTENBERG EBOOK ... ***` (followed by full license prose), while `.epub` releases package OPF Dublin Core metadata (`dc:title`, `dc:creator`, `dc:language`, `dc:identifier`) alongside XHTML chapter documents inside a ZIP container.

Under the Recording Law ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md), `Batch 2` `Laplace#1134`):

- **Wrapper metadata separation:** Header/OPF bibliographic fields (`Title`, `Author`, `Language` → ISO 639 node, eBook number) belong to the edition's metadata/bibliographic record, and Gutenberg license footers are packaging—never merged into the literary work's body paragraphs.
- **Cross-edition body convergence:** Stripping Gutenberg's wrapper markers and unwrapping hard-wrapped 72-column plain-text lines inside paragraphs lets `.txt` and `.epub` editions of the same work decompose (`work → chapter → paragraph → sentence → word → grapheme → codepoint`) onto **identical chapter, paragraph, and sentence `lp_id`s** (`Batch 2` recipe gap: `project-gutenberg/source` currently runs stock `reads text` over whole `.txt` files including boilerplate headers/footers and does not yet unpack `.epub` containers).

| Piece | Laplace reads it as | Target representation & current recipe state |
| --- | --- | --- |
| PG header / `.epub` OPF (`Title`, `Author`, `Language`, eBook `#`) | edition bibliographic metadata linked to the pure work body; license footer omitted from work body | target: separated in `Batch 2` (`Laplace#1134`); currently ingested inline as plain text under `reads text` |
| Pure work body (`.txt` between `*** START` and `*** END`, `.epub` XHTML spine) | canonical `work → chapter → paragraph → sentence → word → grapheme → codepoint` trajectory | converges `.txt` and `.epub` onto identical sentence/paragraph `lp_id`s in `Batch 2` |

## Curated Gutenberg lexicons & encyclopedias

Unlike narrative novels, reference dictionaries and encyclopedias published through Project Gutenberg have explicit entry grammars ([INVENTOR_RECORD](../Repositories/Laplace/docs/INVENTOR_RECORD.md): *"if its the gutenberg websters unabridged... it follows a format we should be able to properly decompose"*):

- **`webster-1913` (`entries.recipe`, `format webster`):** Parses capitalized headwords, syllabification/pronunciation, `webster-pos` parts of speech crosswalked to `upos`, domain labels (`(Gram.)`, `(Med.)`, `(Zoöl.)`), `Defn:` sense paragraphs, literary quotations, `Syn.` synonym lists, and `See` cross-references.
- **`roget-thesaurus` (`thesaurus.recipe`):** Parses numbered conceptual classes, divisions, sections, head categories, POS groups (`roget-pos` crosswalked to `upos`), and synonym/antonym clusters.
- **`britannica-1911` (`articles.recipe`, `format britannica`):** Parses 11th-edition encyclopedia article headwords, cross-references, and article prose trajectories.
- **`sloane-electrical` (`dictionary.recipe`):** Parses technical headwords, definitions, and cross-references from Sloane's *Standard Electrical Dictionary*.
