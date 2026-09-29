# Code authority

The four checkouts `cpython`, `docs`, `postgres`, and `runtime` are source and documentation collections.

## Value

| Attestation | What it means | Lands on | Value | Witness | Proof |
| --- | --- | --- | --- | --- | --- |
| Python language reference | This reference manual describes the Python programming language. It is not intended as a tutorial. Syntax and lexical analysis are the parts written as formal specifications; the rest is English. | the Python language | the reference manual in Doc/reference | CPython | cpython/Doc/reference/introduction.rst |
| docstring | A library function's docstring is the string under its def. os.makedirs documents itself as creating a leaf directory and all intermediate ones. | a function in the CPython library | the docstring text | CPython | cpython/Lib/os.py, makedirs |
| C# language reference | The language reference provides an informal reference to C# syntax and idioms for beginners and experienced C# and .NET developers. | C# | the pages under docs/csharp/language-reference | .NET docs | docs/docs/csharp/language-reference/index.yml |
| Visual Basic language reference | Provides reference information for various aspects of the Visual Basic language. The same page says the Visual Basic language specification contains detailed information on all aspects of the language. | Visual Basic | the language reference linked from docs/visual-basic/reference/index.md | .NET docs | docs/docs/visual-basic/reference/index.md |
| SQL command | The SQL Commands part contains reference information for the SQL commands supported by PostgreSQL. By SQL the language in general is meant. SELECT, TABLE, and WITH retrieve rows from a table or view. | an SQL command | the reference page for that command | PostgreSQL | postgres/doc/src/sgml/reference.sgml and postgres/doc/src/sgml/ref/select.sgml |
| doc comment | All public API documentation (`/// <summary>`, `/// <param>`, and the rest) must be placed on the primary source file named TypeName.cs. The docs README says some API reference is generated directly from the /// in the product source. | a public API in the .NET runtime | the /// summary and param comments | .NET runtime | runtime/docs/coding-guidelines/adding-api-guidelines.md; docs/README.md |

## Format

| Record | Fields in order | What a record is | Proof |
| --- | --- | --- | --- |
| language reference section | Not defined as a fielded record | The Python reference and the C# language reference are prose and syntax descriptions, not a table of records. introduction.rst and index.yml were opened. | cpython/Doc/reference/introduction.rst; docs/docs/csharp/language-reference/index.yml |
| SQL reference entry | refentrytitle, manvolnum, refmiscinfo, refname, refpurpose, synopsis | The SELECT page is a refentry. reference.sgml says each entry is an authoritative, complete, and formal summary of its subject. Other command pages were not each opened, so this field order is the SELECT page's order. | postgres/doc/src/sgml/ref/select.sgml; postgres/doc/src/sgml/reference.sgml |
| docstring | the string literal immediately under the def | The documentation of that function, as os.makedirs writes it. No separate label vocabulary is in the checkout. | cpython/Lib/os.py |
| XML doc comment | summary, param, and the other /// tags the guideline names | The public API documentation on the primary source file. No separate label vocabulary is in the checkout. | runtime/docs/coding-guidelines/adding-api-guidelines.md |
