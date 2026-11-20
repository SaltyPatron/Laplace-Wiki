# Code authority

The `cpython`, `docs`, `postgres`, and `runtime` upstream reference checkouts are queued for declarative `.recipe`, Tree-sitter AST, `.git` Merkle DAG, and compiler/LSP symbol-witness admission (`Batch 2`/`Batch 3`, `Laplace#894`), attesting authoritative language grammars, SQL command specifications, and standard-library API contracts over canonical AST declarations.

## Source & `Batch 3` admission queue

Upstream canonical source and specification checkouts—Python (`cpython`), .NET/C# language and API documentation (`docs`) plus runtime implementation (`runtime`), and PostgreSQL (`postgres`)—are queued for curated source admission alongside native `.git` commit-DAG and compiler/LSP symbol witnessing in `Batch 3` (`Laplace#894`, extending the grammar-and-declaration pipeline already active for [Code corpus](Code-Corpus.md)). Each upstream project forms its own corpus witness trunk (`class StandardsDerived` / `AcademicCurated`).

Under the Recording Law ([26. Code](../Sequence/Code.md)):

- **Zero chunking—pure AST + document hierarchy:** Source files decompose losslessly through compiled Tree-sitter grammars (`python`, `c`, `c_sharp`, `sql`, `rst`, `xml`, `yaml`, `markdown`) down to UAX #29 identifier and prose leaves, so standard-library signatures (`os.makedirs`, `System.Span<T>`, `SPI_exec`) collide on the exact same identifier and AST `lp_id`s referenced in user repositories and [Code corpus](Code-Corpus.md).
- **Authoritative specification binding:** Language reference sections, DocBook/SGML command synopses (`SELECT`, `CREATE EXTENSION`), Python PEP 257 docstrings, and C# `///` XML documentation tags (`<summary>`, `<param>`, `<returns>`, `<exception>`) attest formal contracts directly on the AST declarations they document.

## Publisher record format

| Artifact | Structure | Target Laplace semantics | Upstream reference |
| --- | --- | --- | --- |
| Python & C# language reference (`cpython/Doc/reference/*.rst`, `docs/docs/csharp/language-reference/**`) | reStructuredText / Markdown + YAML frontmatter & EBNF grammar productions | Hierarchical section, grammar production, and normative prose trajectories under the language authority's trunk | [Python Language Reference](https://docs.python.org/3/reference/index.html); [C# Language Reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/) |
| PostgreSQL command & catalog reference (`postgres/doc/src/sgml/ref/*.sgml`, `reference.sgml`) | DocBook `<refentry>` (`refentrytitle`, `manvolnum`, `refmiscinfo`, `refname`, `refpurpose`, `refsynopsisdiv`, `refsect1`) | Structured SQL command synopsis, parameter definitions, and behavioral guarantees linked to SQL AST constructs | [PostgreSQL SQL Commands](https://www.postgresql.org/docs/current/sql-commands.html) |
| Python standard-library docstrings (`cpython/Lib/**/*.py`) | Module, class, and `def` AST nodes with leading string-literal docstring | Function/class declaration AST (`name`, `parameters`, `return_type`, `body`) paired with its attested docstring specification | [PEP 257](https://peps.python.org/pep-0257/) |
| .NET runtime `///` XML API comments (`runtime/src/libraries/**/*.cs`) | C# type/member AST declarations with structured `///` XML tags (`summary`, `param`, `typeparam`, `returns`, `remarks`, `exception`) | Public type/member signature AST bound to parameter, return, and exception contracts | [.NET XML Documentation Comments](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/) |
