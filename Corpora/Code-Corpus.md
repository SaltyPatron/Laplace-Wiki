# Code corpus

The workspace-code source reads the active Laplace repositories with language grammars and extracts declarations through compiled semantic recipes.

## Source

[workspace-code/source](https://github.com/SaltyPatron/Laplace-Engine/blob/main/recipes/workspace-code/source) names one Laplace Workspace corpus trunk and lists the workspace repositories, including Laplace-Prototype. It follows `.gitignore`, skips hidden directories, and supersedes the previous source reading when files change or disappear.

## Records

The [language recipes](https://github.com/SaltyPatron/Laplace-Engine/tree/main/recipes/workspace-code) extract C/C++ functions and structures, C# types and members, Python functions/classes, TypeScript declarations and SQL declarations. Each declaration retains its complete source span beside its name, signature, members and body where those fields apply. Unselected top-level packaging is retained as source content. Name rules describe declarations rather than turning call-site member names into declared identifiers.

C export annotations and conditional linkage guards, and PostgreSQL extension-script syntax, have explicit grammar productions. Other selected workspace formats use their registered language grammar or the source's declared text recipe. Curated declaration capture does not claim that every language construct has a separate semantic rule or every file has completed database admission.

## Not read

Old project trees outside the listed workspace roots are not covered by this source. A checkout's presence on disk does not add it to the corpus automatically.
