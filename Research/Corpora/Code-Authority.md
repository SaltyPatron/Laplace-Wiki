# Code authority

The four checkouts `cpython`, `docs`, `postgres`, and `runtime` are source and documentation collections.

## Files

| Path | Bytes | What the file is | Proof |
| --- | --- | --- | --- |
| /vault/Data/code-authority/cpython | 183152964 | CPython source and documentation checkout. README.rst begins 'This is Python version 3.16.0 alpha 0' and lists the source code and the documentation. Doc/reference/introduction.rst is the language reference. Lib/os.py carries function docstrings. | cpython/README.rst; cpython/Doc/reference/introduction.rst; cpython/Lib/os.py |
| /vault/Data/code-authority/docs | 674921692 | .NET docs checkout. README.md says this repository contains the conceptual documentation for .NET. docs/docs/csharp/language-reference is the C# language reference. docs/docs/visual-basic/reference/index.md links the Visual Basic language reference. | docs/README.md; docs/docs/csharp/language-reference/index.yml; docs/docs/visual-basic/reference/index.md |
| /vault/Data/code-authority/postgres | 185966288 | PostgreSQL source checkout. README.md says this directory contains the source code distribution of PostgreSQL, which supports an extended subset of the SQL standard. doc/src/sgml/ref holds the SQL command reference pages. | postgres/README.md; postgres/doc/src/sgml/reference.sgml; postgres/doc/src/sgml/ref/select.sgml |
| /vault/Data/code-authority/runtime | 812190226 | .NET runtime checkout. README.md says this repo contains the code to build the .NET runtime, libraries, and shared host, and the sources to the .NET runtime and libraries. Public API documentation is the /// comments on the primary source file. | runtime/README.md; runtime/docs/coding-guidelines/adding-api-guidelines.md |

## Attestations

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Python language reference | This reference manual describes the Python programming language. It is not intended as a tutorial. Syntax and lexical analysis are the parts written as formal specifications; the rest is English. | the Python language | the reference manual in Doc/reference | CPython | cpython/Doc/reference/introduction.rst |
| docstring | A library function's docstring is the string under its def. os.makedirs documents itself as creating a leaf directory and all intermediate ones. | a function in the CPython library | the docstring text | CPython | cpython/Lib/os.py, makedirs |
| C# language reference | The language reference provides an informal reference to C# syntax and idioms for beginners and experienced C# and .NET developers. | C# | the pages under docs/csharp/language-reference | .NET docs | docs/docs/csharp/language-reference/index.yml |
| Visual Basic language reference | Provides reference information for various aspects of the Visual Basic language. The same page says the Visual Basic language specification contains detailed information on all aspects of the language. | Visual Basic | the language reference linked from docs/visual-basic/reference/index.md | .NET docs | docs/docs/visual-basic/reference/index.md |
| SQL command | The SQL Commands part contains reference information for the SQL commands supported by PostgreSQL. By SQL the language in general is meant. SELECT, TABLE, and WITH retrieve rows from a table or view. | an SQL command | the reference page for that command | PostgreSQL | postgres/doc/src/sgml/reference.sgml and postgres/doc/src/sgml/ref/select.sgml |
| doc comment | All public API documentation (`/// <summary>`, `/// <param>`, and the rest) must be placed on the primary source file named TypeName.cs. The docs README says some API reference is generated directly from the /// in the product source. | a public API in the .NET runtime | the /// summary and param comments | .NET runtime | runtime/docs/coding-guidelines/adding-api-guidelines.md; docs/README.md |

## Records

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| language reference section | Not defined as a fielded record | The Python reference and the C# language reference are prose and syntax descriptions, not a table of records. introduction.rst and index.yml were opened. | cpython/Doc/reference/introduction.rst; docs/docs/csharp/language-reference/index.yml |
| SQL reference entry | refentrytitle, manvolnum, refmiscinfo, refname, refpurpose, synopsis | The SELECT page is a refentry. reference.sgml says each entry is an authoritative, complete, and formal summary of its subject. Other command pages were not each opened, so this field order is the SELECT page's order. | postgres/doc/src/sgml/ref/select.sgml; postgres/doc/src/sgml/reference.sgml |
| docstring | the string literal immediately under the def | The documentation of that function, as os.makedirs writes it. No separate label vocabulary is in the checkout. | cpython/Lib/os.py |
| XML doc comment | summary, param, and the other /// tags the guideline names | The public API documentation on the primary source file. No separate label vocabulary is in the checkout. | runtime/docs/coding-guidelines/adding-api-guidelines.md |

## Lineage

| Paths | What is shared | Proof |
| --- | --- | --- |
| /vault/Data/code-authority/cpython, /vault/Data/code-authority/docs, /vault/Data/code-authority/postgres, /vault/Data/code-authority/runtime | Four separate checkouts. cpython is Python, docs is the .NET conceptual documentation, postgres is PostgreSQL, and runtime is the .NET runtime. docs/README.md says some published API reference is generated from /// comments in product source, and the runtime guideline says those comments live on the primary source file. No /// comment was compared with a page in the docs checkout. | The four README files and runtime/docs/coding-guidelines/adding-api-guidelines.md |
