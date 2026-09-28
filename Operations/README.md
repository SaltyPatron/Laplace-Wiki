# Operations

Operations covers what Laplace runs on and how it is built, configured, deployed, and tuned, from bare hardware to loaded, indexed, and measured content.

- [Setup](Setup.md): hardware, storage layout, repositories, and toolchain.
- [Builds](Builds.md): building PostgreSQL, Laplace-Native, and Laplace-postgres.
- [Database](Database.md): the PostgreSQL configuration Laplace needs, and why.
- [Deployment](Deployment.md): from an empty server to benchmarked content.

Measurements quoted on these pages come from [Engine Measurements](../Research/Engine.md), taken on a reference machine: a 6-core Intel Core i7-6850K with 125 GB of RAM, an NVMe drive for the database heap, and SATA SSDs for the write-ahead log and temporary files.
