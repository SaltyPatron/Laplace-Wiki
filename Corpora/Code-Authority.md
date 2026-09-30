# Code authority

The `cpython`, `docs`, `postgres`, and `runtime` checkouts have no recipe yet, so they are not ingested and attest nothing.

## Source

No directory under [`recipes/`](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes) reads this collection, and `recipes/order` does not name it. Until a recipe exists, nothing in it is decomposed, recorded, or attested; see [Attestations](../Semantics/Attestations.md#observations). The format below is the publisher's, kept so that a recipe can be written from it.

## Format

| Record | Fields in order | What a record is | Specification |
| --- | --- | --- | --- |
| language reference section | Not defined as a fielded record | The Python reference and the C# language reference are prose and syntax descriptions, not a table of records. introduction.rst and index.yml were opened. | cpython/Doc/reference/introduction.rst; docs/docs/csharp/language-reference/index.yml |
| SQL reference entry | refentrytitle, manvolnum, refmiscinfo, refname, refpurpose, synopsis | The SELECT page is a refentry. reference.sgml says each entry is an authoritative, complete, and formal summary of its subject. Other command pages were not each opened, so this field order is the SELECT page's order. | postgres/doc/src/sgml/ref/select.sgml; postgres/doc/src/sgml/reference.sgml |
| docstring | the string literal immediately under the def | The documentation of that function, as os.makedirs writes it. No separate label vocabulary is in the checkout. | cpython/Lib/os.py |
| XML doc comment | summary, param, and the other /// tags the guideline names | The public API documentation on the primary source file. No separate label vocabulary is in the checkout. | runtime/docs/coding-guidelines/adding-api-guidelines.md |
